from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Count, Q
import json
from .models import Idea, Comment, Like, Follow, CustomUser
from .forms import CustomUserCreationForm, IdeaForm, UserUpdateForm, LoginForm, ContactForm

User = get_user_model()

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
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url or "dashboard")
    else:
        form = LoginForm(request)
    return render(request, "auth/login.html", {"form": form, "next": next_url})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect("home")

# --------------------------
# Search
# --------------------------
@login_required(login_url='/login/')
def search_page(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    ideas = Idea.objects.all()
    if query:
        ideas = ideas.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ideas = ideas.filter(category=category)
    return render(request, "search/index.html", {
        "ideas": ideas,
        "query": query,
        "selected_category": category,
    })


@login_required(login_url='/login/')
def search_api(request):
    q = request.GET.get("q", "").strip()
    tab = request.GET.get("tab", "creations")
    sort = request.GET.get("sort", "recent")
    order = request.GET.get("order", "desc")
    category = request.GET.get("category", "").strip()
    reverse = order == "desc"

    if tab == "creations":
        qs = Idea.objects.all().annotate(num_likes=Count("likes"))
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category__iexact=category)
        if sort == "popular":
            qs = qs.order_by("-num_likes" if reverse else "num_likes")
        elif sort == "title":
            qs = qs.order_by("-title" if reverse else "title")
        else:
            qs = qs.order_by("-created_at" if reverse else "created_at")
        data = list(qs.values("id", "slug", "title", "description", "created_by", "num_likes")[:20])
        for item in data:
            item["author"] = item.pop("author__username", "Unknown")
            item["likes"] = item.pop("num_likes", 0)
    elif tab == "users":
        qs = User.objects.all()
        if q:
            qs = qs.filter(username__icontains=q)
        if sort == "name":
            qs = qs.order_by("-username" if reverse else "username")
        else:
            qs = qs.order_by("-date_joined" if reverse else "date_joined")
        data = list(qs.values("username", "first_name", "last_name", "email")[:20])
    elif tab == "categories":
        qs = Idea.objects.all()
        if q:
            qs = qs.filter(category__icontains=q)
        qs = qs.values("category").annotate(count=Count("id"))
        if sort == "alpha":
            qs = qs.order_by("-category" if reverse else "category")
        else:
            qs = qs.order_by("-count" if reverse else "count")
        data = list(qs)
    else:
        data = []
    return JsonResponse(data, safe=False)

# --------------------------
# Basic Pages
# --------------------------
def index_view(request):
    top_ideas = list(
        Idea.objects.annotate(num_likes=Count("likes"))
        .order_by("-num_likes")[:3]
    )

    top_idea_ids = [idea.id for idea in top_ideas]

    liked_idea_ids = set()
    if request.user.is_authenticated:
        liked_idea_ids = set(
            Like.objects.filter(user=request.user, idea_id__in=top_idea_ids)
            .values_list("idea_id", flat=True)
        )

    for idea in top_ideas:
        idea.user_liked = idea.id in liked_idea_ids
        idea.num_likes = idea.likes.count()  # Use num_likes directly

    # Example: Set default or user-defined theme
    theme = "blue"  # Or fetch from user preferences

    return render(request, "index.html", {
        "top_ideas": top_ideas,
        "theme": theme,
    })

def theme_view(request):
    theme = "blue"
    top_ideas = Idea.objects.order_by('-num_likes')[:3]
    
    context = {
        "theme": theme,
        "top_ideas": top_ideas,
    }
    return render(request, "your_template.html", context)

def about_view(request):
    return render(request, "about.html")
    
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been successfully sent!')
            return redirect('contact')
        else:
            messages.error(request, 'There was an error with your submission.')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['email'] = request.user.email
            initial_data['name'] = request.user.get_full_name() or request.user.username
        
        form = ContactForm(initial=initial_data)

    return render(request, 'contact.html', {'form': form})


# --------------------------
# Dashboard & Profile
# --------------------------
@login_required(login_url='/login/')
def dashboard_view(request):
    user = request.user
    print((user))
    ideas = Idea.objects.filter(created_by=user, is_archived=False)
    starred_ideas = user.starred_ideas.filter(is_archived=False)
    archived_ideas = Idea.objects.filter(created_by=user, is_archived=True)

    total_likes = sum(idea.likes.count() for idea in ideas)

    # Get followers and following
    followers = [f.follower for f in user.followers.select_related('follower').all()]
    following = [f.following for f in user.following.select_related('following').all()]

    theme_colors = ["yellow", "blue", "green", "pink", "purple", "orange", "danger"]

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or use your dashboard URL name
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'ideas': ideas,
        'starred_ideas': starred_ideas,
        'archived_ideas': archived_ideas,
        'total_likes': total_likes,
        'theme_colors': theme_colors,
        'followers': followers,
        'following': following,
        'profile_update_form': form,  # pass form here
    }

    return render(request, 'dashboard.html', context)   

