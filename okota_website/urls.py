from django.conf.urls import patterns, include, url
from okota.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from tastypie.api import Api
from okota.api.resources import *

admin.autodiscover()
handler404='okota.views.custom_404'
handler500='okota.views.custom_500'
v1_api = Api(api_name='v1')
v1_api.register(UserProfileResource())
v1_api.register(CreateUserResource())
v1_api.register(UserResource())
v1_api.register(StoreProductResource())
v1_api.register(ProductResource())
v1_api.register(RetailStoreResource())
v1_api.register(DeliveryPersonnelResource())
v1_api.register(LocationDetailResource())


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^add-product-to-cart/', AddProductToCartView.as_view(), name="add-product-to-cart"),
    url(r'^order-complete/', OrderCompleteView.as_view(), name="order-complete"),
    url(r'^order-failed/', OrderFailedView.as_view(), name="order-failed"),
    url(r'^legals/', LegalsView.as_view(), name="legals"),
    url(r'^faq/', FaqView.as_view(), name="faq"),
    url(r'^check-out/', CheckOutView.as_view(), name="check-out"),
    url(r'^$', LandingView.as_view(), name="category-bunny-chow"),
)