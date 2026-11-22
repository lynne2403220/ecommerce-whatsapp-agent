# Autonomous WhatsApp AI Agent for E-Commerce

An AI-powered e-commerce assistant that interacts with customers through WhatsApp, understands natural-language shopping requests, and performs real operations through an e-commerce backend.

The agent uses tool/function calling to retrieve backend data and execute shopping workflows. Product prices, inventory, carts, and order information come from the backend—not from AI-generated guesses.

## Features

- WhatsApp messaging integration using Neonize
- AI agent powered by Groq
- Tool/function calling with 10 Python tools
- FastAPI REST backend
- SQLite database with SQLAlchemy
- Product and category management
- Product search, details, and stock checking
- Shopping cart operations
- Checkout with shipping address
- Order tracking and cancellation
- Inventory updates when orders are placed or cancelled
- Customer-specific conversation sessions
- English and Arabic interactions
- WhatsApp message filtering to ignore older messages and restrict responses to the configured group

## Architecture

```text
Customer on WhatsApp
        |
        v
WhatsApp Integration (Neonize)
        |
        v
AI Agent (Groq)
        |
        | Tool calling
        v
Python Tools (tools.py)
        |
        | HTTP requests
        v
FastAPI Backend
        |
        v
SQLite Database
```

The AI agent selects tools based on the customer's request. The tools communicate with the backend, return actual results, and the agent generates a response based on those results.

## Technologies

- Python
- Groq API
- FastAPI
- SQLite
- SQLAlchemy
- Neonize
- Requests
- python-dotenv

## Project Structure

```text
ecommerce-whatsapp-agent/
├── agent.py
├── bot.py
├── tools.py
├── simulate_chat.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── backend/
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    └── seed_data.py
```

Local database files and WhatsApp session files are generated locally and excluded from version control.

## AI Agent Tools

| Tool | Description |
|---|---|
| `list_categories` | Lists available product categories. |
| `search_products` | Searches products by keyword, category, and stock filter. |
| `get_product_details` | Retrieves details for a product. |
| `get_customer_cart` | Retrieves a customer's cart and total. |
| `add_item_to_cart` | Adds a product and quantity to a customer's cart. |
| `remove_cart_item` | Removes a cart item by its item ID. |
| `clear_customer_cart` | Clears a customer's cart. |
| `checkout_cart` | Creates an order from a cart and shipping address. |
| `track_order` | Retrieves order information. |
| `cancel_order` | Cancels an order and restores purchased quantities to stock. |

## Backend API

The REST API provides endpoints for categories, products, carts, and orders.

### Categories
- Create, list, retrieve, and delete categories

### Products
- Create, list, search, and retrieve products
- Filter products by category, price, and stock
- Update and delete products

### Cart
- Add items
- View cart
- Update item quantities
- Remove items
- Clear a customer's cart

### Orders
- Checkout
- List orders
- Retrieve an order
- Update order status
- Cancel orders

FastAPI Swagger documentation is available at:

http://127.0.0.1:8000/docs

## Initial Store Data

The seed script provides these categories:
- Electronics
- Accessories
- Audio

Sample products:
- Mechanical Keyboard
- Wireless Gaming Mouse
- Gaming Monitor 27-inch
- USB-C Fast Charging Cable
- Aluminum Laptop Stand
- Noise Cancelling Headphones
- Waterproof Bluetooth Speaker (initially out of stock)

The seed script skips seeding if category data already exists.

## Requirements

- Python 3
- Groq API key
- WhatsApp account for pairing the bot

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/lynne2403220/ecommerce-whatsapp-agent.git
cd ecommerce-whatsapp-agent
```

### 2. Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template. Set your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Do not commit `.env` or expose API keys.

### 5. Initialize the database

```bash
cd backend
python seed_data.py
```

The seed script creates the database tables and initial categories/products if the database is empty.

## Running the Application

The backend and WhatsApp bot run separately. Keep both running.

### Terminal 1 — Backend

From the project root:

```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Backend: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### Terminal 2 — WhatsApp Bot

From the project root, with the virtual environment activated:

```bash
python bot.py
```

Scan the QR code if WhatsApp pairing is requested. The bot receives eligible messages, sends them to the agent, and replies through WhatsApp.

## Chat Simulator

The simulator lets you interact with the AI agent without sending WhatsApp messages.

With the backend running, open another terminal at the project root and run:

```bash
python simulate_chat.py
```

## Example Customer Requests

- “What electronics do you have?”
- “Do you have a mechanical keyboard in stock?”
- “Add one keyboard and two gaming mice to my cart.”
- “Show me my cart.”
- “I want to checkout. My address is …”
- “Track my order.”
- “Cancel my order.”

## Demo Checklist

For a demonstration, show the following workflow:

1. Start the backend.
2. Start the WhatsApp bot and confirm it is connected.
3. Ask for available products and search for a product.
4. Add products to the cart and show the cart total.
5. Provide a shipping address and place an order.
6. Ask to track the order.
7. Demonstrate an Arabic customer request.
8. Optionally demonstrate order cancellation and stock restoration.

## Demo Video

[Watch the project demonstration](https://drive.google.com/file/d/14dm0i0vBRtbhXfOd57XGoCVHAVSaCnF2/view?usp=sharing)

## Notes and Limitations

- The backend must be running for agent tools to work.
- The backend and WhatsApp bot run in separate processes.
- The database uses local SQLite storage.
- WhatsApp login/session data is stored locally.
- Never upload API keys, WhatsApp session files, or local database files to a public repository.
- WhatsApp message filtering is configured in `bot.py`.

## Author

CodeMZ Internship Project
