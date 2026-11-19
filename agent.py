
import json
from dotenv import load_dotenv
from groq import Groq

import tools


# Load environment variables
load_dotenv()

# Initialize Groq
groq_client = Groq()

MODEL_NAME = "openai/gpt-oss-120b"

print("Groq client initialized successfully!")


# Connect tool names to their actual Python functions
AVAILABLE_FUNCTIONS = {
    "list_categories": tools.list_categories,
    "search_products": tools.search_products,
    "get_product_details": tools.get_product_details,
    "get_customer_cart": tools.get_customer_cart,
    "add_item_to_cart": tools.add_item_to_cart,
    "remove_cart_item": tools.remove_cart_item,
    "clear_customer_cart": tools.clear_customer_cart,
    "checkout_cart": tools.checkout_cart,
    "track_order": tools.track_order,
    "cancel_order": tools.cancel_order,
}


# Define the tools available to the AI
GROQ_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_categories",
            "description": "Get all available product categories.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": (
                "Search the product catalog by name or keyword. "
                "Use the exact product name when known. "
                "Search once per requested product. "
                "Do not repeat a search if a matching product was found."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Product name or keyword."
                    },
                    "category_id": {
                        "type": "integer",
                        "description": "Optional category ID."
                    },
                    "in_stock_only": {
                        "type": "boolean",
                        "description": "Whether to show only products in stock."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_details",
            "description": "Get complete details of a product using its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer"}
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_cart",
            "description": "View a customer's shopping cart.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"}
                },
                "required": ["customer_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_item_to_cart",
            "description": (
                "Add the requested product and quantity to a customer's cart. "
                "Never use this to replace or modify other cart items."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"},
                    "product_id": {"type": "integer"},
                    "quantity": {"type": "integer"}
                },
                "required": ["customer_name", "product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_cart_item",
            "description": (
                "Remove a specific cart item ONLY when the customer "
                "explicitly asks to remove that item."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {"type": "integer"}
                },
                "required": ["item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "clear_customer_cart",
            "description": (
                "Clear the entire cart ONLY when the customer "
                "explicitly asks to empty or clear their cart."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"}
                },
                "required": ["customer_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "checkout_cart",
            "description": (
                "Place an order using the customer's cart. "
                "A shipping address is required. "
                "The customer phone number is optional."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"},
                    "shipping_address": {"type": "string"},
                    "customer_phone": {"type": "string"}
                },
                "required": ["customer_name", "shipping_address"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "track_order",
            "description": "Track an order using its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": (
                "Cancel an order ONLY when the customer explicitly "
                "requests cancellation."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer"}
                },
                "required": ["order_id"]
            }
        }
    }
]



customer_sessions = {}


def run_agent(user_message: str, session_id: str = "default"):
    """Process a customer message and remember each customer's conversation."""

    system_message = {
        "role": "system",
        "content": (

            "Use this session ID as the customer_name for all cart and order tools: "
            + session_id + ". "
            "You are a professional e-commerce assistant. "

            "LANGUAGE RULES: "
            "Always reply in the same language as the customer's latest "
            "message. English messages must receive English replies. "
            "Arabic messages must receive Arabic replies. "
            "Never reply in Turkish unless the customer uses Turkish. "
            "Do not randomly switch languages. "

            "TOOL RULES: "
            "Use the available tools to complete customer requests. "
            "Use the minimum number of tool calls needed. "
            "Search once for each distinct requested product. "
            "Do not repeat searches without a clear reason. "
            "Do not call list_categories unless the customer asks "
            "about product categories. "

            "CART PROTECTION RULES: "
            "NEVER remove or clear cart items unless the customer "
            "explicitly asks to remove or clear them. "
            "NEVER use remove_cart_item or clear_customer_cart "
            "to adjust quantities or correct an earlier action. "
            "Only add the exact products and quantities requested. "
            "Do not undo, replace, or modify previous cart items "
            "unless the customer explicitly requests that change. "

            "SHOPPING RULES: "
            "Check product availability before adding products. "
            "Never add a product if its stock is insufficient. "
            "Never invent prices, stock quantities, or order details. "
            "Use backend results as the only source of truth. "

            "CHECKOUT RULES: "
            "Always obtain the customer's shipping address before "
            "calling checkout_cart. "
            "Never use a phone number as a shipping address. "
            "If the shipping address is missing, ask the customer for it. "
            "Do not place an order without a valid shipping address. "

            "ACTION RULES: "
            "Never claim an action succeeded unless the relevant "
            "tool confirms success. "
            "If information required to complete an action is missing, "
            "ask the customer for it."
        )
    }

    if session_id not in customer_sessions:
        customer_sessions[session_id] = [system_message]

    messages = customer_sessions[session_id]
    messages.append({
        "role": "user",
        "content": user_message
    })

    for _ in range(10):

        response = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=GROQ_TOOLS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        if not assistant_message.tool_calls:
            return assistant_message.content or "I couldn't generate a response."

        for tool_call in assistant_message.tool_calls:

            function_name = tool_call.function.name

            try:
                arguments = json.loads(tool_call.function.arguments)

                if function_name not in AVAILABLE_FUNCTIONS:
                    result = {
                        "error": f"Unknown function: {function_name}"
                    }
                else:
                    result = AVAILABLE_FUNCTIONS[function_name](**arguments)

            except Exception as error:
                result = {"error": str(error)}

            print(f"Executed: {function_name}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    result,
                    ensure_ascii=False,
                    default=str
                )
            })

    return "Too many tool calls. Please try again."
