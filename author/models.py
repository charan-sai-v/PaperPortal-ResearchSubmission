from django.db import models

# Author model -> id, name, email, password, created_at, updated_at, is_confirmed, token, token_expires_at
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_confirmed = models.BooleanField(default=False)
    token = models.CharField(max_length=255, null=True)
    token_expires_at = models.DateTimeField(null=True)
    password_reset_token = models.CharField(max_length=255, null=True)
    password_reset_token_expires_at = models.DateTimeField(null=True)
    login_token = models.CharField(max_length=255, null=True)
    login_token_expires_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'author'
        verbose_name = 'author'
        verbose_name_plural = 'authors'


# Paper model -> id, title, abstract, created_at, updated_at, author_id, file, status, review_1, review_2

