from django import template

register = template.Library()


@register.filter()
def field_class(field, cls):
    attrs = field.field.widget.attrs

    if not attrs.get('class', None):
        attrs['class'] = ''

    attrs['class'] += ' ' + cls

    return field


@register.filter()
def placeholder(field, placeholder):
    attrs = field.field.widget.attrs
    attrs['placeholder'] = placeholder
    return field
