from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from core.views import IndexView
from core.api import LoginView, AuthProfileView, LogoutView, SignUpView
from project.url_utils import u

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view()),
)

apis = patterns("",
    url(u('auth', 'login'), LoginView.as_view()),
    url(u('auth','logout'), LogoutView.as_view()),
    url(u('auth','signup'), SignUpView.as_view()),
    url(u('auth','profile'), AuthProfileView.as_view())
)

# Format suffixes
apis = format_suffix_patterns(apis, allowed=['json', 'api'])
