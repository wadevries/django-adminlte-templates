# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html, format_html_join

from os.path import join as pjoin

from django.utils.safestring import mark_safe

from ..settings import Settings
from ..widgets import FontAwesomeIcon, Label

register = template.Library()

_bootstrap_url_base = Settings.get('STATIC.BOOTSTRAP_URL_BASE', None)
bootstrap_url_base = _bootstrap_url_base if _bootstrap_url_base else static('bootstrap')
_fontawesome_url_base = Settings.get('STATIC.FONTAWESOME_URL_BASE', None)
fontawesome_url_base = _fontawesome_url_base if _fontawesome_url_base else static('Font-Awesome')
_ionicons_url_base = Settings.get('STATIC.IONICONS_URL_BASE', None)
ionicons_url_base = _ionicons_url_base if _ionicons_url_base else static('ionicons')
_adminlte_url_base = Settings.get('STATIC.ADMINLTE_URL_BASE', None)
adminlte_url_base = _adminlte_url_base if _adminlte_url_base else static('AdminLTE')
_jquery_url = Settings.get('STATIC.JQUERY_URL', None)
jquery_url = _jquery_url if _jquery_url else static('AdminLTE/plugins/jQuery/jQuery-2.1.4.min.js')

@register.simple_tag
def alte_load_css(*names):
    urls = []
    for name in names:
        if name == 'bootstrap':
            urls.append(pjoin(bootstrap_url_base, 'css/bootstrap.min.css'))
        elif name == 'fontawesome':
            urls.append(pjoin(fontawesome_url_base, 'css/font-awesome.min.css'))
        elif name == 'ionicons':
            urls.append(pjoin(ionicons_url_base, 'css/ionicons.min.css'))
        elif name == 'adminlte':
            urls.append(pjoin(adminlte_url_base, 'css/AdminLTE.min.css'))

    return format_html_join('\n', '<link href="{}" rel="stylesheet" type="text/css" />', ((url,) for url in urls))

@register.simple_tag
def alte_load_js(*names):
    urls = []
    for name in names:
        if name == 'jquery':
            urls.append(jquery_url)
        elif name == 'bootstrap':
            urls.append(pjoin(bootstrap_url_base, 'js/bootstrap.min.js'))
        elif name == 'adminlte':
            urls.append(pjoin(adminlte_url_base, 'js/app.min.js'))

    return format_html_join('\n', '<script src="{}" type="text/javascript"></script>', ((url,) for url in urls))

@register.simple_tag
def alte_load_skin_css():
    skinurl = pjoin(adminlte_url_base, 'css/skins/skin-%s.min.css' % Settings['THEME.SKIN'])
    return format_html('<link href="{}" rel="stylesheet" type="text/css" />', skinurl)

@register.simple_tag
def alte_load_plugin_css(*names):
    urls = (pjoin(adminlte_url_base, 'plugins/{}.css'.format(name)) for name in names if name.startswith('iCheck/'))

    return format_html_join('\n', '<link href="{}" rel="stylesheet" type="text/css" />', ((url,) for url in urls))

@register.simple_tag
def alte_load_plugin_js(*names):
    urls = []
    for name in names:
        if name == 'iCheck':
            urls.append(pjoin(adminlte_url_base, 'plugins/iCheck/icheck.min.js'))
        elif name == 'slimScroll':
            urls.append(pjoin(adminlte_url_base, 'plugins/slimScroll/jquery.slimscroll.js'))

    return format_html_join('\n', '<script src="{}" type="text/javascript"></script>', ((url,) for url in urls))

@register.simple_tag
def alte_get_img_url(name):
    return pjoin(adminlte_url_base, name)

@register.simple_tag(takes_context=True)
def alte_sidebar(context):
    sidebar_generator = Settings['SIDEBAR_GENERATOR']
    if callable(sidebar_generator):
        sidebar = sidebar_generator(context['request'])
        return sidebar.to_html()
    else:
        return ''

@register.simple_tag
def alte_widget(name, *args, **kwargs):
    if name == 'fa':
        return FontAwesomeIcon(*args, **kwargs).to_html()
    elif name == 'label':
        return Label(*args, **kwargs).to_html()
