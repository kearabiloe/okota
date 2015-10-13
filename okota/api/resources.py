from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from okota.utils import *
from tastypie.authentication import Authentication, ApiKeyAuthentication, BasicAuthentication,MultiAuthentication
from tastypie.authorization import Authorization
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource
from tastypie import fields
from okota.api.exceptions import CustomBadRequest
from okota.models import *
import logging
from django.db.models import Q
logger = logging.getLogger(__name__)




class CreateUserResource(ModelResource):
    user = fields.ForeignKey('okota.api.resources.UserResource', 'user', full=True)

    class Meta:
        allowed_methods = ['post']
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        queryset = UserProfile.objects.all()
        resource_name = 'create_user'
        always_return_data = True

    def hydrate(self, bundle):
        REQUIRED_USER_PROFILE_FIELDS = ["user"]
        for field in REQUIRED_USER_PROFILE_FIELDS:
            if field not in bundle.data:
                raise CustomBadRequest(
                    code="missing_key",
                    message="Must provide {missing_key} when creating a user."
                            .format(missing_key=field))

        REQUIRED_USER_FIELDS = ("email", "raw_password")
        for field in REQUIRED_USER_FIELDS:
            if field not in bundle.data["user"]:
                raise CustomBadRequest(
                    code="missing_key",
                    message="Must provide {missing_key} when creating a user."
                            .format(missing_key=field))
        return bundle

    def obj_create(self, bundle, **kwargs):
        try:
            email = bundle.data["user"]["email"]
            if User.objects.filter(email=email):
                raise CustomBadRequest(
                    code="duplicate_exception",
                    message="That email is already used.")
        except KeyError as missing_key:
            raise CustomBadRequest(
                code="missing_key",
                message="Must provide {missing_key} when creating a user."
                        .format(missing_key=missing_key))
        except User.DoesNotExist:
            pass
        logger.debug(bundle.data)
        raw_password = bundle.data['user']['raw_password']
        if not validate_password(raw_password):
                if len(raw_password) < MINIMUM_PASSWORD_LENGTH:
                    logger.debug("password validation failed: length")
                    raise CustomBadRequest(
                        code="invalid_password",
                        message=(
                            "Your password should contain at least {length} "
                            "characters.".format(length=
                                                 MINIMUM_PASSWORD_LENGTH)))
                logger.debug("password validation failed:incorrect combination")
                raise CustomBadRequest(
                    code="invalid_password",
                    message=("Your password should contain at least one number"
                             ", one uppercase letter, one special character,"
                             " and no spaces."))

        ## Add password to kwargs
        bundle.data["password"] = make_password(raw_password)
        # setting resource_name to `user_profile` here because we want
        # resource_uri in response to be same as UserProfileResource resource
        self._meta.resource_name = UserProfileResource._meta.resource_name
        return super(CreateUserResource, self).obj_create(bundle, **kwargs)


class UserResource(ModelResource):
    # We need to store raw password in a virtual field because hydrate method
    # is called multiple times depending on if it's a POST/PUT/PATCH request
    raw_password = fields.CharField(attribute=None, readonly=True, null=True,
                                    blank=True)

    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(
            ApiKeyAuthentication())
        authorization = Authorization()
        # Because this can be updated nested under the UserProfile, it needed
        # 'put'. No idea why, since patch is supposed to be able to handle
        # partial updates.
        allowed_methods = ['get', 'patch', 'put', ]
        always_return_data = True
        queryset = User.objects.all().select_related("api_key")
        excludes = ['is_active', 'is_staff', 'is_superuser', 'date_joined',
                    'last_login','password']

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id).select_related()

    def hydrate(self, bundle):
        if "raw_password" in bundle.data:
            # Pop out raw_password and validate it
            # This will prevent re-validation because hydrate is called
            # multiple times
            # https://github.com/toastdriven/django-tastypie/issues/603
            # "Cannot resolve keyword 'raw_password' into field." won't occur

            raw_password = bundle.data.pop("raw_password")
            logger.debug("raw password %s" % raw_password)
            # Validate password
            if not validate_password(raw_password):
                logger.debug("password validation failed")
                raise CustomBadRequest(
                    code='invalid_password',
                    message='Your password is invalid.')
            bundle.data["password"] = make_password(raw_password)
        logger.debug("password validation failed NOT RAISED")
        return bundle

    def dehydrate(self, bundle):
        bundle.data['key'] = bundle.obj.api_key.key

        try:
            # Don't return `raw_password` in response.
            del bundle.data["raw_password"]
        except KeyError:
            pass

        return bundle


class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(
            ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get', 'patch', ]
        detail_allowed_methods = ['get', 'patch', 'put']
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user).select_related()

    ## Since there is only one user profile object, call get_detail instead
    def get_list(self, request, **kwargs):
        kwargs["pk"] = request.user.profile.pk
        return super(UserProfileResource, self).get_detail(request, **kwargs)


class StoreProductResource(ModelResource):

    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(
            ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get', 'patch', ]
        detail_allowed_methods = ['get', 'patch', 'put']
        queryset = StoreProduct.objects.all()
        resource_name = 'store_product'

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(store__profile__user=bundle.request.user).select_related()



class ProductResource(ModelResource):

    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(
            ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get' ]
        detail_allowed_methods = ['get']
        queryset = StoreProduct.objects.all()
        resource_name = 'product'


class RetailStoreResource(ModelResource):
    location = fields.ForeignKey('okota.api.resources.LocationDetailResource','location')
    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(
            ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get' ]
        detail_allowed_methods = ['get']
        queryset = RetailStore.objects.all()
        resource_name = 'store'


class DeliveryPersonnelResource(ModelResource):

    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(
            ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get' ]
        detail_allowed_methods = ['get']
        queryset = RetailStore.objects.all()
        resource_name = 'delivery_personnel'

class LocationDetailResource(ModelResource):

    class Meta:
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(
            ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get' ]
        detail_allowed_methods = ['get']
        queryset = LocationDetail.objects.all()
        resource_name = 'location'

