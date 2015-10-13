from django import template
from okota.models import StoreProduct
import logging

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter(name='get_product_rating')
def get_product_rating(product_id):
    try:
        product = StoreProduct.objects.get(id=int(product_id))
        ratings = product.reviews.all()

        if len(ratings) ==0:
            logger.info("Dividing by zero")
            return 0

        #calculate ratings
        rating_score=0
        for rating in ratings:
            rating_score = rating_score+rating.rating
        rating_score =(rating_score/len(ratings))
        logger.info("rating = %s" % rating_score)
        return rating_score
    except Exception as e:
        logger.warning(e)
        return 0
