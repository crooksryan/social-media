from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import json

from .models import User, Post, Following, Like


def index(request):
    if request.method == "POST":
        # figure out the user who hit post
        text = request.POST["post-content"]
        username = request.user.username

        try:
            post = Post.objects.create(content=text, user=username)
            post.save()
        except IntegrityError:
            return render(request, "network/index.html")
        
    posts = Post.objects.all().order_by('-time').values()

    post_pages = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = post_pages.get_page(page_number)

    return render(request, "network/index.html", {"posts": page_obj})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def following(request):
    if request.method == "POST":
        # figure out the user who hit post
        text = request.POST["post-content"]
        username = request.user.username

        try:
            post = Post.objects.create(content=text, user=username)
            post.save()
        except IntegrityError:
            return render(request, "network/index.html")
    
    following = Following.objects.filter(follower=request.user.username).values()

    lst = [request.user.username]

    for person in following:
       lst.append(person['followee']) 

    posts = Post.objects.all().order_by('-time').values()
    
    posts = [i for i in posts if i['user'] in lst or i['user'] == request.user.username]

    post_pages = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = post_pages.get_page(page_number)

    return render(request, "network/following.html", {"posts": page_obj})



def profile(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        # method for following/unfollowing
        try:
            follow_obj = Following.objects.filter(followee=id, follower=request.user.username)
            # following
            if follow_obj.count() == 0:
                follow = Following.objects.create(follower=request.user.username, followee=id)
                follow.save()
            
            # unfollow
            else:
                follow_obj.delete()
        except IntegrityError:
            return HttpResponseRedirect(reverse('index'))
    
    posts = Post.objects.filter(user=id).order_by('-time').values()

    post_page = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = post_page.get_page(page_number)

    follower_count = Following.objects.filter(followee=id).count()

    following_count = Following.objects.filter(follower=id).count()

    is_following = Following.objects.filter(followee=id, follower=request.user.username).count() == 0

    return render(request, "network/profile.html", {"profile": id, "posts": page_obj, 'follower_count': follower_count, 'following_count': following_count, 'is_following': is_following})

def listing(request, option, id):
    if option == 'following':
        lst = Following.objects.filter(follower=id).values()
    elif option == 'followers':
        lst = Following.objects.filter(followee=id).values()
    else:
        # reverse to index
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, 'network/list.html', {"option": option, "users": lst})

def likes(request):
    if request.method == "POST":
        if request.headers.get('X-Requested-With') == "XMLHttpRequest":
            data = json.load(request)
            postID = data['postID']
            
            # add like
            if Like.objects.filter(postID=postID, user=request.user.username).count() == 0:
                like = Like.objects.create(postID=postID, user=request.user.username)
                print('like made')
                like.save()

                
            # unlike
            else:
                like = Like.objects.filter(postID=postID, user=request.user.username).delete()
                print('like removed')

            # get count and update
            count = Like.objects.filter(postID=postID).count()

            # update count and save
            post = Post.objects.get(id=postID)
            post.likes = count
            post.save()

            # return with new number of likes
            return JsonResponse({'likes': count})
        
def edit(request):
    if request.method == "POST":
        if request.headers.get('X-Requested-With') == "XMLHttpRequest":
            data = json.load(request)

            postID = data['postID']
            text = data['text']

            try:
                post = Post.objects.get(id=postID)
                if post.user == request.user.username:
                    post.content = text
                    post.save()
            except IntegrityError:
                return JsonResponse({'fail':0})

            return JsonResponse({'Success': 0})