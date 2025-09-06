from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Idea, Comment, Like, Follow, CustomUser
from .forms import CustomUserCreationForm, IdeaForm, UserUpdateForm

User = get_user_model()

# --------------------------
# Search
# --------------------------

@login_required(login_url='/login/')
def search_page(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")

    ideas = Idea.objects.all()

    if query:
        ideas = ideas.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if category:
        ideas = ideas.filter(category=category)

    context = {
        "ideas": ideas,
        "query": query,
        "selected_category": category,
    }
    return render(request, "search/index.html", context)

@login_required(login_url='/login/')
def search_api(request):
    q = request.GET.get("q", "").strip()
    tab = request.GET.get("tab", "creations")  # Default 'creations'
    sort = request.GET.get("sort", "recent")
    order = request.GET.get("order", "desc")
    category = request.GET.get("category", "").strip()

    reverse = order == "desc"

    if tab == "creations":
        # Annotate count as 'num_likes' instead of 'likes'
        qs = Idea.objects.all().annotate(num_likes=Count("likes"))

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

        if category:
            qs = qs.filter(category__iexact=category)

        # Sorting logic
        if sort == "popular":
            qs = qs.order_by("-num_likes" if reverse else "num_likes")
        elif sort == "title":
            qs = qs.order_by("-title" if reverse else "title")
        else:  # recent
            qs = qs.order_by("-created_at" if reverse else "created_at")

        data = list(
            qs.values(
                "id",
                "slug",
                "title",
                "description",
                "created_by",
                "num_likes"
            )[:20]
        )

        # Rename keys for frontend consistency
        for item in data:
            item["author"] = item.pop("author__username", "Unknown")
            item["likes"] = item.pop("num_likes", 0)

    elif tab == "users":
        qs = User.objects.all()
        if q:
            qs = qs.filter(username__icontains=q)

        if sort == "name":
            qs = qs.order_by("-username" if reverse else "username")
        else:  # recent
            qs = qs.order_by("-date_joined" if reverse else "date_joined")

        data = list(qs.values("username", "first_name", "last_name", "email")[:20])

    elif tab == "categories":
        qs = Idea.objects.all()
        if q:
            qs = qs.filter(category__icontains=q)

        qs = qs.values("category").annotate(count=Count("id"))

        if sort == "alpha":
            qs = qs.order_by("-category" if reverse else "category")
        else:  # count
            qs = qs.order_by("-count" if reverse else "count")

        data = list(qs)

    else:
        data = []

    return JsonResponse(data, safe=False)

# --------------------------
# Basic Pages
# --------------------------
def index_view(request):
    return render(request, "index.html")


def about_view(request):
    return render(request, "about.html")


def contact_view(request):
    return render(request, "contact.html")


def basetest_view(request):
    return render(request, "contact.html")


# --------------------------
# Dashboard & Profile
# --------------------------
@login_required(login_url='/login/')
def dashboard_view(request):
    ideas = Idea.objects.filter(created_by=request.user)
    starred_ideas = request.user.starred_ideas.all()  # ManyToMany reverse

    user_form = UserUpdateForm(instance=request.user)

    if request.method == "POST" and "profile_update" in request.POST:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect("dashboard")

    return render(request, "dashboard.html", {
        "ideas": ideas,
        "starred_ideas": starred_ideas,
        "user_form": user_form,
    })

@require_POST
@login_required(login_url='/login/')
def confirm_action(request):
    action = request.POST.get("action")
    idea_id = request.POST.get("idea_id")
    password = request.POST.get("password")

    user = request.user
    idea = Idea.objects.filter(id=idea_id, created_by=user).first()

    if not idea:
        return JsonResponse({"error": "Idea not found."}, status=404)

    if not authenticate(username=user.username, password=password):
        return JsonResponse({"error": "Invalid password."}, status=403)

    if action == "archive":
        idea.is_archived = True
        idea.save()
        return JsonResponse({"success": "Idea archived."})

    elif action == "unarchive":
        idea.is_archived = False
        idea.save()
        return JsonResponse({"success": "Idea unarchived."})

    elif action == "delete":
        idea.delete()
        return JsonResponse({"success": "Idea deleted."})

    return JsonResponse({"error": "Invalid action."}, status=400)

@login_required(login_url='/login/')
def user_update(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect("dashboard")
    return redirect("dashboard")

@login_required(login_url='/login/')
def profile_view(request, username):
    user_obj = get_object_or_404(CustomUser, username=username)

    # compute follow status here
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user_obj
        ).exists()

    stats = {
        "total_ideas": user_obj.ideas.count(),
        "total_likes": sum(i.likes.count() for i in user_obj.ideas.all()),
        "unique_categories": user_obj.ideas.values("category").distinct().count(),
    }

    return render(request, "profile.html", {
        "user_obj": user_obj,
        "is_following": is_following,
        "stats": stats,
        "ideas": user_obj.ideas.all(),
    })

@login_required(login_url='/login/')
def toggle_follow(request, username):
    try:
        target = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    if target == request.user:
        return JsonResponse({"error": "You cannot follow yourself"}, status=400)

    follow, created = Follow.objects.get_or_create(
        follower=request.user, following=target
    )

    if not created:
        # already following → unfollow
        follow.delete()
        return JsonResponse({"status": "unfollowed"})
    else:
        return JsonResponse({"status": "followed"})


# --------------------------
# Auth Views
# --------------------------
def signup_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.is_student:
                user.school_name = ""
            user.save()
            login(request, user)
            return redirect(next_url or "dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/signup.html", {"form": form, "next": next_url})


def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url or "dashboard")
    else:
        form = AuthenticationForm(request)
    return render(request, "auth/login.html", {"form": form, "next": next_url})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect("home")


