from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, IdeaForm
from .models import Idea

# --------------------------
# Basic Pages
# --------------------------

def index_view(request):
    return render(request, "index.html")

def about_view(request):
    return render(request, "about.html")

def contact_view(request):
    return render(request, "contact.html")

@login_required(login_url='login')
def dashboard_view(request):
    user_ideas = Idea.objects.filter(created_by=request.user)
    total_likes = sum(idea.likes.count() for idea in user_ideas)
    total_comments = sum(idea.comments.count() for idea in user_ideas)
    
    context = {
        'ideas': user_ideas,
        'total_likes': total_likes,
        'total_comments': total_comments,
    }
    return render(request, 'dashboard.html', context)


# --------------------------
# Auth Views
# --------------------------

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in immediately after signup
            return redirect("dashboard")  # adjust as needed
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")  # adjust as needed
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")  # send them back to homepage after logout

# --------------------------
# Idea CRUD
# --------------------------

def idea_list(request):
    ideas = Idea.objects.all().order_by("-created_at")
    return render(request, "ideas/idea_list.html", {"ideas": ideas})


def idea_detail(request, slug):
    idea = get_object_or_404(Idea, slug=slug)
    return render(request, "ideas/idea_detail.html", {"idea": idea})


@login_required
def idea_create(request):
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)  # don't save yet
            idea.created_by = request.user  # assign the logged-in user
            idea.save()  # now save
            return redirect('dashboard')  # or wherever you want
    else:
        form = IdeaForm()
    return render(request, 'idea_create.html', {'form': form})


@login_required
def idea_update(request, slug):
    idea = get_object_or_404(Idea, slug=slug, author=request.user)
    if request.method == "POST":
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Idea updated!")
            return redirect("idea_detail", slug=idea.slug)
    else:
        form = IdeaForm(instance=idea)
    return render(request, "ideas/idea_form.html", {"form": form, "is_edit": True})


@login_required
def idea_delete(request, slug):
    idea = get_object_or_404(Idea, slug=slug, author=request.user)
    if request.method == "POST":
        idea.delete()
        messages.warning(request, "🗑️ Idea deleted.")
        return redirect("dashboard")
    return render(request, "ideas/idea_confirm_delete.html", {"idea": idea})
