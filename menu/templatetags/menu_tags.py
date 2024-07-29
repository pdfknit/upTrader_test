# menu_tags.py
from django import template
from django.utils.safestring import mark_safe
from menu.models import Menu, MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path
    menu = Menu.objects.get(name=menu_name)
    items = MenuItem.objects.filter(menu=menu).order_by('order')
    menu_html = render_menu(items, current_url)
    return mark_safe(menu_html)  # Mark the HTML as safe


def render_menu(items, current_url):
    def render_item(item, current_url):
        child_items = items.filter(parent=item)
        is_active = item.get_absolute_url() == current_url
        expanded = is_active or any(child.get_absolute_url() == current_url for child in child_items)

        classes = []
        if is_active:
            classes.append('active')
        if child_items:
            classes.append('has-children')
            if expanded:
                classes.append('expanded')

        class_attr = f'class="{" ".join(classes)}"' if classes else ''
        html = f'<li {class_attr}>'
        html += f'<a href="{item.get_absolute_url()}">{item.title}</a>'
        if child_items:
            html += '<ul>'
            for child in child_items:
                html += render_item(child, current_url)
            html += '</ul>'
        html += '</li>'
        return html

    menu_html = '<ul>'
    top_level_items = items.filter(parent__isnull=True)
    for item in top_level_items:
        menu_html += render_item(item, current_url)
    menu_html += '</ul>'
    return menu_html
