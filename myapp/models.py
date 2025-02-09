from django.db import models
from django.utils.timezone import now
import uuid
from django.db import models


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if File.objects.exists() and not self.pk:
            raise ValueError("Only one file entry is allowed. Edit the existing one.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    STATUS =(
        ('Availabe', 'Available'),
        ('Not Available', 'Not Available')
    )
    full_name = models.CharField(max_length=250)
    profile_image = models.ImageField(upload_to='profile/')
    profes= models.CharField(max_length=100)
    experience = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email_add = models.EmailField()
    address = models.CharField(max_length=200)
    freelance = models.CharField(max_length=100, choices=STATUS)
    
    def __str__(self):
        return self.full_name

class Client(models.Model):
    numbers = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    details = models.CharField(max_length=100)
    
    def __str__(self):
        return f" {self.numbers} - {self.description}"
    
class Experience(models.Model):
    title = models.CharField(max_length=100)
    short_title = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    details = models.TextField()
    
    
    def __str__(self):
        return self.title

class Skill(models.Model):
    STATUS =(
        ('bg-info', 'bg-info'),
        ('bg-success', 'bg-success'),
        ('bg-warning', 'bg-warning'),
        ('bg-danger', 'bg-danger'),
    )
    skill_heading = models.CharField(max_length=100)
    skill_percent = models.CharField(max_length=10)
    skill_color = models.CharField(max_length=20, choices=STATUS)
    
    def __str__(self):
        return self.skill_heading

class About(models.Model):
    about_heading = models.CharField(max_length=50)
    about = models.TextField()
    
    def __str__(self):
        return self.about

class Introduction(models.Model):
    intro_heading = models.CharField(max_length=50)
    intro = models.TextField()
    
    def __str__(self):
        return self.intro

class Testimonial(models.Model):
    test_details = models.TextField()
    test_client_name = models.CharField(max_length=50)
    test_client_profess = models.CharField(max_length=50)
    image = models.ImageField(upload_to='testimoniels/')
    
    def __str__(self):
        return self.test_client_name

class Service(models.Model):
    service_title = models.CharField(max_length=100)
    service_details = models.CharField(max_length=250)
    service_fontawesome = models.CharField(max_length=50)
    
    def __str__(self):
        return self.service_title

class Content(models.Model):
    SELECTION_CHOICE =(
        ('Programming', 'Programming'),
        ('Development', 'Development'),
        ('GraphicDesign', 'GraphicDesign'),
    )
    details = models.CharField(max_length=250)
    section = models.CharField(max_length=50, choices=SELECTION_CHOICE)
    image = models.ImageField(upload_to='project/images/')
    
    def __str__(self):
        return self.section

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, unique=True)  # Unique token for unsubscribing

    def __str__(self):
        return self.email

class UnsubscribedUser(models.Model):
    email = models.EmailField(unique=True)
    unsubscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ResubscriptionLog(models.Model):
    email = models.EmailField()
    resubscribed_at = models.DateTimeField(default=now)
    admin_user = models.CharField(max_length=100)  # Store the admin who performed the action

    def __str__(self):
        return f"{self.email} - {self.resubscribed_at}"

class SocialLinks(models.Model):
    SELECT=(
        ('fab fa-github', 'fab fa-github'),
        ('fab fa-instagram', 'fab fa-instagram'),
        ('fab fa-linkedin-in', 'fab fa-linkedin-in'),
        ('fab fa-facebook-f', 'fab fa-facebook-f'),
        ('fab fa-twitter','fab fa-twitter',)
    )
    link = models.CharField(max_length=50, choices=SELECT)
    link_address= models.CharField(max_length=250)
    
    def __str__(self):
        return self.link

class SentEmail(models.Model):
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)  # Timestamp when saved

    def __str__(self):
        return f"{self.subject} from {self.sender_name}"