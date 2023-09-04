from django.shortcuts import render, redirect
from .models import TweetModel
from django.contrib.auth.decorators import login_required


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user
        my_tweet = TweetModel()
        my_tweet.author = user
        my_tweet.title = request.POST.get('my-title', '')
        my_tweet.content = request.POST.get('my-content', '')
        my_tweet.save()
        return redirect('/tweet')


@login_required
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
