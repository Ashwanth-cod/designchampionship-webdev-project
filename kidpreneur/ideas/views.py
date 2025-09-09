from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from .utils import get_or_create_conversation
from django.db.models import Count, Q
import json
from .models import Idea, Comment, Like, Follow, CustomUser, Conversation, ForumPost, ForumPostLike
from .forms import CustomUserCreationForm, IdeaForm, UserUpdateForm, LoginForm, ContactForm, MessageForm, ForumPostForm, MessageReportForm

User = get_user_model()

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

@login_required(login_url='/login/')
def search_page(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    
    # Searching Ideas
    ideas = Idea.objects.all()
    if query:
        ideas = ideas.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ideas = ideas.filter(category=category)
    
    # Searching Forum Posts
    forum_posts = ForumPost.objects.all()
    if query:
        forum_posts = forum_posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category:
        forum_posts = forum_posts.filter(category=category)
    
    return render(request, "search/index.html", {
        "ideas": ideas,
        "forum_posts": forum_posts,
        "query": query,
        "selected_category": category,
    })

# API function for handling search queries
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
    
    elif tab == "forum_posts":  # Added a new case for forum posts
        qs = ForumPost.objects.all()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        if category:
            qs = qs.filter(category__iexact=category)
        if sort == "title":
            qs = qs.order_by("-title" if reverse else "title")
        else:
            qs = qs.order_by("-created_at" if reverse else "created_at")
        data = list(qs.values("id", "title", "content", "category", "created_by")[:20])
        for item in data:
            item["author"] = item.pop("created_by__username", "Unknown")
    
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
        idea.num_likes = idea.likes.count()

    theme = "blue"

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
            return redirect('contact')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['email'] = request.user.email
            initial_data['name'] = request.user.get_full_name() or request.user.username
        
        form = ContactForm(initial=initial_data)

    return render(request, 'contact.html', {'form': form})

@login_required(login_url='/login/')
def dashboard_view(request):
    user = request.user

    # --- Ideas ---
    ideas = Idea.objects.filter(created_by=user, is_archived=False)
    starred_ideas = user.starred_ideas.filter(is_archived=False)
    archived_ideas = Idea.objects.filter(created_by=user, is_archived=True)
    total_likes = sum(idea.likes.count() for idea in ideas)

    # --- Followers / Following ---
    # Followers = users who follow me
    followers_qs = user.followers.select_related("follower")
    followers = [f.follower for f in followers_qs]

    # Following = users I follow
    following_qs = user.following.select_related("following")
    following = [f.following for f in following_qs]

    # Mutual followers
    mutual_followers = set(followers) & set(following)

    # Followers info for template
    followers_info = [
        {
            "follower": f.follower,
            "is_mutual": f.follower in mutual_followers,
            "is_following_back": f.follower in following,
        }
        for f in followers_qs
    ]

    # --- Conversations / Messages ---
    conversations = (
        Conversation.objects.filter(Q(user1=user) | Q(user2=user))
        .select_related("user1", "user2")
        .annotate(
            unread_count=Count(
                "messages",
                filter=Q(messages__is_read=False) & ~Q(messages__sender=user),
            )
        )
        .distinct()
    )

    inbox_messages = (
        Message.objects.filter(folder="inbox", conversation__in=conversations)
        .exclude(sender=user)
        .select_related("sender", "conversation")
    )
    sent_messages = Message.objects.filter(folder="sent", sender=user).select_related(
        "sender", "conversation"
    )
    archived_messages = Message.objects.filter(
        folder="archived", conversation__in=conversations
    ).select_related("sender", "conversation")

    conversation_messages = {
        convo.id: convo.messages.select_related("sender").order_by("timestamp")
        for convo in conversations
    }
    unread_counts = {convo.id: convo.unread_count for convo in conversations}

    # Mark unread as read when user views
    for convo in conversations:
        convo.messages.filter(is_read=False).exclude(sender=user).update(is_read=True)

    # --- Forms ---
    profile_update_form = UserUpdateForm(instance=user)
    message_form = MessageForm()
    report_form = MessageReportForm()

    # --- Stats ---
    stats = [
        ("Total Ideas", "bi-lightbulb-fill", len(ideas)),
        ("Starred", "bi-star-fill", len(starred_ideas)),
        ("Archived", "bi-archive-fill", len(archived_ideas)),
        ("Total Likes", "bi-hand-thumbs-up-fill", total_likes),
    ]

    # --- Handle POST ---
    if request.method == "POST":
        if "profile_update_form" in request.POST:
            profile_update_form = UserUpdateForm(request.POST, instance=user)
            if profile_update_form.is_valid():
                profile_update_form.save()
                return redirect("dashboard")

        elif "send_message_form" in request.POST:
            conversation_id = request.POST.get("conversation_id")
            subject = request.POST.get("subject", "").strip()

            if conversation_id:
                conversation = get_object_or_404(Conversation, id=conversation_id)
            else:
                recipient_id = request.POST.get("recipient_id")
                if not recipient_id:
                    messages.error(request, "Recipient is required for a new conversation.")
                    return redirect("dashboard")

                recipient = get_object_or_404(CustomUser, id=recipient_id)
                conversation = get_or_create_conversation(user, recipient)

                if subject:
                    conversation.subject = subject
                    conversation.save()

            if user not in [conversation.user1, conversation.user2]:
                return redirect("dashboard")

            message_form = MessageForm(request.POST, request.FILES)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.sender = user
                message.conversation = conversation
                message.folder = "sent"
                if subject:
                    message.subject_override = subject
                message.save()

                recipient = conversation.user1 if conversation.user2 == user else conversation.user2
                Message.objects.create(
                    conversation=conversation,
                    sender=user,
                    text=message.text,
                    attachment=message.attachment,
                    subject_override=message.subject_override,
                    folder="inbox",
                )
                return redirect("dashboard")

        elif "report_message_form" in request.POST:
            message_id = request.POST.get("message_id")
            message = get_object_or_404(Message, id=message_id)
            if user == message.sender:
                return redirect("dashboard")

            report_form = MessageReportForm(request.POST)
            if report_form.is_valid():
                report = report_form.save(commit=False)
                report.message = message
                report.reported_by = user
                report.save()

                message.is_reported = True
                message.save()
                return redirect("dashboard")

    # --- Context ---
    context = {
        "ideas": ideas,
        "starred_ideas": starred_ideas,
        "archived_ideas": archived_ideas,
        "total_likes": total_likes,
        "followers": followers,  # list of user objects
        "following": following,  # list of user objects
        "followers_info": followers_info,  # enriched info dicts
        "mutual_followers": mutual_followers,
        "profile_update_form": profile_update_form,
        "message_form": message_form,
        "report_form": report_form,
        "conversations": conversations,
        "conversation_messages": conversation_messages,
        "unread_counts": unread_counts,
        "inbox_messages": inbox_messages,
        "sent_messages": sent_messages,
        "archived_messages": archived_messages,
        "stats": stats,
    }

    return render(request, "dashboard.html", context)


@login_required(login_url='/login/')
@csrf_exempt
def save_user_theme(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            theme = data.get("theme")
            if theme and theme.startswith("theme-"):
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
                return JsonResponse({"success": True})
            return redirect("dashboard")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("includes/user_update_form.html", {"form": form}, request=request)
        return JsonResponse({"html": html})

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

@login_required(login_url='/login/')
def idea_detail(request, slug):
    idea = get_object_or_404(Idea, slug=slug)
    print(f"DEBUG: idea.is_archived={idea.is_archived}, creator={idea.created_by.id}, user={request.user.id}")

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


@login_required(login_url='/login/')
def forum_post_create(request):
    if request.method == "POST":
        form = ForumPostForm(request.POST, request.FILES)
        if form.is_valid():
            forum_post = form.save(commit=False)
            forum_post.created_by = request.user
            forum_post.save()
            return redirect('dashboard')
    else:
        form = ForumPostForm()

    return render(request, "forums/forum_create.html", {"form": form})

@login_required(login_url='/login/')
def idea_detail(request, slug):
    idea = get_object_or_404(Idea, slug=slug)
    print(f"DEBUG: idea.is_archived={idea.is_archived}, creator={idea.created_by.id}, user={request.user.id}")

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

@login_required(login_url='/login/')
def forum_post_create(request):
    if request.method == "POST":
        form = ForumPostForm(request.POST, request.FILES)
        if form.is_valid():
            forum_post = form.save(commit=False)
            forum_post.created_by = request.user
            forum_post.save()
            return redirect('dashboard')
    else:
        form = ForumPostForm()

    return render(request, "forums/forum_create.html", {"form": form})

@login_required(login_url='/login/')
def forum_toggle_like(request, slug):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        forum_post = get_object_or_404(ForumPost, slug=slug)

        # Toggle like
        like, created = ForumPostLike.objects.get_or_create(
            forum_post=forum_post,
            user=request.user
        )

        if created:
            liked = True
        else:
            like.delete()
            liked = False

        like_count = forum_post.forum_post_likes.count()

        return JsonResponse({
            "liked": liked,
            "like_count": like_count
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required(login_url='/login/')
def forum_post_detail(request, slug):
    forum_post = get_object_or_404(ForumPost, slug=slug)

    user_liked = ForumPostLike.objects.filter(
        forum_post=forum_post,
        user=request.user
    ).exists()

    like_count = forum_post.forum_post_likes.count()

    return render(request, "forums/forum_details.html", {
        "forum_post": forum_post,
        "user_liked": user_liked,
        "like_count": like_count,
    })

@login_required(login_url='/login/')
def forum_post_detail(request, slug):
    forum_post = get_object_or_404(ForumPost, slug=slug)
    user_liked = ForumPostLike.objects.filter(forum_post=forum_post, user=request.user).exists()
    like_count = forum_post.forum_post_likes.count()
    return render(request, 'forums/forum_details.html', {
        'forum_post': forum_post,
        'user_liked': user_liked,
        'like_count': like_count,
    })

