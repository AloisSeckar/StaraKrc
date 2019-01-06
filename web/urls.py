from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

from . import views

urlpatterns = [
	re_path(r'^$', views.indexView, name='index'),
	re_path(r'^articles/(?P<article_id>[0-9]+)/?', views.articleDetailView, name='articleDetail'),
	re_path(r'^articles/?', views.articleIndexView, name='articleIndex'),
	re_path(r'^books/?', views.bookIndexView, name='bookIndex'),
	re_path(r'^gallery/(?P<gallery_id>[0-9]+)/(?P<image_id>[0-9]+)/prev/?', views.galleryImagePrev, name='galleryImagePrev'),
	re_path(r'^gallery/(?P<gallery_id>[0-9]+)/(?P<image_id>[0-9]+)/next/?', views.galleryImageNext, name='galleryImageNext'),
	re_path(r'^gallery/(?P<gallery_id>[0-9]+)/(?P<image_id>[0-9]+)/move/?', views.galleryImageMove, name='galleryImageMove'),
	re_path(r'^gallery/(?P<gallery_id>[0-9]+)/(?P<image_id>[0-9]+)/delete/?', views.galleryImageDelete, name='galleryImageDelete'),
	re_path(r'^gallery/(?P<gallery_id>[0-9]+)/(?P<image_id>[0-9]+)/?', views.galleryImageView, name='galleryImage'),
	re_path(r'^gallery/(?P<gallery_id>[0-9]+)/?', views.galleryDetailView, name='galleryDetail'),
	re_path(r'^gallery/add/?', views.galleryImageAdd, name='galleryImageAdd'),
	re_path(r'^gallery/?', views.galleryIndexView, name='galleryIndex'),
	re_path(r'^links/?', views.linkIndexView, name='linkIndex'),
	re_path(r'^login/?', views.loginView, name='login'),
	re_path(r'^logout/?', views.logoutView, name='logout'),
	re_path(r'^news/?', views.newsView, name='news'),
	re_path(r'^(?!upload|static|admin)', views.unknownView, name='unknown')
]

if settings.DEBUG is True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