# --------------------------
# Idea CRUD + Like Toggle
# --------------------------
@login_required(login_url='/login/')
def idea_detail(request, slug):
    idea = get_object_or_404(Idea, slug=slug)
    user_liked = Like.objects.filter(idea=idea, user=request.user).exists()

    if request.method == "POST":
        if "like_toggle" in request.POST:
            if user_liked:
                Like.objects.filter(idea=idea, user=request.user).delete()
            else:
                Like.objects.create(idea=idea, user=request.user)
            return redirect("idea-detail", slug=slug)

        if "comment_text" in request.POST:
            text = request.POST.get("comment_text")
            if text.strip():
                Comment.objects.create(idea=idea, user=request.user, text=text)
            return redirect("idea-detail", slug=slug)

    comments = idea.comments.all().order_by("-created_at")
    like_count = Like.objects.filter(idea=idea).count()

    context = {
        "idea": idea,
        "user_liked": user_liked,
        "comments": comments,
        "like_count": like_count,
    }
    return render(request, "ideas/idea_detail.html", context)


def idea_list(request):
    ideas = Idea.objects.annotate(like_count=Count("likes"))
    return render(request, "ideas/list.html", {"ideas": ideas})


@login_required(login_url='/login/')
def toggle_like(request, slug):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        idea = get_object_or_404(Idea, slug=slug)
        like, created = Like.objects.get_or_create(idea=idea, user=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        like_count = Like.objects.filter(idea=idea).count()
        return JsonResponse({"liked": liked, "like_count": like_count})

    return JsonResponse({"error": "Invalid request"}, status=400)

def toggle_star(request, slug):
    idea = get_object_or_404(Idea, slug=slug)
    if request.user in idea.starred_by.all():
        idea.starred_by.remove(request.user)
    else:
        idea.starred_by.add(request.user)
    return redirect("idea-detail", slug=slug)

@login_required(login_url='/login/')
def idea_create(request):
    if request.method == "POST":
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.created_by = request.user
            idea.save()
            return redirect("dashboard")
    else:
        form = IdeaForm()
    return render(request, "ideas/idea_form.html", {"form": form})


@login_required(login_url='/login/')
def idea_update(request, slug):
    idea = get_object_or_404(Idea, slug=slug, created_by=request.user)
    if request.method == "POST":
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            updated_idea = form.save(commit=False)
            updated_idea.created_by = request.user
            updated_idea.save()
            return redirect("dashboard")
    else:
        form = IdeaForm(instance=idea)
    return render(request, "ideas/idea_form.html", {"form": form})


@login_required(login_url='/login/')
def idea_delete(request, slug):
    idea = get_object_or_404(Idea, slug=slug, created_by=request.user)
    if request.method == "POST":
        idea.delete()
        return redirect("dashboard")
    return render(request, "ideas/idea_confirm_delete.html", {"idea": idea})
