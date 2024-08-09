from django.contrib import admin

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'name',
        'is_published',
    )
    list_editable = (
        'is_published',
    )


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'is_published',
    )
    list_editable = (
        'is_published',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'location',
        'is_published',
        'author',
    )
    list_editable = (
        'category',
        'is_published',
    )
    list_filter = (
        'category',
        'location',
    )
    search_fields = (
        'title',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
