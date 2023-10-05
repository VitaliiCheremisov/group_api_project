from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

admin.site.empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name', 'year', 'description', 'genre', 'category')
    list_filter = ('year', 'genre', 'category')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'score', 'pub_date', 'title')
    search_fields = ('author', 'text', 'score', 'pub_date', 'title')
    list_filter = ('author', 'score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'reviews')
    search_fields = ('text', 'author', 'reviews')
    list_filter = ('author', 'pub_date')
