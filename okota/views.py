from django.views.generic import View
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext, loader
from django.db.models import Q
from okota.models import *
from datetime import datetime
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

class LandingView(View):
    def get(self, request, *args, **kwargs):
        context_variables={}
        try:
            #Generate area select options
            area_select_suburbs=[]
            area_select_options=[]
            areas = DeliveryFee.objects.filter().order_by('location__province')
            for area in areas:
                if area.location.suburb not in area_select_suburbs:
                    area_select_suburbs.append(area.location.suburb)
                    area_select_options.append({'suburb':area.location.suburb,
                                                'city':area.location.city,
                                                'province':area.location.province})
            context_variables['area_select_options']=area_select_options

            #TODO Handle featured kotas, using this method. lazy
            if not request.GET.get('category'):
                request.GET=request.GET.copy()
                request.GET['category']="City bowl"

            if not request.GET.get('filter_by'):
                request.GET=request.GET.copy()
                request.GET['filter_by']="Quick"

            if request.GET.get('category'):
                search_term = request.GET.get('category')
                filter_by = request.GET['filter_by']
                context_variables['search_term']=search_term
                context_variables['filter_by']=filter_by
                #Get all products delivered within area
                area = DeliveryFee.objects.filter(location__suburb=search_term,delivery_type=filter_by)
                area_stores = []
                for delivery_area in area:
                    area_stores.append(delivery_area.store)

                #Get all products owned by stores
                results_products = []
                for store in area_stores:
                    products=StoreProduct.objects.filter(store=store)
                    for product in products:
                        if product not in results_products:
                            results_products.append(product)
                context_variables['results_products']=results_products
            #Featured products
            featured_products = StoreProduct.objects.filter(featured=True)

            #Shopping cart
            if Order.objects.filter(session=request.session.session_key,checked_out=False).exists():
                shopping_cart = Order.objects.get(session=request.session.session_key,checked_out=False)
                context_variables['shopping_cart'] = shopping_cart

            #testimonials
            testimonials = Testimonial.objects.filter(is_moderated=True)
            context_variables['testimonials']=testimonials[:4]

            #Featured profiles
            context_variables['featured_products']=featured_products[:4]

            #Get landing page ad
            landing_page_ad=Advert.objects.filter()
            if len(landing_page_ad)>0:
                context_variables['landing_page_ad']= landing_page_ad[0]


            template = loader.get_template('landing.html')
            context= RequestContext(request,context_variables)
            return HttpResponse(template.render(context))

        except Exception,e:
            logger.warning(e.message)
            raise Http404


class AddProductToCartView(View):
    def post(self, request, *args, **kwargs):
        try:
            #Check/create shopping cart
            if not Order.objects.filter(session=request.session.session_key,checked_out=False).exists():
                shopping_cart = Order.objects.create(session=request.session.session_key,status='Shopping Cart',checked_out=False)
            else:
                shopping_cart = Order.objects.get(session=request.session.session_key,checked_out=False)
            #Get product details
            product = StoreProduct.objects.get(id=int(request.POST.get('product')))
            ingredients=[]
            for ingredient in request.POST.getlist('ingredients'):
                ingredients.append(ProductIngredient.objects.get(id=int(ingredient)))

            #Create order product
            order_product = OrderProduct.objects.create(product=product)

            #Create order product's attributes
            logger.info(ingredients)
            for ingredient in ingredients:
                logger.info(ingredient)
                product_attribute = OrderProductAttribute.objects.create(key=ingredient.key,value=True)
                product_attribute.save()
                order_product.attributes.add(product_attribute)
                order_product.save()

            #Add delivery personnel information
            search_term = request.POST.get('search_term')
            area = DeliveryFee.objects.get(location__suburb=search_term,store=product.store)
            order_product.delivery_fee=area
            order_product.save()


            #Add product to shopping cart/order
            shopping_cart.products.add(order_product)
            shopping_cart.save()
            next = '/check-out/'
            return HttpResponseRedirect(next)

        except Exception,e:
            logger.warning(e.message)
            raise Http404


def notify_admin_email(order):
    #send email notification to admin
    from django.core.mail import send_mail

    try:
        logger.info('Sending new order e-mail notification to admin')
        send_mail('New order: %s' % order.id, 'New Order received. http://www.okota.co.za/admin/okota/order/%s/' % order.id,'support@okota.co.za',['kearabiloe.ledwaba@gmail.com'])
        logger.info("E-mail sent.")
    except Exception as e:
        logger.error('E-mail failed. %s' % e)

    return

