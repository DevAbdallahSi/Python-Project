from django import template

register = template.Library()

@register.filter
def filter_by_status(department, status):
    return department.dp_tickets.filter(status=status)