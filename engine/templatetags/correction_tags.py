from django import template

register = template.Library()

# https://stackoverflow.com/questions/5755150/altering-one-query-parameter-in-a-url-django
@register.simple_tag(takes_context = True)
def word_replace(context, original, replacement):
	request = context['request'].GET.copy()
	request['query'] = request['query'].replace(original, replacement)
	return request.urlencode()
