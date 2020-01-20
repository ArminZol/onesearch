from django.contrib import admin
from .models import Document

# Register your models here.

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ('doc_id', 'title', 'description')
	search_fields = ('doc_id', 'title', 'description')