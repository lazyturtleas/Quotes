from django.contrib import admin
from .models import Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("text", "source_name", "genre", "author_name", "weight", "likes", "dislikes", "views")
    list_filter = ("genre",)
    search_fields = ("text", "source_name", "author_name")
    ordering = ("-likes",)
