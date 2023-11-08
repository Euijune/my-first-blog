'''
models 객체와 querysets 같은 복잡한 데이터를 JSON, XML과 같은 native 데이터로
바꿔주는 역할
'''

from blog.models import Post, User
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text', 'created_date', 'published_date', 'image')     # blog/models.py의 속성과 동일하게
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'pw', 'group', 'is_studying_now', 'stime_daily', 'stime_weekly', 'stime_monthly', 'stime_total')