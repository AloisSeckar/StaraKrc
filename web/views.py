import os.path

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render


from .forms import MoveImageForm, NewImageForm
from .models import Article, Book, Category, Gallery, Image, Link, News
from .utils import errorHelper, StatusMessage

def indexView(request):
	lastNews = News.objects.all().order_by('-date_created')[:5]
	return render(request, 'index.html', {'lastNews' : lastNews})

def newsView(request):
	allNews = News.objects.all().order_by('-date_created')
	return render(request, 'news.html', {'allNews' : allNews})

def articleIndexView(request):
	articles = Article.objects.all().order_by('-date_created')
	for article in articles:
		if not os.path.isfile(os.path.join(settings.MEDIA_ROOT, article.thumb.name)):
			article.thumb.name = 'article.png'
	return render(request, 'articleIndex.html', {'articles' : articles})
	
def articleDetailView(request, article_id):
	try:
		article = Article.objects.get(article_id = article_id)
		if not os.path.isfile(os.path.join(settings.MEDIA_ROOT, article.thumb.name)):
			article.thumb.name = 'article.png'
		return render(request, 'articleDetail.html', {'article' : article})
	except Article.DoesNotExist:
		return render(request, 'articleDetail.html', {'msg' : 'Článek s požadovaným ID nebyl nalezen...'})

def bookIndexView(request):
	bookCount = 0
	bookList = []
	categories = Category.objects.filter(type = "b").order_by('ord')
	for cat in categories:
		relatedBooks = Book.objects.filter(category = cat).order_by('ord')
		for book in relatedBooks:
			if not os.path.isfile(os.path.join(settings.MEDIA_ROOT, book.thumb.name)):
				book.thumb.name = 'book.png'
		bookCount += relatedBooks.count()
		bookObject = [cat, relatedBooks]
		bookList.append(bookObject)
	return render(request, 'bookIndex.html', {'bookList' : bookList, 'bookCount' : bookCount})

def galleryIndexView(request):
	return galleryIndexViewWithStatus(request, None)
	
def galleryIndexViewWithStatus(request, status):
	itemCount = [Gallery.objects.all().count(), Image.objects.all().count()]
	galleryList = []
	galleries = Gallery.objects.filter(parent__isnull=True).order_by('name')
	for currentGallery in galleries:
		imageCount = Image.objects.filter(gallery = currentGallery).count()
		relatedImages = Image.objects.filter(gallery = currentGallery).order_by('ord')[:6]
		relatedGalleryList = []
		relatedGalleries = Gallery.objects.filter(parent = currentGallery).order_by('name')
		for relatedGallery in relatedGalleries:
			relatedGalleryImages = Image.objects.filter(gallery = relatedGallery).count()
			relatedGalleryList.append([relatedGallery, relatedGalleryImages])
		relatedArticles = Article.objects.filter(gallery = currentGallery).order_by('name')
		galleryObject = [currentGallery, imageCount, relatedImages, relatedGalleryList, relatedArticles]
		galleryList.append(galleryObject)
	newImageForm = NewImageForm()
	return render(request, 'galleryIndex.html', {'galleryList' : galleryList, 'itemCount' : itemCount, 'status' : status, 'newImageForm' : newImageForm})
	
def galleryDetailView(request, gallery_id):
	try:
		currentGallery = Gallery.objects.get(gallery_id = gallery_id)
		if currentGallery.parent is not None:
			try:
				parentGallery = Gallery.objects.get(gallery_id = currentGallery.parent.gallery_id)
			except Gallery.DoesNotExist:
				parentGallery = None
		else:
			parentGallery = None
		relatedImages = Image.objects.filter(gallery = currentGallery).order_by('ord')
		relatedGalleryList = []
		relatedGalleries = Gallery.objects.filter(parent = currentGallery).order_by('name')
		for relatedGallery in relatedGalleries:
			relatedGalleryImages = Image.objects.filter(gallery = relatedGallery).count()
			relatedGalleryList.append([relatedGallery, relatedGalleryImages])
		relatedArticles = Article.objects.filter(gallery = currentGallery).order_by('name')
		galleryObject = [currentGallery, parentGallery, relatedImages, relatedGalleryList, relatedArticles]
		imageWithCurrentGallery = Image()
		imageWithCurrentGallery.gallery = currentGallery
		newImageForm = NewImageForm(instance = imageWithCurrentGallery)
		return render(request, 'galleryDetail.html', {'galleryObject' : galleryObject, 'newImageForm' : newImageForm})
	except Gallery.DoesNotExist:
		return render(request, 'galleryDetail.html', {'msg' : 'Galerie s požadovaným ID nebyla nalezena...'})

