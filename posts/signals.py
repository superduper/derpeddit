from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post
from guardian.shortcuts import assign_perm

@receiver(post_save, sender=Post)
def auto_upvote(sender, instance, created, **kwargs):
    if created:
        instance.submit_vote(instance.owner, positive=True)

@receiver(post_save, sender=Post)
def auto_assign_permission(sender, instance, created, **kwargs):
    """
    automatically grant edit/delete permissions to post owner
    """
    if created:
        assign_perm('change_post', instance.owner, instance)
        assign_perm('delete_post', instance.owner, instance)