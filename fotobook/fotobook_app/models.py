from django.db import models
import re 
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', default='images/none/no-img.jpg', blank=False, null=False)

    user = models.ForeignKey('User', related_name='images', on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add = True)				
    updated_at = models.DateTimeField(auto_now = True)

class UserManager(models.Manager):
    def register(self, form):
        errors = {}
        email_check = User.objects.filter(email=form['email'])
        if len(form['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'

        if len(form['email']) < 1:
            errors['email'] = 'Email cannot be blank.'

        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
            
        if email_check:
            errors['email'] = "Email already in use"
        return errors

    def login_validate(self, form):
        errors = {}
        check = User.objects.filter(email=form['email'])
        if not check:
            errors['email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(form['password'].encode(), check[0].password.encode()):
                errors['email'] = "Email and password do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    about_me = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)