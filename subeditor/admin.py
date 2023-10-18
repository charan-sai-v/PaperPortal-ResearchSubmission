from django.contrib import admin
from .models import SubEditor

class SubEditorModel(admin.ModelAdmin):
    fields = ['name', 'email', 'phone', 'address', 'image', 'designation', 'password']

# Register your models here.
admin.site.register(SubEditor, SubEditorModel)
