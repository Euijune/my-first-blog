from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Post, User
from .forms import PostForm, UserForm
from .serializers import PostSerializer, UserSerializer

from urllib.parse import parse_qsl
from django.http import HttpResponse
import json


class IntruderImage(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def create(self, request):
        serializer = PostSerializer(data=request.data)  # request로부터 데이터form을 만들고
        print(request.data['image'])
        
        if serializer.is_valid():
            try:
                # 유저의 이전 post가 존재하면, 순공시간과 공부 모습을 갱신
                post = Post.objects.get(title=request.data['title']) # 만약 기존 database에 uid가 있다면 (즉, 유저 데이터가 서버에 이미 존재한다면)
                user = User.objects.get(uid=request.data['title'])
                user.stime_daily += 5                                # detect.py는 5초마다 감지 결과를 전송하기 때문
                user.stime_total += 5
                h = user.stime_daily // 3600
                m = (user.stime_daily % 3600) // 60
                s = user.stime_daily % 60
                post.text = f"순공시간: {h}시간 {m}분 {s}초"
                post.image = request.data['image']
                post.save()
                user.save()
            except ObjectDoesNotExist as e:
                # 존재하지 않는다면, post를 새로 만들면됨.
                serializer.save(text="순공시간: 0시간 0분 0초")
                            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST) 

class UserInfo(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    print('post_detail')
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    print('post_new')
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    print('post_edit')
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# 회원가입
def user_signup(request):
    res = {'Signup_valid': False, 'uid': None, 'group': 0}
    
    #user = User.objects.get(uid=request.data['title'])
    if request.method == "POST":
        j = json.loads(request.body)
        signup_uid = j["uid"]
        signup_pw = j['pw']
        try:
            User.objects.create(uid=signup_uid, pw=signup_pw)
            res['Signup_valid'] = True
            res['uid'] = signup_uid
        except:
            pass
        
        
    return HttpResponse(json.dumps(res))
    
# 로그인 (유저 정보 조회)
def user_signin(request):
    print(request)
    res = {'Login_valid': False, 'uid': None, 'group': 0}
    
    if request.method == "POST":
        j = json.loads(request.body)
        req_id = j["uid"]
        req_pw = j['pw']
        
        try:
            matchid = User.objects.get(uid=req_id) # db에 저장된 id
        except:
            matchid = None
        try:
            matchpw = User.objects.get(pw=req_pw)   # db에 저장된 pw
        except:
            matchpw = None
            
        if (matchid is not None and matchpw is not None):
            res['Login_valid'] = True   # 로그인 성공
            res['uid'] = req_id
        else:
            res['Login_valid'] = False  # ID 또는 비밀번호 틀림
            
    return HttpResponse(json.dumps(res))

        