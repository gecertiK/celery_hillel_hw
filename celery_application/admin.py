from django.contrib import admin

from .models import Author, Quote


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday')
    search_fields = ['name']


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')
    search_fields = ['name', 'author']