
import requests

BASE_URL = "http://127.0.0.1:8000"


def _request(method, endpoint, **kwargs):
    """Send a request to the e-commerce backend."""
    try:
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            timeout=10,
            **kwargs
        )

        response.raise_for_status()

        if response.content:
            return response.json()

        return {"message": "Operation completed successfully"}

    except requests.exceptions.HTTPError:
        try:
            return {
                "error": True,
                "message": response.json().get("detail", response.text),
                "status_code": response.status_code
            }
        except ValueError:
            return {
                "error": True,
                "message": response.text,
                "status_code": response.status_code
            }

    except requests.exceptions.RequestException as error:
        return {
            "error": True,
            "message": f"Backend connection failed: {str(error)}"
        }


def list_categories():
    """Get all available product categories."""
    return _request("GET", "/categories")


def search_products(
    keyword: str = "",
    category_id: int = None,
    in_stock_only: bool = False
):
    """Search products by name, category, and stock availability."""
    params = {
        "search": keyword,
        "in_stock_only": in_stock_only
    }

    if category_id is not None:
        params["category_id"] = category_id

    return _request("GET", "/products", params=params)


def get_product_details(product_id: int):
    """Get complete details of a product using its ID."""
    return _request("GET", f"/products/{product_id}")


def get_customer_cart(customer_name: str):
    """Get the shopping cart belonging to a customer."""
    return _request("GET", f"/cart/{customer_name}")


def add_item_to_cart(
    customer_name: str,
    product_id: int,
    quantity: int = 1
):
    """Add a product to the customer's cart."""
    data = {
        "customer_name": customer_name,
        "product_id": product_id,
        "quantity": quantity
    }

    return _request("POST", "/cart/items", json=data)


def remove_cart_item(item_id: int):
    """Remove a specific item from a shopping cart."""
    return _request("DELETE", f"/cart/items/{item_id}")


def clear_customer_cart(customer_name: str):
    """Remove all items from a customer's shopping cart."""
    return _request("DELETE", f"/cart/{customer_name}")


def checkout_cart(
    customer_name: str,
    shipping_address: str,
    customer_phone: str = None
):
    """Place an order using the customer's cart and shipping address."""
    data = {
        "customer_name": customer_name,
        "shipping_address": shipping_address,
        "customer_phone": customer_phone
    }

    return _request("POST", "/checkout", json=data)


def track_order(order_id: int):
    """Retrieve the current status and details of an order."""
    return _request("GET", f"/orders/{order_id}")


def cancel_order(order_id: int):
    """Cancel an order and restore its purchased stock."""
    return _request("PUT", f"/orders/{order_id}/cancel")
