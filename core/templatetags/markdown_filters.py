# under the terms of the GNU General Public License v2
from django import template
import markdown as Markdown
from re import sub

register = template.Library()

@register.filter
def markdown(text):
    # We also format links automatically
    text = sub(
      r'(^|\s)(https?://[^\s"]+)(\s|$)',
      r'\1<a href="\2">\2</a>\3',
      text
    )
    return Markdown.markdown(text)
