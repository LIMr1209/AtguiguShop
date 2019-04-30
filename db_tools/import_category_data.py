import os
import sys

# 独立使用models

# 得到当前文件的位置和名称
filename_path = os.path.realpath(__file__)
# filename_path = os.path.abspath(__file__)

print("filename_path==", filename_path)
# C:\Users\Administrator\PycharmProjects\AtguiguShop\db_tools\import_category_data.py


# 只要得到目录名称
# dirname = os.path.dirname(filename_path)
dirname = os.getcwd()
print("dirname==", dirname)

sys.path.insert(0,dirname)
print(sys.path)
# 设置独立使用models--从manage.py拷贝过来的
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AtguiguShop.settings")

# 导入django设置
import django

django.setup()

# 这行代码不能卸载前面，一定要写在django.setup()的后面
from goods.models import GoodsCategory

# all_GoodsCategory = GoodsCategory.objects.all()
# print(all_GoodsCategory)

from db_tools.data.category_data import row_data

print(row_data)

# all_GoodsCategory = GoodsCategory.objects.all()
# print(all_GoodsCategory)
# 一级类目的数据
for level1_data in row_data:
    level1_instance = GoodsCategory()
    level1_instance.name = level1_data["name"]
    level1_instance.code = level1_data["code"]
    level1_instance.category_type = 1  # 类别属于一级类目
    # 保存数据
    level1_instance.save()
    # 二级类目的数据
    for level2_data in level1_data["sub_categorys"]:
        level2_instance = GoodsCategory()
        level2_instance.name = level2_data["name"]
        level2_instance.code = level2_data["code"]
        level2_instance.category_type = 2  # 类别属于二级类目
        # 这个不要忘记
        level2_instance.parent_category = level1_instance
        # 保存数据
        level2_instance.save()

        # 三级类目的数据
        for level3_data in level2_data["sub_categorys"]:
            level3_instance = GoodsCategory()
            level3_instance.name = level3_data["name"]
            level3_instance.code = level3_data["code"]
            level3_instance.category_type = 3  # 类别属于三级类目
            # 这个不要忘记
            level3_instance.parent_category = level2_instance
            # 保存数据
            level3_instance.save()
