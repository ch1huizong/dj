from django.conf import settings
import redis

from .models import Product


r = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


class Recommender(object):

    def get_product_key(self, id):
        return 'product:{}:purchased_with'.format(id)

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(
                        self.get_product_key(product_id),
                        amount=1,
                        value=with_id,
                    )

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(product_ids):
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0,
                -1,
                desc=True
            )[:max_results]
        else:
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)  # 关键这里,link数最多?
            r.zrem(tmp_key, *product_ids)
            suggestions = r.zrange(
                tmp_key,
                0,
                -1,
                desc=True
            )[:max_results]
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id)
        )
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
