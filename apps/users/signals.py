from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

# 信号量 当注册使用的时候加密密码(user创建的时候)

@receiver(post_save,sender=User)
def create_user(sender,instance=None,created=False,**kwargs):
    # 当用户创建的时候 为 True ,instance 就是UserProfile
    if created:
        # print(instance)
        # print(sender)
        password = instance.password
        instance.set_password(password)
        instance.save()




