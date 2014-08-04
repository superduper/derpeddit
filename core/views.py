from django.views.generic import RedirectView


class IndexView(RedirectView):
    url = 'derpeddit.github.com'
