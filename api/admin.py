from django.contrib import admin
from .models import Category,Clothes,Saved,History,Experiment,Feedback
# Register your models here.

# admin.site.register(Clothes)
admin.site.register(Saved)
admin.site.register(Category)
admin.site.register(History)
admin.site.register(Experiment)
admin.site.register(Feedback)