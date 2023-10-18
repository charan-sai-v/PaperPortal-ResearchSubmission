from django.db import models


class SubEditor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100, default='12345678')
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/subeditor/images')
    designation = models.CharField(max_length=100)
    
    is_password_changed = models.BooleanField(default=False)
    login_token = models.CharField(max_length=255, null=True, blank=True)
    login_token_expires_at = models.DateTimeField(null=True, blank=True)
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    password_reset_token_expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Sub Editor'