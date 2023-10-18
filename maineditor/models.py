from django.db import models


# Main Editor Model
class MainEditor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100, default='12345678')
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/maineditor/images')
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
        verbose_name_plural = 'Main Editor'



# Conference -> id, title, description, image, start_date, end_date, venue, status, main_editor_id, paper_submission_deadline, paper_review_deadline, paper_acceptance_deadline, paper_publish_deadline
class Conference(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='static/conference/images')
    start_date = models.DateField()
    end_date = models.DateField()
    venue = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    paper_submission_deadline = models.DateField()
    paper_review_deadline = models.DateField()
    paper_acceptance_deadline = models.DateField()
    paper_publish_deadline = models.DateField()
    main_editor_id = models.ForeignKey(MainEditor, on_delete=models.CASCADE)
    no_of_papers = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Conferences'

