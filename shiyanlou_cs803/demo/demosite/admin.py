from django.contrib import admin
from .models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_data', 'update_time',)

admin.site.register(Article,ArticleAdmin)
