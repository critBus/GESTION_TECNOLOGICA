from django import template
import re
register = template.Library()

def numeroConComa(value):
    return str(value).replace(",",".")
register.filter('numeroConComa', numeroConComa)