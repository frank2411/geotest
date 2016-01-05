from django import template

register = template.Library()


@register.filter
def dollarify(value):
    return '${:,.2f}'.format(value)
