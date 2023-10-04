from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import (Category, Comment, CustomUser, Genre, GenreTitle,
                            Review, Title)


admin.site.empty_value_display = '-пусто-'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role', 'bio')
    list_filter = ('role',)

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

@admin.register(GenreTitle) 
class GenreTitleAdmin(admin.ModelAdmin): 
    list_display = ('title', 'genre') 
    search_fields = ('title__name', 'genre__name') 
    list_filter = ('genre__name',) 

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
