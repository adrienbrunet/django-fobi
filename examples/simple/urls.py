from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

from fobi.settings import DEFAULT_THEME

from nine import versions

admin.autodiscover()

# Mapping.
fobi_theme_home_template_mapping = {
    'bootstrap3': 'home/bootstrap3.html',
    'foundation5': 'home/foundation5.html',
    'simple': 'home/simple.html',
}

# Get the template to be used.
fobi_home_template = fobi_theme_home_template_mapping.get(
    DEFAULT_THEME,
    'home/base.html'
)

FOBI_EDIT_URLS_PREFIX = ''
if DEFAULT_THEME in ('simple', 'djangocms_admin_style_theme'):
    FOBI_EDIT_URLS_PREFIX = 'admin/'

urlpatterns = []

url_patterns_args = [
    # DB Store plugin URLs
    # namespace='fobi'
    url(r'^fobi/plugins/form-handlers/db-store/',
        include('fobi.contrib.plugins.form_handlers.db_store.urls')),
    url(r'^fobi/plugins/form-wizard-handlers/db-store/',
        include('fobi.contrib.plugins.form_handlers.db_store.urls.'
                'form_wizard_handlers')),

    # django-fobi URLs:
    # namespace='fobi'
    url(r'^fobi/', include('fobi.urls.view')),
    # namespace='fobi'
    url(r'^{0}fobi/'.format(FOBI_EDIT_URLS_PREFIX),
        include('fobi.urls.edit')),

    url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # django-registration URLs:
    url(r'^accounts/', include('registration.backends.default.urls')),

    # foo URLs:
    url(r'^foo/', include('foo.urls')),

    # bar URLs:
    # url(r'^bar/', include('bar.urls')),

    url(r'^$', TemplateView.as_view(template_name=fobi_home_template)),

    # django-fobi public forms contrib app:
    # url(r'^', include('fobi.contrib.apps.public_forms.urls')),
]

if versions.DJANGO_LTE_1_7:
    urlpatterns += i18n_patterns('', *url_patterns_args)
else:
    urlpatterns += i18n_patterns(*url_patterns_args)

# Serving media and static in debug/developer mode.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# Conditionally including FeinCMS URls in case if
# FeinCMS in installed apps.
if 'feincms' in settings.INSTALLED_APPS:
    from page.models import Page
    Page
    url_patterns_args = [
        url(r'^pages/', include('feincms.urls')),
    ]
    if versions.DJANGO_LTE_1_7:
        urlpatterns += i18n_patterns('', *url_patterns_args)
    else:
        urlpatterns += i18n_patterns(*url_patterns_args)

# Conditionally including DjangoCMS URls in case if
# DjangoCMS in installed apps.
if 'cms' in settings.INSTALLED_APPS:
    url_patterns_args = [
        url(r'^cms-pages/', include('cms.urls')),
    ]
    if versions.DJANGO_LTE_1_7:
        urlpatterns += i18n_patterns('', *url_patterns_args)
    else:
        urlpatterns += i18n_patterns(*url_patterns_args)

# Conditionally including Django REST framework integration app
if 'fobi.contrib.apps.drf_integration' in settings.INSTALLED_APPS:
    from fobi.contrib.apps.drf_integration.urls import fobi_router
    urlpatterns += [
        url(r'^api/', include(fobi_router.urls))
    ]

# Conditionally including Captcha URls in case if
# Captcha in installed apps.
if getattr(settings, 'ENABLE_CAPTCHA', False):
    try:
        from captcha.fields import ReCaptchaField
    except ImportError:
        try:
            from captcha.fields import CaptchaField
            if 'captcha' in settings.INSTALLED_APPS:
                urlpatterns += [
                    url(r'^captcha/', include('captcha.urls')),
                ]
        except ImportError:
            pass
