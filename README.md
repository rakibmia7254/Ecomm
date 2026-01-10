# Ecomm - Multi-Vendor E-Commerce Platform

Ecomm is a high-performance, multi-vendor e-commerce platform built with **Django 5.2**, **Vanilla JS**, and **Bootstrap**. It provides a robust architecture for marketplace owners where multiple sellers can manage their own storefronts while customers enjoy a seamless shopping experience.

## 🚀 Features

-   **Multi-Vendor Ecosystem**: Independent shop registration and management for sellers.
-   **Comprehensive Seller Dashboard**: Analytics, product CRUD, order management, and invoice generation.
-   **Inventory Management**: Track stock levels (`in_stock`) and manage product variants.
-   **Secure Checkout Flow**: Supports both **Cash On Delivery** and **Stripe-powered Credit Card** payments.
-   **Dynamic Cart System**: Session-based cart with real-time updates.
-   **Address Management**: Save and edit multiple shipping addresses.
-   **PDF Invoices**: Automatically generate downloadable PDF invoices for orders.
-   **Responsive UI**: Sleek, mobile-first design using modern Bootstrap components.
-   **Automated Slug Generation**: SEO-friendly URLs for products and categories.

---

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rakibmia7254/Ecomm.git
    cd Ecomm
    ```

2.  **Set up Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Database Configuration:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Admin Setup:**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Environment Variables:**
    Create a `.env` file or export your Stripe keys:
    ```bash
    export STRIPE_PUBLISHABLE_KEY='pk_test_...'
    export STRIPE_SECRET_KEY='sk_test_...'
    ```

6.  **Run Server:**
    ```bash
    python manage.py runserver
    ```

---

## 🛣️ API Endpoints & Routes

### 🏠 Home & Discovery
- `/` : Landing page with featured products/categories.
- `/search/?q={query}` : Search for products.
- `/subscribe/` : Newsletter subscription.

### 👤 User Management
- `/login/` : User authentication.
- `/signup/` : New user registration (Auto-generates unique usernames).
- `/logout/` : Session termination.
- `/profile/` : User profile, order history, and address management.
- `/save_address/` : Add new shipping address.
- `/edit_address/<id>/` : Modify existing address.

### 🛍️ Shopping & Orders
- `/products/<slug>/` : Product detail page.
- `/category/<slug>/` : Browse products by category.
- `/add_to_cart/<slug>/` : Add product to session cart.
- `/cart/` : View and manage cart items.
- `/checkout/` : Integrated checkout for cart items.
- `/checkout/<slug>/` : Instant "Buy Now" checkout.
- `/payment/<order_id>/` : Process single order payment.
- `/paymentCart/<order_id>/` : Process bulk cart payment.
- `/order/<id>/` : View order status and details.

### 🏪 Seller & Shop
- `/register_shop/` : Become a vendor and create a shop.
- `/shop/<id>/` : Public shop storefront.
- `/seller/dashboard/` : Overview of sales, products, and orders.
- `/seller/products/` : Manage vendor inventory.
- `/seller/add_product/` : List new products.
- `/seller/orders/` : View all orders placed for your shop.
- `/seller/shipping/<id>/` : Mark an order as delivered.
- `/seller/invoice/<id>/` : Download order invoice as PDF.

---

## 🛡️ Security & Validations
- **Circular Dependency Protection**: Resolved architectural loops between Products and Shops.
- **Stock Validation**: Prevents checkout if product `in_stock` is insufficient.
- **Ownership Security**: Sellers can only view or manage orders belonging to their own shop.
- **Unique Identification**: Automatic collision-handling for usernames and slugs.

## 📄 License
Licensed under the [MIT License](LICENSE).
