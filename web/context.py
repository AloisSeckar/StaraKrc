# context processors definition
from django.conf import settings

# global variables for templates
def global_variables(request):
	return {
		'site_name': settings.SITE_NAME,
		'site_bg': settings.SITE_BG,
		'toplist_url': settings.TOPLIST_URL,
		'toplist_img': settings.TOPLIST_IMG,
	}
