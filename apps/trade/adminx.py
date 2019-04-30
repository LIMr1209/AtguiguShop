import xadmin
from .models import ShopingCart, OrderInfo, OrderGoods

class ShopingCartXAdmin(object):
    list_display = ["user","goods","nums"]
    search_fields = ['goods']

class OrderInfoXAdmin(object):
    list_display = ['user','order_sn','trade_no','pay_status','post_script','order_mount','pay_time','signer_name','signer_mobile','address']
    search_fields = ['order_sn','trade_no']

class OrderGoodsXAdmin(object):
    list_display = ['order','goods','good_nums','add_time']
    search_fields = ['goods','order']

xadmin.site.register(ShopingCart,ShopingCartXAdmin)
xadmin.site.register(OrderInfo,OrderInfoXAdmin)
xadmin.site.register(OrderGoods,OrderGoodsXAdmin)

