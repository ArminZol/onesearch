from django.contrib import admin
from .models import Document, DocumentWord, Word

# Register your models here.

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ('doc_id', 'title', 'description')
	search_fields = ('doc_id', 'title', 'description')

@admin.register(DocumentWord)
class DocumentWordAdmin(admin.ModelAdmin):
	list_display = ('document', 'word', 'frequency')
	search_fields = ('document__title', 'word__word')

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
	list_display = ('word',)
	search_fields = ('word',)

