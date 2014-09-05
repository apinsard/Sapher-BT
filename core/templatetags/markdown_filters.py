from django import template
import markdown as Markdown

register = template.Library()

@register.filter
def markdown(text):
    return Markdown.markdown(text)
