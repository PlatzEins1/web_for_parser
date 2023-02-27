from django import forms
from django.contrib.auth.models import User

#from. models import
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class user_login_form(AuthenticationForm):
	username = forms.CharField(max_length=40, strip=True, label="Имя пользователя", widget=forms.TextInput(), help_text='Длина логина не должна превышать сорока символов')
	password = forms.CharField(max_length=40, strip=True, label="Имя пользователя", widget=forms.TextInput(), help_text='Длина пароля не должна превышать сорока символов')

class vk_start_form_file_select(forms.Form):
	file = forms.FileField(label='Файл с данными', required=None, widget = forms.FileInput())

class vk_start_form_url_input(forms.Form):
	url_to_object = forms.CharField(label='Ссылка на сообщество', required=None, widget = forms.URLInput())

class vk_start_form_word_search(forms.Form):
	word_for_search = forms.CharField(label='Слово для поиска', required=None, widget = forms.TextInput())

class vk_posts_and_users(forms.Form):
	get_posts = forms.BooleanField(label='Получить посты со стены сообщества', widget=forms.CheckboxInput, required=None)
	get_users = forms.BooleanField(label='Получить пользователей сообщества', widget=forms.CheckboxInput, required=None)

class vk_parse_subject_form(forms.Form):
	subject_choices = [
		('group', 'Группы'),
		('user', 'Пользователей'),
	]
	parse_subject = forms.CharField(label = 'Что парсить?', widget=forms.RadioSelect(choices=subject_choices))

class vk_groups_options(forms.Form):

	activities = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	city = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	country = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	domain = forms.BooleanField(widget=forms.CheckboxInput, required=None)

	'''
	activity = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	addresses = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	age_limits = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	ban_info = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	city = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	contacts = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	counters = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	country = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	cover = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	description = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	fixed_post = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	is_favorite = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	is_hidden_from_feed = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	is_message_blocked = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	links = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	main_album_id = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	main_section = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	member_status = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	members_count = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	place = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	public_date_label = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	site = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	start_date = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	finish_date = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	status = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	trending = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	verified = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	wall = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	'''


class vk_users_options(forms.Form):
	activities = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	bdate = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	books = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	city = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	country = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	domain = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	education = forms.BooleanField(widget=forms.CheckboxInput, required=None)
	military = forms.BooleanField(widget=forms.CheckboxInput, required=None)

'''
class parse_in_groups_main(forms.Form):
	parse_main_info = forms.BooleanField(widget=forms.CheckboxInput, required=None, label = 'Необходимо парсить основную информацию о группе')
	parse_users = forms.BooleanField(widget=forms.CheckboxInput, required=None, label = 'Необходимо парсить пользователей')
	parse_posts = forms.BooleanField(widget=forms.CheckboxInput, required=None, label = 'Необходимо парсить посты')
	parse_outer = forms.BooleanField(widget=forms.CheckboxInput, required=None, label = 'Необходимо парсить внешние группы')
	parse_group_info  = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить доп. информацию группы')
'''

class parse_in_groups_main(forms.Form):
	subject_choices = [
		('main_info', 'Основную информацию'),
		('users', 'Пользователей'),
		('posts', 'Посты и комментарии'),
		('outer', 'Внешние ссылки'),
		('group_info', 'Доп.информацию'),
	]
	parse_option = forms.CharField(label = 'Что парсить?', widget=forms.RadioSelect(choices=subject_choices))

class parse_in_groups_optional(forms.Form):
	#name  = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить наименование группы')
	screm_name = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить отображаемое название')
	is_closed = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить закрытость сообществ')
	deactivated = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить доступность сообщества')
	type = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить тип сообщества')
	activity = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить тематику сообщества')
	age_limits = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить возрастные ограничения')
	city = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить город, указанный в информации о сообществе')
	country = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить страну, указанную в информации о сообществе')
	links = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить страну, указанную в информации о сообществе')
	members_count = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить количество подписчиков')
	verified = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить верифицированность сообщества')
	wall = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить стену')

class vk_datafile_attrs(forms.Form):
	filename = forms.CharField(max_length=100, label='Наименование файла', widget=forms.TextInput(), help_text='длина не должна превышать 100 символов', required=True)
	comment = forms.CharField(max_length=500, label='Комментарий к файлу', widget=forms.Textarea(), help_text='длина не должна превышать 500 символов')
	is_public = forms.BooleanField(widget=forms.CheckboxInput(), required=None, label='Публичный файл', help_text='публичные файлы доступны другим пользователям')

class parse_user_suboptions(forms.Form):
	can_write_private_message = forms.BooleanField(widget=forms.CheckboxInput, required=None, label='Необходимо парсить доступность страницы')
class parse_in_users_main(forms.Form):
	subject_choices = [
		('subscribed_on', 'Сообщества, на которые подписаны пользователи'),
	]
	parse_option = forms.CharField(label='Что парсить?', widget=forms.RadioSelect(choices=subject_choices))