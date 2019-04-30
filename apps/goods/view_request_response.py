from .models import Goods
from .serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class GoodsListViewRequestResponse(APIView):
    def get(self,request,format=None):
        print('request.data==>',request.data) #{}  返回请求正文的解析内容
        print('request.user==>',request.user) # AnonymousUser 得到请求登录用户名
        print('request.method==>',request.method) #get 请求的方法
        print('request.auth==>',request.auth)  #None
        print('request.content_type==>',request.content_type) #text/plain
        print('request.query_params==>',request.query_params)  # <QueryDict: {}>
        print('request.parsers==>',request.parsers)
        #[<rest_framework.parsers.JSONParser object at 0x00000190ACE84E80>, <rest_framework.parsers.FormParser object at 0x00000190ACE84EB8>, <rest_framework.parsers.MultiPartParser object at 0x00000190ACE84EF0>]
        goods = Goods.objects.all()[:10]  # 取前10条数据
        good_serializer = GoodsSerializer(goods,many=True)
        response = Response(data=good_serializer.data)
        print('response.data==>',response.data) #返回的数据
        print('response.status_code==>',response.status_code)  #HTTP响应的数字状态代码
        print('response.template_name==>',response.template_name)  #none
        print('response.content_type==>',response.content_type) #none
        # print('response.content==>',response.content.render())  响应的呈现内容
        return response
