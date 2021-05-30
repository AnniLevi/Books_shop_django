from django.contrib import admin
from sales_manager.models import Book, Comment


class CommentAdmin(admin.StackedInline):
    model = Comment
    readonly_fields = ('like', )


class BookInline(admin.ModelAdmin):
    inlines = (CommentAdmin, )
    # readonly_fields = ('likes', )
    list_filter = ('date_publish', )
    # list_editable = ('title', )
    # list_display = ('title', 'text', )
    # list_display_links = ('text', )


admin.site.register(Book, BookInline)
