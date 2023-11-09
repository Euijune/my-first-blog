import os
import mysite.settings as mysettings
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    '''
    동일한 이름의 파일이 존재할 경우 overwrite
    '''
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(mysettings.MEDIA_ROOT, name))
        return name


def user_directory_path(instance, filename):
    return f'student_image/{instance.title}/study_hard.jpg'

class Post(models.Model):
    models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, storage=OverwriteStorage)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    

# User 정보를 저장하는 Database를 하나 더 만들어야 함
class User(models.Model):
    uid = models.EmailField(max_length=200, blank=False, unique=True)
    pw = models.CharField(max_length=50, blank=False, unique=True)
    group = models.IntegerField(default=0)                  # 0: group이 없는 사람들에게 부여하는 group index
    is_studying_now = models.BooleanField(default=False)    # 순공시간은 이 변수가 True일때 측정시작
    stime_daily = models.IntegerField(default=0)            # 순공시간 기록 (* 매일 초기화 필요, 단위:초)
    stime_weekly = models.IntegerField(default=0)           # 순공시간은 다른 table 만들어서 join하는 방안 탐구(foreign key)
    stime_monthly = models.IntegerField(default=0)
    stime_total = models.IntegerField(default=0)
    #image = models.ImageField(upload_to='intruder_image/%Y/%m/%d/')    # 이미지가 필요할까?