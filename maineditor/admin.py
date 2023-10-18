from django.contrib import admin
from .models import MainEditor, Conference


class MainEditorModel(admin.ModelAdmin):
    fields = ['name', 'email', 'phone', 'address', 'image', 'designation', 'password']

# Register your models here.
admin.site.register(MainEditor, MainEditorModel)
admin.site.register(Conference)
