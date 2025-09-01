from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Idea, Comment, Like, Subscriber, Report
from django.db.models import Count, Sum
from .forms import CustomUserCreationForm, IdeaForm, SubscriberForm, UserUpdateForm

User = get_user_model()

# --------------------------
# Search
# --------------------------
@login_required
def search_page(request):
    return render(request, "search/index.html")


@login_required
def search_api(request):
    q = request.GET.get("q", "").strip()
    tab = request.GET.get("tab", "ideas")

    if tab == "ideas":
        qs = Idea.objects.all()
        if q:
            qs = qs.filter(title__icontains=q)
        qs = qs[:20]
        data = list(qs.values("title", "slug", "category", "description", "likes"))

    elif tab == "users":
        qs = User.objects.all()
        if q:
            qs = qs.filter(username__icontains=q)
        qs = qs[:20]
        data = list(qs.values("username", "first_name", "last_name", "email"))

    elif tab == "categories":
        qs = Idea.objects.all()
        if q:
            qs = qs.filter(category__icontains=q)
        qs = qs.values("category").annotate(count=Count("id")).order_by("-count")
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
@login_required(login_url="login")
def dashboard_view(request):
    if request.method == "POST" and "profile_update" in request.POST:
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect("dashboard")
    else:
        form = UserUpdateForm(instance=request.user)

    ideas = Idea.objects.filter(created_by=request.user)
    return render(
        request,
        "dashboard.html",
        {"ideas": ideas, "user_form": form},
    )


@login_required
def user_update(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
        return redirect("dashboard")
    return redirect("dashboard")


@login_required
def user_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    ideas = getattr(user_obj, "ideas", None).all() if hasattr(user_obj, "ideas") else []

    stats = {
        "total_ideas": ideas.count(),
        "total_likes": ideas.aggregate(total=Sum("likes"))["total"] or 0,
        "unique_categories": ideas.values("category").distinct().count(),
    }

    return render(request, "profile.html", {
        "user_obj": user_obj,
        "ideas": ideas,
        "stats": stats,
    })


# --------------------------
# Auth Views
# --------------------------

def signup_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")  # capture ?next=...
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.is_student:
                user.school_name = ""
            user.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect(next_url or "dashboard")  # use next if available
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/signup.html", {"form": form, "next": next_url})


def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")  # capture ?next=...
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url or "dashboard")  # use next if available
    else:
        form = AuthenticationForm(request)
    return render(request, "auth/login.html", {"form": form, "next": next_url})

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


# --------------------------
# Idea CRUD + AJAX Like Toggle
# --------------------------
@login_required
def idea_detail(request, slug):
    idea = get_object_or_404(Idea, slug=slug)
    user_liked = Like.objects.filter(idea=idea, user=request.user).exists()
    comments = idea.comments.all().order_by("-created_at")

    context = {
        "idea": idea,
        "user_liked": user_liked,
        "comments": comments,
        "like_count": Like.objects.filter(idea=idea).count(),
    }
    return render(request, "ideas/idea_detail.html", context)


@login_required
def toggle_like(request, slug):
    """AJAX endpoint for toggling like/unlike."""
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        idea = get_object_or_404(Idea, slug=slug)
        like, created = Like.objects.get_or_create(idea=idea, user=request.user)
        if not created:  # already liked -> unlike
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({
            "liked": liked,
            "like_count": Like.objects.filter(idea=idea).count(),
        })
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def idea_create(request):
    if request.method == "POST":
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.created_by = request.user
            idea.save()
            messages.success(request, "💡 Idea created successfully!")
            return redirect("dashboard")
    else:
        form = IdeaForm()
    return render(request, "ideas/idea_form.html", {"form": form})


@login_required
def idea_update(request, slug):
    idea = get_object_or_404(Idea, slug=slug, created_by=request.user)
    if request.method == "POST":
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            updated_idea = form.save(commit=False)
            updated_idea.created_by = request.user
            updated_idea.save()
            messages.success(request, "✏️ Idea updated successfully!")
            return redirect("dashboard")
    else:
        form = IdeaForm(instance=idea)
    return render(request, "ideas/idea_form.html", {"form": form})


@login_required
def idea_delete(request, slug):
    idea = get_object_or_404(Idea, slug=slug, created_by=request.user)
    if request.method == "POST":
        idea.delete()
        messages.warning(request, "🗑️ Idea deleted.")
        return redirect("dashboard")
    return render(request, "ideas/idea_confirm_delete.html", {"idea": idea})


# --------------------------
# Newsletter AJAX
# --------------------------
def subscribe_newsletter(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber, created = Subscriber.objects.get_or_create(email=form.cleaned_data["email"])
            if created:
                return JsonResponse({"status": "success", "message": "Subscribed successfully!"})
            else:
                return JsonResponse({"status": "info", "message": "You are already subscribed."})
        else:
            return JsonResponse({"status": "error", "message": "Invalid email address."})
    return JsonResponse({"status": "error", "message": "Invalid request."})
