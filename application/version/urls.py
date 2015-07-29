from django.conf.urls import url
from version import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	
	url(r'^project/(?P<url>[a-z 0-9 \. \/]+)$', views.project_edit),
	url(r'^new$',views.project_new),
	url(r'^$',views.home),
	# url(r'^',views.catchall),
	# url(r'^food/(?P<pk>[0-9]+)/$', views.food_detail),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