def galleryImageView(request, gallery_id, image_id):
	return galleryImageViewWithStatus(request, gallery_id, image_id, None)

def galleryImageViewWithStatus(request, gallery_id, image_id, status):
	try:
		gallery = Gallery.objects.get(gallery_id = gallery_id)
		if image_id is None:
			return galleryDetailView(request, gallery_id)
		image = Image.objects.get(image_id = image_id)
		moveImageForm = MoveImageForm(instance = image)
		imageWithCurrentGallery = Image()
		imageWithCurrentGallery.gallery = gallery
		newImageForm = NewImageForm(instance = imageWithCurrentGallery)
		return render(request, 'galleryImage.html', {'gallery' : gallery, 'image' : image, 'moveImageForm' : moveImageForm, 'newImageForm' : newImageForm, 'status' : status})
	except Gallery.DoesNotExist:
		return render(request, 'galleryImage.html', {'msg' : 'Galerie s požadovaným ID nebyla nalezena...'})
	except Image.DoesNotExist:
		return render(request, 'galleryImage.html', {'msg' : 'Obrázek s požadovaným ID nebyl nalezen...'})

def galleryImagePrev(request, gallery_id, image_id):
	try:
		image = Image.objects.get(image_id = image_id)
		prevImage = image.prev
		nextImage = image.next
		if prevImage is not None:
			prevPrevImage = prevImage.prev
			image.prev = prevImage.prev
			prevImage.prev = image
			prevImage.next = image.next
			image.next = prevImage
			image.ord -= 1
			prevImage.ord += 1
			image.save()
			prevImage.save()
			if nextImage is not None:
				nextImage.prev = prevImage
				nextImage.save()
			if prevPrevImage is not None:
				prevPrevImage.next = image
				prevPrevImage.save()
			status = StatusMessage('Obrázek byl posunut vzad', settings.STYLE_SUCCESS)
		else:
			status = StatusMessage('Obrázek již nelze přesunout více vzad', settings.STYLE_ERROR)
	except Exception as ex:
		status = StatusMessage('Obrázek se nepodařilo správně přesunout vzad' + errorHelper(ex), settings.STYLE_ERROR)
	return galleryImageViewWithStatus(request, gallery_id, image_id, status)

def galleryImageNext(request, gallery_id, image_id):
	try:
		image = Image.objects.get(image_id = image_id)
		prevImage = image.prev
		nextImage = image.next
		if nextImage is not None:
			nextNextImage = nextImage.next
			image.next = nextImage.next
			nextImage.next = image
			nextImage.prev = image.prev
			image.prev = nextImage
			image.ord += 1
			nextImage.ord -= 1
			image.save()
			nextImage.save()
			if prevImage is not None:
				prevImage.next = nextImage
				prevImage.save()
			if nextNextImage is not None:
				nextNextImage.prev = image
				nextNextImage.save()
			status = StatusMessage('Obrázek byl posunut vpřed', settings.STYLE_SUCCESS)
		else:
			status = StatusMessage('Obrázek již nelze přesunout více vpřed', settings.STYLE_ERROR)
	except Exception as ex:
		status = StatusMessage('Obrázek se nepodařilo správně přesunout vpřed' + errorHelper(ex), settings.STYLE_ERROR)
	return galleryImageViewWithStatus(request, gallery_id, image_id, status)

