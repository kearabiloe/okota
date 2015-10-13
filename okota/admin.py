from django.contrib import admin
from okota.models import *
import logging

logger = logging.getLogger(__name__)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','checked_out','status']
    list_filter = ['checked_out']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['id','rating','reviewers_name','is_moderated']
    list_filter = ['is_moderated']


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['id','reviewers_name','is_moderated']
    list_filter = ['is_moderated']

admin.site.register(UserProfile)
admin.site.register(ContactDetail)
admin.site.register(LocationDetail)
admin.site.register(RetailStore)
admin.site.register(ProductIngredient)
admin.site.register(StoreProduct)
admin.site.register(DeliveryPersonnel)
admin.site.register(DeliveryFee)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProductAttribute)
admin.site.register(OrderProduct)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Testimonial,TestimonialAdmin)
admin.site.register(OrderTimeSlot)
admin.site.register(Advert)