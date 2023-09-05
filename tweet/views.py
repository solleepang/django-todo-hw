from django.shortcuts import render, redirect
from .models import TweetModel
from django.contrib.auth.decorators import login_required


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


def create_tweet(request):
    if request.method == 'GET':
        # 로그인 확인
        user = request.user.is_authenticated
        if user:
            # 로그인됨: 모든 할 일 가져와서 보여주기
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            # 로그인 안 됨:
            return redirect('/sign-in')

    elif request.method == 'POST':
        # 새 할 일 생성
        user = request.user
        my_tweet = TweetModel()
        my_tweet.author = user
        my_tweet.title = request.POST.get('my-title', '')
        my_tweet.content = request.POST.get('my-content', '')
        my_tweet.save()
        return redirect('/tweet')


@login_required # 로그인 한 사람만 접근 가능
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


def detail_tweet(request, id):
    if request.method == 'GET':
        my_tweet = TweetModel.objects.get(id=id)
        return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet})


def my_tweet(request, id):
    if request.method == 'GET':
        my_tweet = TweetModel.objects.filter(author_id=id).order_by('-created_at')
        return render(request, 'tweet/tweet_my.html', {'tweet': my_tweet})
    else:
        return redirect('/')


def update_tweet(request, id):
    tweet = TweetModel.objects.get(id=id)
    if request.method == 'GET':
        # 개별 페이지에서 수정 버튼 클릭시 수정 가능한 페이지로 이동
        return render(request,'tweet/tweet_update.html', {'tweet': tweet})

    elif request.method == 'POST':
        # 수정 후 수정하기 버튼 클릭시 내용 저장하고 개별페이지로 이동
        tweet.title = request.POST['my-title']
        tweet.content = request.POST['my-content']
        tweet.save()
        return redirect(f'/tweet/{id}')
