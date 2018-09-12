from django.conf.urls import url
from routing import views

urlpatterns = [
    url('^simple_route/$', views.simple_rout),
    url(r'^slug_route/([0-9a-z_-]{,16})/$', views.slug_route),
    url(r'^sum_route/([-0-9]+)/([-0-9]+)/$', views.sum_route),
    url(r'^sum_get_method/$', views.sum_get_method),
    url(r'^sum_post_method/$', views.sum_post_method)
]
