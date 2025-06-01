from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from projects.models import TeamMember

@receiver(post_save, sender=CustomUser)
def create_team_member(sender, instance, created, **kwargs):
    if created and instance.role in ['staff', 'manager']:
        TeamMember.objects.get_or_create(
            user=instance,
            defaults={
                'full_name': instance.get_full_name() or instance.username,
                'role': instance.get_role_display()
            }
        )
