from django.contrib import admin
from . import models


admin.site.register(models.Products)
admin.site.register(models.variants)
admin.site.register(models.Category)
