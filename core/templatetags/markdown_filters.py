# Distributed under the terms of the GNU General Public License v2
from django import template
import markdown as Markdown

register = template.Library()

@register.filter
def markdown(text):
    return Markdown.markdown(text)
