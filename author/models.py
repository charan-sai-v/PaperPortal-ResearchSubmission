from django.db import models
from maineditor.models import Conference, MainEditor

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
class Paper(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    file = models.FileField(upload_to='papers/')
    status = models.CharField(max_length=255, default='pending')
    no_of_authors = models.IntegerField(default=1)
    author_1 = models.CharField(max_length=255 )
    author_2 = models.CharField(max_length=255, null=True)
    author_3 = models.CharField(max_length=255, null=True)
    author_4 = models.CharField(max_length=255, null=True)
    author_5 = models.CharField(max_length=255, null=True)
    author_6 = models.CharField(max_length=255, null=True)
    review_remark_1 = models.TextField(null=True)
    review_remark_2 = models.TextField(null=True)
    is_review_1_completed = models.BooleanField(default=False)
    is_review_2_completed = models.BooleanField(default=False)
    maineditor = models.ForeignKey(MainEditor, on_delete=models.CASCADE, related_name='maineditor', null=True)
    subeditor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='subeditor', null=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'paper'
        verbose_name = 'paper'
        verbose_name_plural = 'papers'



# Contact model -> email, subject, message, created_at, updated_at
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'contact'
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'