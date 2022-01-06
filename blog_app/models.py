from django.db import models
from django.utils import timezone
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Last Name should be at least 1 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether email matches regex matches the pattern
            errors['email'] = "Invalid email address!"

        if len(postData['password']) < 5:
            errors["password"] = "Password should be at least 5 characters"
        if postData["password"] != postData["confpassword"]:
            errors["password"] = "Passwords must match!"
        return errors
        
    def login(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether email matches regex pattern
            errors['email'] = "Invalid email address!"

        if len(postData['password']) < 5:
            errors["password"] = "Password should be at least 5 characters"
        return errors
    


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=255, default="default.jpg")
    objects = UserManager()

    def __str__(self):
        template = '{0.first_name} {0.last_name}'
        return template.format(self)

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)

    def __str__(self):
        return self.title