def galleryImageMove(request, gallery_id, image_id):
	try:
		if request.method == 'POST':
			image = Image.objects.get(image_id = image_id)
			moveImageForm = MoveImageForm(request.POST)
			if moveImageForm.is_valid():
				sourceGallery = image.gallery
				targetGallery = moveImageForm.cleaned_data['gallery']
				if sourceGallery != targetGallery:
					image.gallery = targetGallery
					prevImage = image.prev
					if prevImage is not None:
						prevImage.next = image.next
						prevImage.save()
					nextImage = image.next
					if nextImage is not None:
						nextImage.prev = image.prev
						nextImage.save()
					followingImages = Image.objects.filter(gallery = sourceGallery, ord__gt = image.ord)
					for followingImage in followingImages:
						followingImage.ord -= 1
						followingImage.save()
					lastImage = Image.objects.filter(gallery = targetGallery).order_by('-ord').first()
					if lastImage is not None:
						image.ord = lastImage.ord + 1
						image.prev = lastImage
						lastImage.next = image
						lastImage.save()
					else:
						image.ord = 1
						image.prev = None
					image.next = None
					image.save()
					status = StatusMessage('Obrázek byl přesunout do nové galerie', settings.STYLE_SUCCESS)
				else:
					raise ValueError('Nesmí být vybrána stejná galerie')
			else:
				raise ValueError('Neplatné hodnoty formuláře')
		else:
			status = None
	except Exception as ex:
		status = StatusMessage('Obrázek se nepodařilo správně přesunout do nové galerie' + errorHelper(ex), settings.STYLE_ERROR)
	return galleryImageViewWithStatus(request, targetGallery.gallery_id, image_id, status)

def galleryImageAdd(request):
	try:
		if request.method == 'POST':
			newImageForm = NewImageForm(request.POST, request.FILES)
			if newImageForm.is_valid():
				newImage = newImageForm.save(commit = False)
				newImage.image = newImageForm.cleaned_data['image']
				newImage.author = request.user
				newImage.save()
				lastImage = Image.objects.filter(gallery = newImage.gallery).order_by('-ord').first()
				if lastImage is not None:
					newImage.ord = lastImage.ord + 1
					newImage.prev = lastImage
					lastImage.next = newImage
					lastImage.save()
				else:
					newImage.ord = 1
					newImage.prev = None
				newImage.save()
				status = StatusMessage('Nový obrázek byl nahrán', settings.STYLE_SUCCESS)
				return galleryImageViewWithStatus(request, newImage.gallery.gallery_id, newImage.image_id, status)
			else:
				raise ValueError('Neplatné hodnoty formuláře')
		else:
			status = None
	except Exception as ex:
		status = StatusMessage('Nový obrázek se nepodařilo nahrát' + errorHelper(ex), settings.STYLE_ERROR)
	return galleryIndexViewWithStatus(request, status)

def galleryImageDelete(request, gallery_id, image_id):
	newImageId = None
	try:
		image = Image.objects.get(image_id = image_id)
		prevImage = image.prev
		if prevImage is not None:
			prevImage.next = image.next
			prevImage.save()
			newImageId = prevImage.image_id
		nextImage = image.next
		if nextImage is not None:
			nextImage.prev = image.prev
			nextImage.save()
			newImageId = nextImage.image_id
		followingImages = Image.objects.filter(gallery = image.gallery, ord__gt = image.ord)
		for followingImage in followingImages:
			followingImage.ord -= 1
			followingImage.save()
		image.delete()
		status = StatusMessage('Obrázek byl smazán', settings.STYLE_SUCCESS)
	except Exception as ex:
		status = StatusMessage('Obrázek se nepodařilo správně smazat' + errorHelper(ex), settings.STYLE_ERROR)
	return galleryImageViewWithStatus(request, gallery_id, newImageId, status)

def linkIndexView(request):
	linkCount = 0
	linkList = []
	categories = Category.objects.filter(type = "l").order_by('ord')
	for cat in categories:
		relatedLinks = Link.objects.filter(category = cat).order_by('ord')
		for link in relatedLinks:
			if not os.path.isfile(os.path.join(settings.MEDIA_ROOT, link.thumb.name)):
				link.thumb.name = 'link.png'
		linkCount += relatedLinks.count()
		linkObject = [cat, relatedLinks]
		linkList.append(linkObject)
	return render(request, 'linkIndex.html', {'linkList' : linkList, 'linkCount' : linkCount})

def loginView(request):
	status = None
	next = request.GET.get('next')
	if request.user.is_authenticated != True:
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				next = request.POST['next']
				if next is not None and next != "None":
					return HttpResponseRedirect(next)
				status = StatusMessage('Přihlášení proběhlo úspěšně', settings.STYLE_SUCCESS)
			else:
				status = StatusMessage('Nesprávné jméno nebo heslo', settings.STYLE_ERROR)
	return render(request, 'login.html', {'status' : status, 'next' : next})

def logoutView(request):
	logout(request)
	return render(request, 'logout.html', {})
	
def unknownView(request):
	return render(request, 'unknown.html', {})