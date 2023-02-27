from django.shortcuts import redirect
from django import template
from .sel.sel_sub import get_user_token, url_for_token

register = template.Library()

@register.simple_tag(name='get_token')
def get_token():
	try:
		token = get_user_token(url_for_token)
	except:
		pass
	if token:
		responce = redirect('vk_parse_subject')
		responce['Location'] += f'?token={token}'
		return responce
	else:
		pass