import xadmin
from .models import UserFav, UserAddress, UserLeavingMessage


class UserFavXAdmin(object):
    list_display = ['user', 'goods', "add_time"]
    search_fields = ['goods']


class UserLeavingXAdmin(object):
    list_display = ['user', 'msg_type', "message", "add_time"]
    search_fields = ['msg_type']


class UserAddressXAdmin(object):
    list_display = ["signer_name", "signer_mobile", "district", "address"]
    search_fields = ['signer_name']


xadmin.site.register(UserFav, UserFavXAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingXAdmin)
xadmin.site.register(UserAddress, UserAddressXAdmin)
