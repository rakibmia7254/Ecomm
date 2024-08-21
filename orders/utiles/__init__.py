import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(order):
    try:
        product = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': order.product.name,
                },
                'unit_amount': int(order.product.price * 100),  # Convert to cents
            },
            'quantity': order.quantity,
        }

        # Create a new checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[product],
            mode='payment',
            success_url='http://127.0.0.1:8000/payment_done',
            cancel_url='http://127.0.0.1:8000/payment_cancel',
        )
        return session
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def create_checkout_session_cart(order):
    try:
        line_items = []

        for product in order.orders_in.all():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.product.name,
                    },
                    'unit_amount': int(product.total_amount * 100),  # Convert to cents
                },
                'quantity': product.quantity,
            })

        # Create a new checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:8000/payment_done',
            cancel_url='http://127.0.0.1:8000/payment_cancel',
        )
        return session
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def check_payment_status(payment_intent_id):
    if not payment_intent_id:
        return "Unpaid"
    payment_intent = stripe.stripe.checkout.Session.retrieve(payment_intent_id)
    return payment_intent['payment_status']
