from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import LocaleRegexURLResolver
from django.utils import six
from django.utils.importlib import import_module

arg = lambda s: r"(?P<%s>\d+)" % s
# concat url pattern parts
u = lambda *a: r"^/%s$" % "/".join(a)
ROOT = "^$"

def include(arg, namespace=None, app_name=None,  pattern_varname='urlpatterns'):
    """
    Extends ol' django url include with support of custom pattern variable name,
    in case you want to use something other than "urlpatterns" you can do that this way:
        include("foo.urls:custompatterns")
    or
        include("foo.urls", pattern_varname="custompatterns")
    instead of:
        import foo.urls
        include(foo.urls.custompatterns, pattern_varname="custompatterns")
    """
    if isinstance(arg, tuple):
        # callable returning a namespace hint
        if namespace:
            raise ImproperlyConfigured('Cannot override the namespace for a dynamic module that provides a namespace')
        urlconf_module, app_name, namespace = arg
    else:
        # No namespace hint - use manually provided namespace
        urlconf_module = arg

    if isinstance(urlconf_module, str) and ":" in urlconf_module:
        urlconf_module, pattern_varname = urlconf_module.split(':')

    if isinstance(urlconf_module, six.string_types):
        urlconf_module = import_module(urlconf_module)

    patterns = getattr(urlconf_module, pattern_varname, urlconf_module)
    # Make sure we can iterate through the patterns (without this, some
    # testcases will break).
    if isinstance(patterns, (list, tuple)):
        for url_pattern in patterns:
            # Test if the LocaleRegexURLResolver is used within the include;
            # this should throw an error since this is not allowed!
            if isinstance(url_pattern, LocaleRegexURLResolver):
                raise ImproperlyConfigured(
                    'Using i18n_patterns in an included URLconf is not allowed.')
    # urlconf_full_path has to be unique, thats why we should care about pattern_varname
    if pattern_varname != "urlpatterns":
        urlconf_module = patterns
    return (urlconf_module, app_name, namespace)
