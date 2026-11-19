# Autonomous WhatsApp AI Agent for E-Commerce

An AI-powered e-commerce assistant that interacts with customers through
WhatsApp, understands natural-language shopping requests, and uses
Python tools to perform real operations on an e-commerce backend.

The agent can search products, manage shopping carts, place orders,
track orders, and cancel orders. Product prices, inventory, and order
information are retrieved from the backend rather than invented by the
AI.

## Features

-   WhatsApp messaging integration using Neonize
-   AI agent powered by Groq
-   Tool/function calling with 10 Python tools
-   FastAPI backend
-   SQLite database with SQLAlchemy
-   Product and category management
-   Product search and stock checking
-   Shopping cart operations
-   Checkout with shipping address
-   Order tracking and cancellation
-   Inventory updates when orders are placed or cancelled
-   Separate conversation sessions for customers
-   English and Arabic responses
-   WhatsApp message filtering to ignore old messages and restrict group
    responses

## Architecture

``` text
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

The AI agent selects the appropriate tool based on the customer's
request. The tool sends a request to the backend, receives the real
result, and returns it to the agent. The agent then generates a response
based on that result.

## Technologies

-   Python
-   Groq API
-   FastAPI
-   SQLite
-   SQLAlchemy
-   Neonize
-   Requests
-   python-dotenv

## Project Structure

``` text
ecommerce-whatsapp-agent/
├── agent.py
├── bot.py
├── tools.py
├── simulate_chat.py
├── requirements.txt
├── .env.example
├── .gitignore
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed_data.py
│   └── ecommerce.db
└── whatsapp_session.db
```

Database files and WhatsApp session files are created locally and should
not be committed to GitHub.

## AI Agent Tools

The agent has access to the following 10 tools:

  -----------------------------------------------------------------------
  Tool                                Description
  ----------------------------------- -----------------------------------
  `list_categories`                   Lists available product categories.

  `search_products`                   Searches for products using a
                                      keyword, category, and stock
                                      filter.

  `get_product_details`               Retrieves details for a specific
                                      product.

  `get_customer_cart`                 Retrieves the customer's current
                                      cart and total.

  `add_item_to_cart`                  Adds a product and quantity to the
                                      customer's cart.

  `remove_cart_item`                  Removes an item from the cart using
                                      its cart item ID.

  `clear_customer_cart`               Clears all items from the
                                      customer's cart.

  `checkout_cart`                     Creates an order using the cart and
                                      shipping address.

  `track_order`                       Retrieves information about an
                                      order.

  `cancel_order`                      Cancels an order and restores the
                                      purchased quantities to stock.
  -----------------------------------------------------------------------

## Backend API

The backend provides REST API endpoints for categories, products, carts,
and orders.

### Categories

-   Create a category
-   List categories
-   Retrieve a category
-   Delete a category

### Products

-   Create a product
-   List and search products
-   Filter by category, price, and stock
-   Retrieve product details
-   Update a product
-   Delete a product

### Cart

-   Add items
-   View cart
-   Update item quantities
-   Remove items
-   Clear a customer's cart

### Orders

-   Checkout
-   List orders
-   Retrieve an order
-   Update order status
-   Cancel an order

The API documentation is available through FastAPI's Swagger interface
after the backend starts:

`http://127.0.0.1:8000/docs`

## Initial Store Data

The seed script populates the database with:

### Categories

-   Electronics
-   Accessories
-   Audio

### Sample Products

-   Mechanical Keyboard
-   Wireless Gaming Mouse
-   Gaming Monitor 27-inch
-   USB-C Fast Charging Cable
-   Aluminum Laptop Stand
-   Noise Cancelling Headphones
-   Waterproof Bluetooth Speaker (initially out of stock)

The seed script skips seeding if category data already exists.

## Requirements

-   Python installed
-   A Groq API key
-   WhatsApp account for pairing with the bot

## Installation and Setup

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ecommerce-whatsapp-agent
```

### 2. Create and activate a virtual environment

macOS/Linux:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a
template.

Add your Groq API key:

``` env
GROQ_API_KEY=your_groq_api_key
```

Do not commit `.env` or expose API keys publicly.

### 5. Initialize and seed the database

``` bash
cd backend
python seed_data.py
```

The seed script creates the database tables and initial
categories/products if the database is empty.

## Running the Application

The backend and WhatsApp bot run separately. Keep both running.

### Terminal 1 --- Start the backend

From the project root:

``` bash
cd backend
uvicorn main:app --reload
```

Backend address:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### Terminal 2 --- Start the WhatsApp bot

From the project root, activate the virtual environment if necessary,
then run:

``` bash
python bot.py
```

Follow the QR pairing instructions if WhatsApp requests pairing.

The bot listens for incoming messages, passes eligible messages to the
AI agent, and sends the generated response back through WhatsApp.

## Running the Chat Simulator

The terminal simulator can be used to test the agent without sending
WhatsApp messages.

Make sure the backend is running, then from the project root run:

``` bash
python simulate_chat.py
```

## Example Customer Requests

-   "What electronics do you have?"
-   "Do you have a mechanical keyboard in stock?"
-   "Add one keyboard and two gaming mice to my cart."
-   "Show me my cart."
-   "I want to checkout. My address is ..."
-   "Track my order."
-   "Cancel my order."

The agent uses backend tool results to provide product information, cart
totals, order details, and stock information.

## Important Notes

-   The backend must be running before the agent tools can communicate
    with it.
-   The WhatsApp bot and backend run in separate terminal sessions.
-   The database is local SQLite storage.
-   WhatsApp login/session data is stored locally.
-   Never upload API keys, private WhatsApp session files, or local
    database files to a public repository.
-   The bot's message filters are configured in `bot.py`.

## Demo

A demonstration video showing the WhatsApp interaction, product search,
multi-tool calling, cart operations, checkout, order tracking, and
cancellation will be added here.

## Author

CodeMZ Internship Project
