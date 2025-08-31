from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Idea, Comment, Like, Subscriber, Report
from .forms import CustomUserCreationForm, IdeaForm, SubscriberForm, UserUpdateForm


User = get_user_model()


@login_required
def search_view(request):
    query = request.GET.get('q', '')
    tab = request.GET.get('tab', 'ideas')
    cat_filter = request.GET.get('cat', None)

    context = {'query': query, 'tab': tab}

    # ----------------------
    # Ideas
    # ----------------------
    ideas = Idea.objects.all()
    if query:
        ideas = ideas.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    if cat_filter:
        ideas = ideas.filter(category=cat_filter)
    context['ideas'] = ideas

    # ----------------------
    # Users
    # ----------------------
    users = User.objects.all()
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    context['users'] = users

    # ----------------------
    # Categories with counts
    # ----------------------
    categories = Idea.objects.values('category').annotate(count=Count('id'))
    context['categories'] = categories  # [{'category': 'other', 'count': 2}, ...]

    return render(request, 'search/INDEX.html', context)

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
@login_required(login_url='login')
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
    return render(request, "dashboard.html", {
        "ideas": ideas,
        "user_form": form,
    })


@login_required
def user_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard')
    return redirect('dashboard')


# --------------------------
# Auth Views
# --------------------------
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.is_student:  # if not student, clear school_name
                user.school_name = ""
            user.save()
            login(request, user)  # auto-login
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm(request)
    return render(request, "auth/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


# --------------------------
# Search View
# --------------------------
@login_required
def search_view(request):
    query = request.GET.get('q', '')
    tab = request.GET.get('tab', 'ideas')
    category_filter = request.GET.get('cat', None)

    context = {'query': query, 'tab': tab}

    # Ideas search
    if tab == 'ideas':
        ideas = Idea.objects.all()
        if query:
            ideas = ideas.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
        if category_filter:
            ideas = ideas.filter(category=category_filter)
        context['ideas'] = ideas

    # Users search
    elif tab == 'users':
        users = User.objects.all()
        if query:
            users = users.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        context['users'] = users

    # Categories search
    elif tab == 'categories':
        categories = Idea.objects.all()
        if query:
            categories = categories.filter(category__icontains=query)
        categories = categories.values('category').annotate(count=Count('id')).order_by('category')
        context['categories'] = categories

    return render(request, 'search/INDEX.html', context)


# --------------------------
# Idea CRUD
# --------------------------
@login_required
def idea_detail(request, slug):
    idea = get_object_or_404(Idea, slug=slug)
    user_liked = Like.objects.filter(idea=idea, user=request.user).exists()
    comments = idea.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if 'like_toggle' in request.POST:
            if user_liked:
                Like.objects.filter(idea=idea, user=request.user).delete()
            else:
                Like.objects.create(idea=idea, user=request.user)
            return redirect('idea_detail', slug=slug)

        elif 'comment_text' in request.POST:
            text = request.POST.get('comment_text', '').strip()
            if text:
                Comment.objects.create(idea=idea, user=request.user, text=text)
            return redirect('idea_detail', slug=slug)

        elif 'report_toggle' in request.POST:
            Report.objects.get_or_create(idea=idea, user=request.user)
            return redirect('idea_detail', slug=slug)

    context = {
        'idea': idea,
        'user_liked': user_liked,
        'comments': comments,
    }
    return render(request, 'ideas/idea_detail.html', context)


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
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber, created = Subscriber.objects.get_or_create(email=form.cleaned_data['email'])
            if created:
                return JsonResponse({'status': 'success', 'message': 'Subscribed successfully!'})
            else:
                return JsonResponse({'status': 'info', 'message': 'You are already subscribed.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid email address.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
