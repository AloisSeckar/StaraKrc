from django.contrib import admin

from .models import Article, Book, Category, Gallery, Image, Link, News

class AdminArticle(admin.ModelAdmin):
	list_display = ('name', 'category', 'author', 'date_created', 'date_edited')

class AdminBook(admin.ModelAdmin):
	list_display = ('name', 'category', 'author', 'date_created', 'date_edited', 'writer', 'year')

class AdminCategory(admin.ModelAdmin):
	list_display = ('name', 'type')
	def has_delete_permission(self, request, obj=None):
		return False

class AdminImage(admin.ModelAdmin):
	list_display = ('image_id', 'name', 'author', 'date_created', 'date_edited', 'gallery')
	exclude = ('gallery','ord','prev','next')
	def has_add_permission(self, request):
		return False
	def has_delete_permission(self, request, obj=None):
		return False

class AdminGallery(admin.ModelAdmin):
	list_display = ('name', 'author', 'date_created', 'date_edited', 'parent')
	def has_delete_permission(self, request, obj=None):
		return False

class AdminLink(admin.ModelAdmin):
	list_display = ('name', 'category', 'author', 'date_created', 'date_edited')

class AdminNews(admin.ModelAdmin):
	list_display = ('news_id', 'author', 'date_created', 'content')

admin.site.register(Article, AdminArticle)
admin.site.register(Book, AdminBook)
admin.site.register(Category, AdminCategory)
admin.site.register(Gallery, AdminGallery)
admin.site.register(Image, AdminImage)
admin.site.register(Link, AdminLink)
admin.site.register(News, AdminNews)
