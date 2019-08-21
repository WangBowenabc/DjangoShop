#定义一个索引类
from haystack import indexes
#导入模型类
from Store.models import Goods
#指定对于某个类的某些数据建立索引
#索引类名的格式：模型类名+Index
class GoodsIndex(indexes.SearchIndex,indexes.Indexable):
    #索引字段 use_template=True指定根据表中的那些字段建立索引文件，
    #的说明放在一个文件中
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):#返回模型类
        return Goods
    def index_queryset(self, using=None):
        return self.get_model().objects.all()