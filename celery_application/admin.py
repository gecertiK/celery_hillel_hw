from django.contrib import admin  # noqa:F401

from celery_application.models import Author, Quotes


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Quotes)
class QuotesAdmin(admin.ModelAdmin):
    list_display = ['texts', 'author']
    search_fields = ['author']
