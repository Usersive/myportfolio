import datetime
from django.shortcuts import get_object_or_404, render, redirect
import threading
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from  myapp.forms import EmailForm, SubscriptionForm
from django.http import FileResponse, Http404, HttpResponse
from myapp.models import About, Client, Content, Experience, File, Profile, Service, Skill, SocialLinks, Testimonial, UnsubscribedUser, Subscriber, Introduction
import os
from django.conf import settings
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from myapp.models import SentEmail

def current_year(request):
    year = datetime.now().year
    return render(request, 'index.html', {'current_year': current_year})

def send_email_in_thread(subject, html_message, sender_email, recipient_list):
    # Convert HTML to plain text
    plain_message = strip_tags(html_message)
    thread = threading.Thread(target=send_mail, args=(subject, plain_message, sender_email, recipient_list),
                              kwargs={'html_message': html_message})
    thread.start()



def email_compose(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['sender_name']
            sender_email = form.cleaned_data['sender_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Render HTML email template
            html_message = render_to_string('myapp/email_template.html', {
                'sender_name': sender_name,
                'sender_email': sender_email,
                'subject': subject,
                'message': message
            })

            # Send email in a thread
            send_email_in_thread(subject, html_message, sender_email, ['horenteam@gmail.com'])

            # Save email details to the database
            SentEmail.objects.create(
                sender_name=sender_name,
                sender_email=sender_email,
                subject=subject,
                message=message
            )

            messages.success(request, "Message sent successfully and saved!")
            return redirect('/')
    else:
        form = EmailForm()

    return render(request, 'index.html', {'form': form})



def index(request):
    file_obj = File.objects.first()  # Get the only available file
    client= Client.objects.all()
    form = SubscriptionForm()
    profile = Profile.objects.first() 
    experience = Experience.objects.all()
    skill = Skill.objects.all()
    about = About.objects.first()
    intro = Introduction.objects.first()
    testimonial = Testimonial.objects.all()
    service = Service.objects.all()
    link = SocialLinks.objects.all()
    section = request.GET.get('section', 'ALL')
    if section == 'ALL' or not section:
        contents = Content.objects.all()
    else:
        contents = Content.objects.filter(section=section)
    
    
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscriber.objects.filter(email=email).exists():
                messages.warning(request, "You're already subscribed!")
            else:
                form.save()
                messages.success(request, "Subscription successful!")
            return redirect('index')  # Redirect to clear the form
    context ={
        'form': form,
        'file': file_obj,
        'clients': client,
        'profiles': profile,
        'experiences': experience,
        'skills': skill,
        'abouts': about,
        'introductions':intro,
        'testimonies': testimonial,
        'services': service,
        'contents': contents,
        'links':link,
    }
    return render(request, 'index.html', context)

def download_file(request):
    file_obj = File.objects.first()  # Always fetch the only file
    if not file_obj:
        raise Http404("No file available")

    file_path = os.path.join(settings.MEDIA_ROOT, str(file_obj.file))
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
        return response
    else:
        raise Http404("File not found")





def subscribe_newsletter(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email is in UnsubscribedUser
            if UnsubscribedUser.objects.filter(email=email).exists():
                messages.error(request, "You have previously unsubscribed. Contact support to resubscribe.")
            else:
                subscriber, created = Subscriber.objects.get_or_create(email=email)

                if not created:
                    messages.warning(request, "You're already subscribed!")
                else:
                    messages.success(request, "Subscription successful! A confirmation email has been sent.")

                    # Generate unsubscribe link
                    unsubscribe_url = request.build_absolute_uri(
                        reverse('unsubscribe', args=[subscriber.unsubscribe_token])
                    )

                    # Render email template
                    html_content = render_to_string("myapp/subscription_email.html", {'unsubscribe_link': unsubscribe_url})
                    text_content = strip_tags(html_content)

                    # Send email
                    email_message = EmailMultiAlternatives(
                        subject="Subscription Confirmation",
                        body=text_content,
                        from_email=settings.EMAIL_HOST_USER,
                        to=[email]
                    )
                    email_message.attach_alternative(html_content, "text/html")
                    email_message.send()

            return redirect('index')  # Redirect to prevent resubmission
    else:
        form = SubscriptionForm()

    return render(request, 'index.html', {'form': form})



def unsubscribe(request, token):
    subscriber = Subscriber.objects.filter(unsubscribe_token=token).first()

    if not subscriber:
        messages.error(request, "Invalid or expired unsubscribe link.")
        return redirect('index')  # Redirect to homepage

    email = subscriber.email  # Store email before removing from subscribers list

    # Move user to the UnsubscribedUser table
    UnsubscribedUser.objects.create(email=email, unsubscribed_at=now())

    # Remove from subscribers list
    subscriber.delete()

    # Send Unsubscribe Confirmation Email
    subject = "You Have Unsubscribed"
    html_content = render_to_string("myapp/unsubscribe_email.html", {"email": email})
    text_content = strip_tags(html_content)  # Plain text fallback

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email]
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

    messages.success(request, "You have successfully unsubscribed. A confirmation email has been sent.")
    return redirect('index')

def favicon_view(request):
    """Manually serve favicon.ico"""
    favicon_path = os.path.join(settings.BASE_DIR, 'static/logo/favicon.ico')
    if os.path.exists(favicon_path):
        return FileResponse(open(favicon_path, "rb"), content_type = "image/x-icon")
    return HttpResponse(status=404)