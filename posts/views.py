from django.views.generic import FormView, TemplateView


class SubmitPostView(FormView):
    template_name = "posts/submit_new.jade"

class IndexView(TemplateView):
    template_name = "posts/index.jade"

