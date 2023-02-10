from django.views import View
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import ItemModel


stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemDetailPageView(TemplateView):

    
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailPageView, self).get_context_data(**kwargs)
        item_id = context['pk']
        item = ItemModel.objects.get(id=item_id)
        context.update({
            'item': item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    
    def get(self, request, *args, **kwargs):

        item_id = self.kwargs['pk']
        item = ItemModel.objects.get(id=item_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000/"
        checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'name': '{{ item.name }}',
                        'desc': '{{ item.description }}',
                        'price': '{{ item.price }}',
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