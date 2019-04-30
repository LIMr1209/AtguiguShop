from django.views.generic import View
from .models import Goods
# from django.shortcuts import HttpResponse
from django.http import HttpResponse,JsonResponse
import json
from django.core import serializers



class GoodsListView(View):
    def get(self, request):
        """
        通过django 的view 获取商品列表页
        :param request:
        :return:
        """

        goods_list = Goods.objects.all()[:10]
        data = serializers.serialize('json',goods_list)
        data = json.loads(data)
        # json_list = []
        # for good in goods_list:
        #     json_item = {}
        #     json_item['name'] = good.name
        #     json_item['market_price'] = good.market_price
        #     json_item['sold_num'] = good.sold_num
        #     # json_item['add_time'] = str(good.add_time)
        #     json_list.append(json_item)
        # content = json.dumps(json_list)
        # return HttpResponse(data, 'application/json')
        return JsonResponse(data,safe=False)