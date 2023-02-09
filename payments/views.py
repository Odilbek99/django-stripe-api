from django.views import View
import stripe
from django.conf import settings
from django.http import JsonResponse


stripe.api_key = settings.STRIPE_SECRET_KEY
class CreateCheckoutSessionView(View):
    
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000/"
        checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': '{{PRICE_ID}}',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )

        return JsonResponse({
            'id': checkout_session.id 
            })

    # return redirect(checkout_session.url, code=303)