import os.path
import time

from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField


class Category(models.Model):
	cat_id = models.AutoField(primary_key=True)
	type = models.CharField(choices=[('a', 'article'),('b', 'book'), ('l', 'link')], max_length=1, verbose_name = "Typ")
	ord = models.PositiveIntegerField(default=0)
	name = models.CharField(max_length=50, verbose_name = "Název")
	dscr = models.CharField(max_length=255)
	def __str__(self):
		return str(self.name)
	class Meta:
		verbose_name = "Kategorie"
		verbose_name_plural = "3. Kategorie"

class Gallery(models.Model):
	gallery_id = models.AutoField(primary_key=True)
	parent = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name = "Nadřazená galerie")
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name = "Autor")
	date_created = models.DateTimeField(auto_now_add=True, verbose_name = "Datum vytvoření")
	date_edited = models.DateTimeField(auto_now=True, verbose_name = "Poslední úprava")
	name = models.CharField(max_length=50, verbose_name = "Název")
	dscr = HTMLField(null=True, blank=True)
	def __str__(self):
		nameString = str(self.name)
		if self.parent is not None:
			nameString += ' (' + self.parent.name + ')'
		return nameString
	class Meta:
		verbose_name = "Galerie"
		verbose_name_plural = "1. Galerie"

def image_with_timestamp(instance, filename):
	return 'image/' + str(int(round(time.time()))) + '.' + os.path.splitext(filename)[1]

class Image(models.Model):
	image_id = models.AutoField(primary_key=True, verbose_name = "ID")
	gallery = models.ForeignKey(Gallery, on_delete=models.DO_NOTHING, verbose_name = "Galerie")
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name = "Autor")
	date_created = models.DateTimeField(auto_now_add=True, verbose_name = "Datum vytvoření")
	date_edited = models.DateTimeField(auto_now=True, verbose_name = "Poslední úprava")
	name = models.CharField(max_length=50, verbose_name = "Název")
	dscr = HTMLField(null=True, blank=True)
	image = models.FileField(upload_to=image_with_timestamp, default = 'image.png')
	ord = models.PositiveIntegerField(default=0)
	prev = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True, related_name = 'prevImage')
	next = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True, related_name = 'nextImage')
	def __str__(self):
		return '#' + str(self.image_id) + " - " + str(self.name) + " (" + str(self.gallery) + ")"
	@property
	def has_dscr(self):
		return self.dscr is not None and self.dscr.strip() != ""
	class Meta:
		verbose_name = "Obrázek"
		verbose_name_plural = "2. Obrázky"

class Article(models.Model):
	article_id = models.AutoField(primary_key=True)
	category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name = "Kategorie")
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name = "Autor")
	date_created = models.DateTimeField(auto_now_add=True, verbose_name = "Datum vytvoření")
	date_edited = models.DateTimeField(auto_now=True, verbose_name = "Poslední úprava")
	name = models.CharField(max_length=50, verbose_name = "Název")
	dscr = models.CharField(max_length=255)
	content = HTMLField()
	thumb = models.FileField(upload_to='article', default = 'article.png')
	gallery = models.ForeignKey(Gallery, on_delete=models.DO_NOTHING, null=True, blank=True)
	def __str__(self):
		return '#' + str(self.article_id) + " - " + str(self.name)
	class Meta:
		verbose_name = "Článek"
		verbose_name_plural = "4. Články"

class Book(models.Model):
	book_id = models.AutoField(primary_key=True)
	category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name = "Kategorie")
	ord = models.PositiveIntegerField(default=0)
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name = "Autor")
	date_created = models.DateTimeField(auto_now_add=True, verbose_name = "Datum vytvoření")
	date_edited = models.DateTimeField(auto_now=True, verbose_name = "Poslední úprava")
	name = models.CharField(max_length=100, verbose_name = "Název")
	writer = models.CharField(max_length=100, verbose_name = "Napsal")
	year = models.CharField(max_length=4, verbose_name = "Rok vydání")
	dscr = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	review = models.CharField(max_length=255, null=True, blank=True)
	thumb = models.FileField(upload_to='book', default = 'book.png')
	def __str__(self):
		return '#' + str(self.book_id) + " - " + str(self.name)
	class Meta:
		verbose_name = "Kniha"
		verbose_name_plural = "5. Knihy"

class Link(models.Model):
	link_id = models.AutoField(primary_key=True)
	category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name = "Kategorie")
	ord = models.PositiveIntegerField(default=0)
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	date_created = models.DateTimeField(auto_now_add=True, verbose_name = "Datum vytvoření")
	date_edited = models.DateTimeField(auto_now=True, verbose_name = "Poslední úprava")
	name = models.CharField(max_length=100, verbose_name = "Název")
	dscr = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	thumb = models.FileField(upload_to='link', default = 'link.png')
	def __str__(self):
		return '#' + str(self.link_id) + " - " + str(self.name) + " (" + str(self.url) + ")"
	class Meta:
		verbose_name = "Odkaz"
		verbose_name_plural = "6. Odkazy"

class News(models.Model):
	news_id = models.AutoField(primary_key=True, verbose_name = "ID")
	date_created = models.DateField(auto_now_add=True, verbose_name = "Datum vytvoření")
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name = "Autor")
	content = HTMLField()
	class Meta:
		verbose_name = "Novinka"
		verbose_name_plural = "7. Novinky"