@login_required(login_url='/login/')
@csrf_exempt
def save_user_theme(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            theme = data.get("theme")
            if theme and theme.startswith("theme-"):
                # Save to user profile or wherever you keep preferences
                profile = request.user.profile
                profile.theme_preference = theme
                profile.save()
                return JsonResponse({"status": "success"})
            return JsonResponse({"error": "Invalid theme"}, status=400)
        except Exception:
            return JsonResponse({"error": "Invalid request"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

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
    elif action == "unarchive":
        idea.is_archived = False
    elif action == "delete":
        idea.delete()
        return JsonResponse({"success": "Idea deleted."})
    else:
        return JsonResponse({"error": "Unknown action."}, status=400)

    idea.save()
    return JsonResponse({"success": f"Idea {action}d."})

@require_POST
@login_required(login_url='/login/')
def idea_action(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)

    action = data.get("action")
    idea_id = data.get("idea_id")
    user = request.user

    if not action or not idea_id:
        return JsonResponse({"error": "Missing action or idea ID."}, status=400)

    try:
        idea = Idea.objects.get(id=idea_id, created_by=user)
    except Idea.DoesNotExist:
        return JsonResponse({"error": "Idea not found or not authorized."}, status=404)

    if action == "archive":
        idea.is_archived = True
    elif action == "unarchive":
        idea.is_archived = False
    elif action == "delete":
        idea.delete()
        return JsonResponse({"success": "Idea deleted."})
    else:
        return JsonResponse({"error": "Invalid action."}, status=400)

    idea.save()
    return JsonResponse({"success": f"Idea {action}d."})


@login_required(login_url='/login/')
def user_update(request):
    user = request.user
    form = UserUpdateForm(request.POST or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                # Respond with success JSON for AJAX
                return JsonResponse({"success": True})
            # Normal POST redirect fallback
            return redirect("dashboard")

    # Serve form partial for AJAX GET request
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("includes/user_update_form.html", {"form": form}, request=request)
        return JsonResponse({"html": html})

    # Fallback redirect for non-AJAX GET (you can change as needed)
    return redirect("dashboard")

@login_required(login_url='/login/')
def profile_view(request, username):
    user_obj = get_object_or_404(CustomUser, username=username)
    is_following = Follow.objects.filter(follower=request.user, following=user_obj).exists()
    followers = user_obj.followers.all()
    following = user_obj.following.all()
    stats = {
        "total_ideas": user_obj.ideas.count(),
        "total_likes": sum(i.likes.count() for i in user_obj.ideas.all()),
        "unique_categories": user_obj.ideas.values("category").distinct().count(),
        "followers_count": followers.count(),
        "following_count": following.count(),
    }
    return render(request, "profile.html", {
        "user_obj": user_obj,
        "is_following": is_following,
        "stats": stats,
        "ideas": user_obj.ideas.all(),
        "followers": followers,
        "following": following,
    })


@login_required(login_url='/login/')
def toggle_follow(request, username):
    try:
        target = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    if target == request.user:
        return JsonResponse({"error": "You cannot follow yourself"}, status=400)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
        return JsonResponse({"status": "unfollowed"})
    return JsonResponse({"status": "followed"})

# --------------------------
# Idea Views
# --------------------------
@login_required(login_url='/login/')
def idea_detail(request, slug):
    idea = get_object_or_404(Idea, slug=slug)
    print(f"DEBUG: idea.is_archived={idea.is_archived}, creator={idea.created_by.id}, user={request.user.id}")

    # 🔒 Check if idea is archived and user is NOT the creator
    if idea.is_archived:
        return redirect("archived_idea")

    user_liked = Like.objects.filter(idea=idea, user=request.user).exists()

    if request.method == "POST":
        if "like_toggle" in request.POST:
            if user_liked:
                Like.objects.filter(idea=idea, user=request.user).delete()
            else:
                Like.objects.create(idea=idea, user=request.user)
            return redirect("idea-detail", slug=slug)

        if "comment_text" in request.POST:
            text = request.POST.get("comment_text", "").strip()
            if text:
                Comment.objects.create(idea=idea, user=request.user, text=text)
            return redirect("idea-detail", slug=slug)

    comments = idea.comments.all().order_by("-created_at")
    like_count = idea.likes.count()

    return render(request, "ideas/idea_detail.html", {
        "idea": idea,
        "user_liked": user_liked,
        "comments": comments,
        "like_count": like_count,
    })

def idea_list(request):
    ideas = Idea.objects.annotate(like_count=Count("likes"))
    return render(request, "ideas/list.html", {"ideas": ideas})

@login_required(login_url='/login/')
def archived_idea(request):
    return render(request, "ideas/archived_notice.html")

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
        like_count = idea.likes.count()
        return JsonResponse({"liked": liked, "like_count": like_count})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required(login_url='/login/')
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
        form = IdeaForm(request.POST, request.FILES)
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
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
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
