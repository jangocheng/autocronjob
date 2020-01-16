from importlib import import_module

from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.templatetags.admin_list import result_headers, result_hidden_fields, results
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.contrib.admin.views.main import (
    ALL_VAR
)
DOT = '.'
register = template.Library()


CUSTOM_FIELD_RENDERER = getattr(settings, 'DAB_FIELD_RENDERER', False)


@register.simple_tag(takes_context=True)
def render_with_template_if_exist(context, template, fallback):
    text = fallback
    try:
        text = render_to_string(template, context)
    except:
        pass
    return text

@register.simple_tag(takes_context=True)
def language_selector(context):
    """ displays a language selector dropdown in the admin, based on Django "LANGUAGES" context.
        requires:
            * USE_I18N = True / settings.py
            * LANGUAGES specified / settings.py (otherwise all Django locales will be displayed)
            * "set_language" url configured (see https://docs.djangoproject.com/en/dev/topics/i18n/translation/#the-set-language-redirect-view)
    """
    output = ""
    i18 = getattr(settings, 'USE_I18N', False)
    if i18:
        template = "admin/language_selector.html"
        context['i18n_is_set'] = True
        try:
            output = render_to_string(template, context)
        except:
            pass
    return output


@register.filter(name='column_width')
def column_width(value):
    try:
        return 12 // len(list(value))
    except ZeroDivisionError:
        return 12


@register.filter(name='form_fieldset_column_width')
def form_fieldset_column_width(form):
    def max_line(fieldset):
        try:
            return max([len(list(line)) for line in fieldset])
        # This ValueError is for case that fieldset has no line.
        except ValueError:
            return 0

    try:
        width = max([max_line(fieldset) for fieldset in form])
        return 12 // width
    except ValueError:
        return 12


@register.filter(name='fieldset_column_width')
def fieldset_column_width(fieldset):
    try:
        width = max([len(list(line)) for line in fieldset])
        return 12 // width
    except ValueError:
        return 12


@register.simple_tag(takes_context=True)
def render_app_name(context, app, template="/admin_app_name.html"):
    """ Render the application name using the default template name. If it cannot find a
        template matching the given path, fallback to the application name.
    """
    try:
        template = app['app_label'] + template
        text = render_to_string(template, context)
    except:
        text = app['name']
    return text


@register.simple_tag(takes_context=True)
def render_app_label(context, app, fallback=""):
    """ Render the application label.
    """
    try:
        text = app['app_label']
    except KeyError:
        text = fallback
    except TypeError:
        text = app
    return text


@register.simple_tag(takes_context=True)
def render_app_description(context, app, fallback="", template="/admin_app_description.html"):
    """ Render the application description using the default template name. If it cannot find a
        template matching the given path, fallback to the fallback argument.
    """
    try:
        template = app['app_label'] + template
        text = render_to_string(template, context)
    except:
        text = fallback
    return text


@register.simple_tag(takes_context=True, name="dab_field_rendering")
def custom_field_rendering(context, field, *args, **kwargs):
    """ Wrapper for rendering the field via an external renderer """
    if CUSTOM_FIELD_RENDERER:
        mod, cls = CUSTOM_FIELD_RENDERER.rsplit(".", 1)
        field_renderer = getattr(import_module(mod), cls)
        if field_renderer:
            return field_renderer(field, **kwargs).render()
    return field


@register.tag(name='result_list')
def result_list_tag(parser, token):
    return InclusionAdminNode(
        parser, token,
        func=result_list,
        template_name='../_change_list_results.html',
        takes_context=False,
    )


@register.tag(name='pagination')
def pagination_tag(parser, token):
    return InclusionAdminNode(
        parser, token,
        func=pagination,
        template_name='../_pagination.html',
        takes_context=False,
    )


def result_list(cl):
    """
    Displays the headers and data list together
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': list(results(cl))}


def pagination(cl):
    """
    Generate the series of links to the pages in a paginated list.
    """
    paginator, page_num = cl.paginator, cl.page_num

    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2

        # If there are 10 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 10:
            page_range = range(paginator.num_pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > (ON_EACH_SIDE + ON_ENDS):
                page_range += [
                    *range(0, ON_ENDS), DOT,
                    *range(page_num - ON_EACH_SIDE, page_num + 1),
                ]
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
                page_range += [
                    *range(page_num + 1, page_num + ON_EACH_SIDE + 1), DOT,
                    *range(paginator.num_pages - ON_ENDS, paginator.num_pages)
                ]
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))

    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return {
        'cl': cl,
        'pagination_required': pagination_required,
        'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: ''}),
        'page_range': page_range,
        'ALL_VAR': ALL_VAR,
        '1': 1,
    }