class CheckOutView(View):
    def get(self, request, *args, **kwargs):
        context_variables={}
        try:

            #Shopping cart
            if Order.objects.filter(session=request.session.session_key,checked_out=False).exists():
                shopping_cart = Order.objects.get(session=request.session.session_key,checked_out=False)
                context_variables['shopping_cart'] = shopping_cart
            else:
                #TODO return not items in cart error message
                shopping_cart = Order.objects.create(session=request.session.session_key,status='Shopping Cart',checked_out=False)

            #Calculate Delivery fee
            delivery_fee=0
            unique_stores=[]
            for product in shopping_cart.products.all():
                if product.delivery_fee not in unique_stores:
                    unique_stores.append(product.delivery_fee)
            for store in unique_stores:
                delivery_fee = delivery_fee+store.price
            context_variables['delivery_fee'] = delivery_fee

            #Calculate Estimated time of arrival
            eta=0
            for product in shopping_cart.products.all():
                if product.delivery_fee.eta > eta:
                    eta= product.delivery_fee.eta
            context_variables['eta'] = eta

            #Generate delivery time slots
            context_variables['delivery_time_slots'] = OrderTimeSlot.objects.filter()

            #Calculate cart cost
            cart_cost=delivery_fee
            for product in shopping_cart.products.all():
                cart_cost = cart_cost+product.product.price
            context_variables['cart_cost'] = cart_cost

            #Remove product from cart
            if request.GET.get('remove'):
                product = OrderProduct.objects.get(id=int(request.GET.get('remove')))
                if product in shopping_cart.products.all():
                    shopping_cart.products.remove(product)
                    return HttpResponseRedirect('/check-out/')

            elif request.GET.get('submit-order') :
                logger.info(shopping_cart)
                shopping_cart = Order.objects.get(id=shopping_cart.id)
                address_street = request.GET.get('address_street')
                address_suburb = request.GET.get('address_suburb')
                address_city = request.GET.get('address_city')
                address_province = request.GET.get('address_province')
                address_postal = request.GET.get('address_postal')
                address = LocationDetail.objects.create(street=address_street,
                                                 suburb=address_suburb,
                                                 city=address_city,
                                                 province=address_province,
                                                 postal_code=address_postal)
                address.save()
                shopping_cart.delivery_address=address
                shopping_cart.contact_person = request.GET.get('contact_name')
                new_contact = ContactDetail.objects.create(key=request.GET.get('contact_name'),value=request.GET.get('contact_number'))
                shopping_cart.contact_number = new_contact
                shopping_cart.payment_method = request.GET.get('payment_method')
                shopping_cart.checked_out=True
                shopping_cart.final_amount=cart_cost
                shopping_cart.datetime_stamp = datetime.now()
                shopping_cart.time_slot = OrderTimeSlot.objects.get(id=int(request.GET.get('delivery_timeslot')))
                shopping_cart.save()

                #Redirect to PayFast if payment method is pay fast
                if shopping_cart.payment_method == 'payfast' :
                    url='https://www.payfast.co.za/eng/process?cmd=_paynow&receiver=kearabiloe.ledwaba@gmail.com&item_name=Okota-Order%s&amount=%s&return_url=http://okota.co.za/order-complete/&cancel_url=http://okota.co.za/order-failed/' % (shopping_cart.id,cart_cost)
                    return HttpResponseRedirect(url)

                #TODO Notify admin using celery
                notify_admin_email(shopping_cart)

                return HttpResponseRedirect('/order-complete/?order_id=%s' % shopping_cart.id)
            previous = request.META.get('HTTP_REFERER', None) or '/'
            context_variables['previous'] = previous
            template = loader.get_template('check-out.html')
            context= RequestContext(request,context_variables)
            return HttpResponse(template.render(context))

        except Exception,e:
            logger.warning(e.message)
            raise Http404


def custom_404(request):
    context_variables={}
    template = loader.get_template('404.html')
    next = request.META.get('HTTP_REFERER', None) or '/'
    context_variables['next']=next
    context= RequestContext(request,context_variables)
    return HttpResponse(template.render(context))

def custom_500(request):
    context_variables={}
    template = loader.get_template('404.html')
    next = request.META.get('HTTP_REFERER', None) or '/'
    context_variables['next']=next
    context= RequestContext(request,context_variables)
    return HttpResponse(template.render(context))


class OrderCompleteView(View):
    def get(self, request, *args, **kwargs):
        context_variables={}
        template = loader.get_template('orders.html')
        request.GET=request.GET.copy()
        context_variables['order']= Order.objects.get(id=int(request.GET.get('order_id')))
        context= RequestContext(request,context_variables)
        return HttpResponse(template.render(context))


class OrderFailedView(View):
    def get(self, request, *args, **kwargs):
        context_variables={}
        template = loader.get_template('order-failure.html')
        context= RequestContext(request,context_variables)
        return HttpResponse(template.render(context))



class LegalsView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'legals.html')

class FaqView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'faq.html')