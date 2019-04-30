import xadmin
from .models import VerifyCode
from xadmin import views

class GlobalSettings(object):
    site_title = '硅谷商店后台'
    site_footer = 'atguigu_shop'
    menu_style = 'accordion'

class BaseXAdminSettings(object):
    enable_themes = True
    use_bootswath = True


class VerifyCodeXAdmin(object):
    list_display = ['code', 'mobile', "add_time"]


xadmin.site.register(VerifyCode, VerifyCodeXAdmin)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(views.BaseAdminView,BaseXAdminSettings)