from django.conf.urls import patterns, url
from url_utils import include


api_urlpatterns = patterns('',
   url(r"^posts", include('posts.urls', pattern_varname='apis')),
   url(r"^core", include('core.urls', pattern_varname='apis')),
)

urlpatterns = patterns('',
    url(r'^', include('core.urls')),
    url(r'^api/v1/', include(api_urlpatterns, namespace="api"))
)
