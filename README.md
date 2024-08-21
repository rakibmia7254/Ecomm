  Ecomm README

Ecomm
=====

Ecomm is a multi-vendor e-commerce platform built using Django and Bootstrap. This project provides a scalable and customizable solution for building an online marketplace, where multiple sellers can list their products, and users can browse and purchase items seamlessly.

Features
--------

*   **Multi-Vendor Support**: Multiple sellers can register and manage their products.
*   **Responsive Design**: Built with Bootstrap, ensuring the platform is mobile-friendly and visually appealing.
*   **Seller Dashboard**: Comprehensive dashboard for sellers to manage orders, products, and sales.
*   **Product Management**: Add, edit, and remove products with ease.
*   **Order Tracking**: Buyers can track their orders from purchase to delivery.
*   **Stripe Payment Integration**: Secure and reliable payment processing using Stripe.
*   **User Authentication**: Secure authentication system with registration and login functionality.
*   **Customizable UI**: Easily customizable Bootstrap-based front end.

Installation
------------

1.  **Clone the repository:**
    
        git clone https://github.com/rakibmia7254/Ecomm.git
        cd ecomm
                    
    
2.  **Create a virtual environment:**
    
        python -m venv env
        source env/bin/activate  # On Windows use `env\Scripts\activate`
                    
    
3.  **Install the dependencies:**
    
        pip install -r requirements.txt
                    
    
4.  **Run database migrations:**
    
        python manage.py migrate
                    
    
5.  **Create a superuser:**
    
        python manage.py createsuperuser
                    
    
6.  **Configure Stripe:**
    *   Set up your Stripe API keys in your environment variables:
    
        export STRIPE_PUBLIC_KEY='your-public-key'
        export STRIPE_SECRET_KEY='your-secret-key'
                        
    
    *   Update your settings file to include Stripe configuration:
    
        STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
        STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
                        
    
7.  **Run the development server:**
    
        python manage.py runserver
                    
    
8.  **Access the application:** Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Usage
-----

*   Register as a seller to start listing products.
*   Use the seller dashboard to manage products, view orders, and track sales.
*   Buyers can browse products, add them to their cart, and proceed to checkout using Stripe for payments.
*   Admin users can manage all aspects of the platform from the Django admin interface.

Contributing
------------

Feel free to submit issues, fork the repository, and send pull requests. Contributions are welcome!

License
-------

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
