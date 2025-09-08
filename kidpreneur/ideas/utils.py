from .models import Follow, Conversation

def are_mutual_followers(user1, user2):
    return (
        Follow.objects.filter(follower=user1, following=user2).exists()
        and Follow.objects.filter(follower=user2, following=user1).exists()
    )

def get_or_create_conversation(user1, user2):
    convo = Conversation.objects.filter(
        user1__in=[user1, user2],
        user2__in=[user1, user2]
    ).first()
    if not convo:
        convo = Conversation.objects.create(user1=user1, user2=user2)
    return convo
