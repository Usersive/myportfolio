
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.timezone import now, timedelta
from django.utils.html import format_html


from django.contrib import admin
from .models import Client, Content, File, Profile, Experience, ResubscriptionLog, SentEmail, Service, Skill, About, SocialLinks, Testimonial, UnsubscribedUser,  Subscriber,Introduction
from django.contrib import messages

class FileAdmin(admin.ModelAdmin):
    list_display =['name','file', 'uploaded_at',]
    list_display_links=('name','file',)
    def has_add_permission(self, request):
        return not File.objects.exists()  # Disable "Add" if a file exists

class ProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;">'.format(object.profile_image.url))
    thumbnail.short_description = 'Profile Picture'
    list_display =[ 'thumbnail','full_name','email_add', 'phone', 'freelance',]
    list_display_links=('thumbnail','full_name','email_add',)
    def has_add_permission(self, request):
        return not Profile.objects.exists()  # Disable "Add" if a file exists

class AboutAdmin(admin.ModelAdmin):
    list_display =[ 'about_heading','about',]
    list_display_links=('about_heading','about',)
    def has_add_permission(self, request):
        return not About.objects.exists() 


class IntroductionAdmin(admin.ModelAdmin):
    list_display =[ 'intro_heading','intro',]
    list_display_links=('intro_heading','intro',)
    def has_add_permission(self, request):
        return not Introduction.objects.exists() 

class TestimonialAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;">'.format(object.image.url))
    thumbnail.short_description = 'Image'
    list_display =[ 'thumbnail', 'test_client_name','test_client_profess',]
    list_display_links=( 'thumbnail','test_client_name','test_client_profess',)

class SkillAdmin(admin.ModelAdmin):
    list_display =[ 'skill_heading','skill_percent',]
    list_display_links=('skill_heading','skill_percent',)
    def has_add_permission(self, request):
        return not Skill.objects.exists() 
    
class ServiceAdmin(admin.ModelAdmin):
    list_display =[ 'service_title','service_details',]
    list_display_links=('service_title','service_details',)


class SentEmailAdmin(admin.ModelAdmin):
    list_display =[ 'sender_name','sender_email', 'subject', 'sent_at', ]
    list_display_links=('sender_name','sender_email',)

@admin.action(description="Resubscribe selected users")
def resubscribe_users(modeladmin, request, queryset):
    resubscribed_count = 0

    for unsubscribed_user in queryset:
        if not Subscriber.objects.filter(email=unsubscribed_user.email).exists():
            new_subscriber = Subscriber.objects.create(email=unsubscribed_user.email)
            unsubscribed_user.delete()
            resubscribed_count += 1

            # Log the resubscription
            ResubscriptionLog.objects.create(
                email=new_subscriber.email,
                admin_user=str(request.user)  # Store admin username
            )

            # Send resubscription email
            subject = "You Have Been Resubscribed!"
            html_content = render_to_string("emails/resubscribe_email.html", {})
            text_content = strip_tags(html_content)

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[new_subscriber.email]
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

    messages.success(request, f"{resubscribed_count} users have been resubscribed and notified.")

class ResubscriptionLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'resubscribed_at', 'admin_user')
    ordering = ('-resubscribed_at',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Get recent resubscriptions (last 7 days)
        recent_resubscriptions = ResubscriptionLog.objects.filter(
            resubscribed_at__gte=now() - timedelta(days=7)
        ).order_by('-resubscribed_at')[:5]

        extra_context['recent_resubscriptions'] = recent_resubscriptions
        return super().changelist_view(request, extra_context=extra_context)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)

class UnsubscribedUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'unsubscribed_at')
    actions = [resubscribe_users]  # Add custom action

admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(UnsubscribedUser, UnsubscribedUserAdmin)
admin.site.register(ResubscriptionLog, ResubscriptionLogAdmin)

admin.site.register(File, FileAdmin)
admin.site.register(Client)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Experience)
admin.site.register(Skill, SkillAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(Introduction, IntroductionAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Content)
admin.site.register(SocialLinks) 
admin.site.register(SentEmail, SentEmailAdmin) 