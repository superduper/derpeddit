from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from posts.api import PostView, PostListView, VoteView, CommentListView
from project.url_utils import u, arg, ROOT


apis = patterns("",
    url(ROOT, PostListView.as_view()),
    url(u(arg("pk")), PostView.as_view()),
    url(u(arg("pk"), "vote"), VoteView.as_view()),
    url(u(arg("pk"), "comment"), CommentListView.as_view()),
)

# Format suffixes
apis = format_suffix_patterns(apis, allowed=['json', 'api'])
