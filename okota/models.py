from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class UserProfile(models.Model):
    """
    A model to store extra information for each user.
    """
    user = models.OneToOneField(User, related_name='profile')
    gender = models.CharField(_("gender"), max_length=10,null=True,blank=True, choices=(('Male','Male'),
                                                                   ('Female','Female'))
    )
    contacts = models.ManyToManyField('ContactDetail', null=True,blank=True)
    locations = models.ManyToManyField('LocationDetail', null=True, blank=True)
    def __unicode__(self):
        return self.user.username


class ContactDetail(models.Model):
    """
    A model to store contact information.
    """
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s = %s' % (self.key,self.value)


class LocationDetail(models.Model):
    """
    A model to store location information.
    """
    description = models.CharField(max_length=100, null=True,blank=True)
    street = models.CharField(max_length=100, null=True,blank=True)
    suburb = models.CharField(max_length=100, null=True,blank=True)
    city = models.CharField(max_length=100, null=True,blank=True)
    province = models.CharField(max_length=100, null=True,blank=True)
    country = models.CharField(max_length=100, null=True,blank=True)
    latitude = models.CharField(max_length=100, null=True,blank=True)
    longitude = models.CharField(max_length=100, null=True,blank=True)
    postal_code = models.CharField(max_length=100, null=True,blank=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.description,self.street,self.suburb)


class RetailStore(models.Model):
    """
    A model to store Retail store information.
    """
    profile = models.ForeignKey(UserProfile, related_name='StoreProfile')
    name = models.CharField(max_length=100)
    location = models.ForeignKey(LocationDetail,null=True,blank=True)
    contact = models.ManyToManyField(ContactDetail, null=True, blank=True)

    def __unicode__(self):
        return self.name


class ProductIngredient(models.Model):
    """
    A model to store product ingredient.
    """
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return self.key


class StoreProduct(models.Model):
    """
    A model to store Store Product information.
    """
    store = models.ForeignKey(RetailStore, related_name='ProductStore')
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    ingredients = models.ManyToManyField(ProductIngredient,null=True,blank=True)
    picture = models.ImageField(null=True,blank=True,upload_to='products_pictures',default='products_pictures/okota-image-unavailable.png')
    featured = models.BooleanField(default=False)
    reviews = models.ManyToManyField('ProductReview',null=True,blank=True)

    def __unicode__(self):
        return '%s by %s' %(self.name,self.store.name)


class ProductReview(models.Model):
    reviewers_name = models.CharField(max_length=100)
    review = models.CharField(max_length=500)
    rating = models.FloatField(default=0)
    stamp = models.DateTimeField(auto_now=True)
    is_moderated = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %s' %(self.rating,self.reviewers_name)


class Testimonial(models.Model):
    reviewers_name = models.CharField(max_length=100)
    review = models.CharField(max_length=500)
    stamp = models.DateTimeField(auto_now=True)
    is_moderated = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' %self.reviewers_name


class DeliveryFee(models.Model):
    """
    A model to store delivery fee information.
    """
    location = models.ForeignKey(LocationDetail)
    store = models.ForeignKey(RetailStore)
    price = models.FloatField(null=True, blank=True)
    eta = models.IntegerField(default=1)
    delivery_type = models.CharField(max_length=100,default='Courier')

    def __unicode__(self):
        return '%s to %s = R%s' % (self.store, self.location.suburb, self.price)


class DeliveryPersonnel(models.Model):
    """
    A model to store delivery personnel information.
    """
    profile = models.OneToOneField(UserProfile)
    delivery_fee = models.ManyToManyField(DeliveryFee,null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.profile.user.username)


class OrderProductAttribute(models.Model):
    """
    A model to store order product attributes.
    """
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return self.key


class OrderProduct(models.Model):
    """
    A model to store order products information.
    """
    product = models.ForeignKey(StoreProduct)
    attributes = models.ManyToManyField(OrderProductAttribute,blank=True,null=True)
    delivery_fee = models.ForeignKey(DeliveryFee,blank=True,null=True)

    def __unicode__(self):
        return '%s' % (self.product)


class OrderTimeSlot(models.Model):
    """
    A model to store order products information.
    """
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.start_time,self.end_time)

class Order(models.Model):
    """
    A model to store order information.
    """
    session = models.CharField(max_length=500,blank=True,null=True)
    products = models.ManyToManyField(OrderProduct,null=True, blank=True)
    delivery_person = models.ForeignKey(DeliveryPersonnel,null=True, blank=True)
    delivery_address = models.ForeignKey(LocationDetail,null=True, blank=True)
    contact_person = models.CharField(max_length=100,null=True, blank=True)
    contact_number = models.ForeignKey(ContactDetail,null=True, blank=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    datetime_stamp = models.DateTimeField(null=True,blank=True)
    payment_method = models.CharField(null=True,blank=True,max_length=100)
    checked_out = models.BooleanField(default=False)
    final_amount = models.FloatField(default=0,null=True,blank=True)
    time_slot = models.ForeignKey(OrderTimeSlot,blank=True,null=True)

    def __unicode__(self):
        return '%s' % (self.status)


class Advert(models.Model):
    title = models.CharField(max_length=100,blank=True,null=True)
    picture = models.ImageField(null=True,blank=True,upload_to='advert_pictures')
    url = models.URLField(null=True,blank=True)


    def __unicode__(self):
        return '%s' % self.title


#===========================================================================
# SIGNALS
#===========================================================================
def signals_import():
    """ A note on signals.

    The signals need to be imported early on so that they get registered
    by the application. Putting the signals here makes sure of this since
    the models package gets imported on the application startup.
    """
    from tastypie.models import create_api_key
 
    models.signals.post_save.connect(create_api_key, sender=User)
 
signals_import()