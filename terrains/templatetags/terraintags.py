from django import template

register = template.Library()


@register.filter
def dollarify(value):
    """Filter to convert int to dollar value"""
    return '${:,.2f}'.format(value)
