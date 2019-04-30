from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserFav


@receiver(post_save, sender=UserFav)
def save_userfav(sender, instance=None, created=False, **kwargs):
    # 当收藏的时候，收藏数加一
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def del_userfav(sender, instance=None, created=False, **kwargs):
    # 当取消收藏时-1
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
