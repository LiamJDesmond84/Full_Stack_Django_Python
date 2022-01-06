from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

from django.contrib import messages
from .models import User, Post
import bcrypt


def home(request):
    if "userid" not in request.session:
        return redirect("/oops")
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)

def about(request):
    return render(request, "blog/about.html", {"title": "About"})

def register(request):
    return render(request, "blog/register_login.html")

def register_process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/register')

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']

    userEmail = User.objects.filter(email=request.POST['email'])
    if userEmail.exists():
        return redirect("/register")

    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    logged_user = User.objects.create(first_name=f"{first_name}", last_name=f"{last_name}", email=f"{email}", password=pw_hash)
    request.session['userid'] = logged_user.id

    return redirect("blog-home")

def go_login(request):
    return render(request, "blog/login.html")

def login(request):
    errors = User.objects.login(request.POST)
    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/register')
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("blog-home")

    return redirect("blog-home")

def logout(request):
    if "userid" in request.session:
        del request.session['userid']
        return redirect("/register")
    return redirect("/register")

def oops(request):
    return render(request, "blog/oops.html")



def profile(request, id):
    if "userid" not in request.session:
        return redirect("/oops")

    user_id = id
    context = {
            "one_user": User.objects.get(id=user_id),
            "users_posts": User.objects.get(id=user_id).posts.all(),
            "logged_user": request.session['userid']
            }
    print(context)
    return render(request, "blog/profile.html", context)

def view_post(request, id):
    if "userid" not in request.session:
        return redirect("/oops")
    post_id = id

    context = {
            "one_post": Post.objects.get(id=post_id),
            "posts_user": Post.objects.get(id=post_id),
            "logged_user": request.session['userid']
            }
    return render(request, "blog/view_post.html", context)

def new_post(request):
    if "userid" not in request.session:
        return redirect("/oops")
    return render(request, "blog/new_post.html")

def new_post_process(request):
    user_id = request.session['userid']

    title = request.POST["title"]
    content = request.POST["content"]
    Post.objects.create(title=f"{title}", content=f"{content}", user=User.objects.get(id=user_id))

    return redirect("blog-home")

def update_user(request, id):
    if "userid" not in request.session:
        return redirect("/oops")
    user_id = id
    context = {"one_user": User.objects.get(id=user_id)}
    return render(request,"blog/update_user.html", context)

def update_user_process(request, id):
    user_id = id
    image = request.POST["image"]
    update_user = User.objects.get(id=user_id)
    update_user.image = image
    update_user.save()
    return redirect(f"/profile/{user_id}")

def update_post(request, id):
    post_id = id
    context= {"one_post": Post.objects.get(id=post_id)}
    return render(request, "blog/update_post.html", context)

def update_post_process(request, id):
    post_id = id
    title = request.POST["title"]
    content = request.POST["content"]
    post = Post.objects.get(id=post_id)
    post.title = title
    post.content = content
    post.save()
    return redirect(f"/view_post/{post_id}")

def all_users(request):
    context = {"all_users": User.objects.all()}
    return render(request,"blog/all_users.html", context)