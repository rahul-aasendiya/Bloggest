from django.contrib import admin
from .models import Post, Category, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author', 'category',)
    readonly_fields = ('view_count',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','by', 'created_on','comment',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator',)



admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
