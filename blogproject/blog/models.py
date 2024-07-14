from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# Create Profile, Auth User is used and extra things are specified in profile

class Profile(models.Model):
    USER_ROLE = (
        ('reader','Reader'),
        ('author','Author'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    user_type = models.CharField(max_length=10, choices=USER_ROLE)
    
    def __str__(self):
        return f'{self.user}-{self.user_type}'
    
class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    published = models.BooleanField(default=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    upadted_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.title}-{self.author}'