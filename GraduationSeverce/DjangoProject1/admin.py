from django.contrib import admin

# Register your models here.

from DjangoProject1 import models
admin.site.register(models.AuthorList)
admin.site.register(models.Book)
admin.site.register(models.Colordic)