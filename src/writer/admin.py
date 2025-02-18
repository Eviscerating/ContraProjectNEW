from django.contrib import admin

# Register your models here.
from . import models  as writer_models

admin.site.register(writer_models.Article)