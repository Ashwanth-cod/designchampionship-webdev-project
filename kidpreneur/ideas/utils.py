from .models import Follow

def are_mutual_followers(user1, user2):
    return Follow.objects.filter(follower=user1, following=user2).exists() and \
           Follow.objects.filter(follower=user2, following=user1).exists()
