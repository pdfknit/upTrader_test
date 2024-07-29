from django import template
from django.urls import resolve
from menu.models import Menu, MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path
    menu = Menu.objects.get(name=menu_name)
    items = MenuItem.objects.filter(menu=menu).order_by('order')
    return render_menu(items, current_url)


def render_menu(items, current_url):
    def render_item(item, current_url, level=0):
        child_items = items.filter(parent=item)
        is_active = item.get_absolute_url() == current_url
        if is_active:
            expanded = True
        else:
            expanded = any(child.get_absolute_url() == current_url for child in child_items)

        html = f'<li class={"active" if is_active else ""}>'
        html += f'<a href="{item.get_absolute_url()}">{item.title}</a>'
        if child_items:
            html += '<ul>'
            for child in child_items:
                html += render_item(child, current_url, level + 1)
            html += '</ul>'
        html += '</li>'
        return html

    menu_html = '<ul>'
    top_level_items = items.filter(parent__isnull=True)
    for item in top_level_items:
        menu_html += render_item(item, current_url)
    menu_html += '</ul>'
    return menu_html