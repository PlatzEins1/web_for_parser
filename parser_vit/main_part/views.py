import math
import json
import csv
import datetime
import io
import time
import pandas as pd
import os
import rest_framework
import requests
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .forms import user_login_form, vk_start_form_file_select, vk_start_form_url_input, vk_start_form_word_search, \
	vk_groups_options, vk_users_options, vk_parse_subject_form, parse_in_groups_main, parse_in_groups_optional, \
	vk_datafile_attrs, parse_user_suboptions, parse_in_users_main
from .models import data_file, user_intersection_file
from .sel_sub import get_user_token, url_for_token

from .serializers.serializers import DataFilesSerializer

@login_required()
def main(request):

	message = request.GET.get('message', '')
	match message:
		case '1':
			message = 'Пожалуйста попробуйте еще раз'

	help_text = 'Выбирается соцсеть, которую вы будете парсить, однако на данный момент, для парсинга доступен только "Вконтакте". После нажатия у вас откроется окно браузера, в него нужно будет ввести ваш логин и пароль от "Вконтакте"'

	context = {
		'message': message,
		'help_text': help_text,
	}

	return render(request, 'main_part/main.html', context)

def login_user(request):
	if request.method == 'POST':
		form = user_login_form(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('main_page')
	else:
		form = user_login_form()

	context = {
		'form': form,
		'title': 'Вход',
	}

	return render(request, 'main_part/login_page.html', context)

def user_logout(request): #выход текущего пользователя
	logout(request)
	return redirect(('login_page'))

@login_required()
def getting_access_token(request):  #Получение токена для вк
	try:
		token = get_user_token(request.user, url_for_token)
	except:
		print(Exception.with_traceback())

	if token:
		responce = redirect('vk_parse_subject')
		responce['Location'] += f'?token={token}'
		return responce
	else:
		responce = redirect('main_page')
		message = 1
		responce['Location'] += f'?message={message}'
		return responce

@login_required()
def vk_parse_subject(request): #Выбор что парсить: группы, пользователей
	if request.method == 'POST':
		form = vk_parse_subject_form()
		parsing = request.POST['parse_subject']
		match parsing:
			case 'group':
				responce = redirect('vk_group_start')
				token = request.GET.get('token', 'no token?') #дописать что делать при отсутствии токена
				responce['Location'] +=  f'?token={token}'
				return responce
			case 'user':
				responce = redirect('vk_user_start')
				token = request.GET.get('token', 'no token?')  # дописать что делать при отсутствии токена
				responce['Location'] += f'?token={token}'
				return responce
	else:
		form = vk_parse_subject_form()

	help_text = 'Выбирается объект парсинга: можно парсить либо информацию пользователя, либо информацию сообщества. На данный момент доступен только парсинг сообщества'

	context = {
		'form': form,
		'help_text': help_text
	}

	return render(request, 'main_part/vk_parse_subjects.html', context)

@login_required()
def vk_group_start(request): #выбор источника данных для сообщества



	if request.method == 'POST':

		token = request.GET.get('token')

	if request.method == 'POST' and 'object_vk_button' in request.POST: #поменять на помещение списка url-ов
		'''
		form_object = vk_start_form_file_select(request.POST)
		form_url = vk_start_form_url_input()
		form_word = vk_start_form_word_search()

		if form_object.is_valid():

			new_file = data_file(data = request.FILES['file'])
			new_file.user = request.user.app_user
			new_file.save()
			file = new_file.pk

			response = redirect('vk_adding_file')
			response['Location'] += f'?file={file}'
			return response
		'''
		file = request.FILES['file']
		decoded_file = file.read().decode('utf-8')

		io_string = io.StringIO(decoded_file)
		reader = csv.reader(io_string, delimiter=',')

		group_ids = ''
		for line in reader:
			if line[0] == '0':
				continue
			group_ids += line[0]
			group_ids += ','

		new_temp_name = str(request.user.app_user.pk) + '_' + \
		                str(datetime.datetime.now().timestamp()).split('.')[0] + '.txt'

		temp_path = os.path.join(os.path.dirname(__file__), 'data_files_folder',
		                         'temporary_groups_ids_files', new_temp_name)

		with open(temp_path, 'w', encoding='utf-8') as f:
			f.write(group_ids)

		response = redirect('parse_options_groups')
		response['Location'] += f'?token={token}&temp_file={new_temp_name}'
		return response



	elif request.method == 'POST' and 'url_vk_button' in request.POST:

		form_url = vk_start_form_url_input(request.POST)
		form_object = vk_start_form_file_select()
		form_word = vk_start_form_word_search()

		if form_url.is_valid():
			group = form_url.cleaned_data['url_to_object'] # возвращает введенную в форму ссылку
			group = group[15:]
			response = redirect('parse_options_groups')
			response['Location'] += f'?url={group}&token={token}'
			return response

	elif request.method == 'POST' and 'word_vk_button' in request.POST:

		form_word = vk_start_form_word_search(request.POST)
		form_object = vk_start_form_file_select()
		form_url = vk_start_form_url_input()

		pass


	else:
		form_object = vk_start_form_file_select()
		form_url = vk_start_form_url_input()
		form_word = vk_start_form_word_search()

	help_text = 'Выбирается источник данных: на данный момент можно либо вставить уже существующий файл с данными, либо вставить ссылку на сообщество, скопированную из адресной строки'

	context = {
		'form_object': form_object,
		'form_url': form_url,
		'form_word': form_word,
		'help_text': help_text,
	}

	return render(request, 'main_part/vk_group_start.html', context)

@login_required()
def vk_data_operations(request):
	return render(request, 'main_part/data_operations.html')

@login_required()
def parse_options(request):  #parameters from vk pages of users and groups 3
	need_users = request.GET.get('need_users')
	need_posts = request.GET.get('need_posts')
	
	if request.method == 'POST':
		form_group = vk_groups_options(request)

		if need_users:
			form_users = vk_users_options(request)

		if form_group.is_valid():

			if need_users and form_users  in locals() and form_users.is_valid():
				#data processing
				return redirect('data_operations')

			# data processing
			return redirect('data_operations')
	else:

		form_group = vk_groups_options()
		form_users = vk_users_options()

	context = {
		'form_group': form_group,
	}

	if need_users == 'True':
		context['form_users'] = form_users

	return render(request, 'main_part/parse_options.html', context)

@login_required()
def parse_options_groups(request): #парсинг групп
	if request.method == 'POST':

		group = request.GET.get('url', 0)
		token = request.GET.get('token')
		form = parse_in_groups_main(request.POST)
		temp_file = request.GET.get('temp_file', 0)

		if form.is_valid():

			option = request.POST['parse_option']

			match option:
				case 'main_info':
					response = redirect('vk_parse_groups_suboptions')
					response['Location'] += f'?url={group}&token={token}'
					return response
				case 'users':

					response = redirect('vk_parse_user_suboptions')
					response['Location'] += f'?url={group}&token={token}'
					if temp_file:
						response['Location'] +=f'&temp_file={temp_file}'
					return response

				case "posts":

					token=request.GET.get('token')

					if temp_file:

						temp_path = os.path.join(os.path.dirname(__file__), 'data_files_folder',
												 'temporary_groups_ids_files', temp_file)

						with open(temp_path, 'r', encoding='utf-8') as f:
							group_ids = f.readlines()[0][:-1].split(
								',')  # читается файл, берется первая строка, в которую и записаны данные, у нее отбрасывается последний знак-запятая, и генерируется массив идентификаторов

						#print(group_ids)

						data = {
							"items": {},
						}

						for id in group_ids:
							group_id = id.split('https://vk.com/')[1]
							print(group_id)
							params = {
								'domain': group_id,
								'count': 1,
								'offset': 0,
								'access_token': token,
								'v': '5.131',
							}

							request_for_counter = requests.get(
								'https://api.vk.com/method/wall.get?', params=params)

							params['count'] = 100

							#owner_id = request_for_counter.json()['response']['items'][0]['from_id']

							data['items'][str(group_id)]=[]
							print('каунтер', request_for_counter.json())
							#if 'error' in request_for_counter.json():
								#time.sleep(5)

							while 'error' in request_for_counter.json():
								time.sleep(5)
								request_for_counter = requests.get(
									'https://api.vk.com/method/wall.get?', params=params)

							counter = request_for_counter.json()['response']['count']


							for i in range(math.ceil(counter / 100)):
								print(counter)
								print("сеил", math.ceil(counter / 100))
								vk_request = requests.get(
									'https://api.vk.com/method/wall.get?', params=params)
								if 'error' in vk_request.json():
									print(vk_request.json())
									while vk_request.json()['error']['error_msg'] == 'Too many requests per second':
										time.sleep(5)
										vk_request = requests.get(
											'https://api.vk.com/method/wall.get?', params=params)
								data['items'][group_id].extend(vk_request.json()['response']['items'])
								params['offset'] = 100 * (i + 1)
								print(vk_request.json()['response']['items'], '\n')
								time.sleep(1)

							for post in data['items'][group_id]:
								print(post['owner_id'], post['id'])
								sub_params = {
									'owner_id': post['owner_id'],
									'access_token': token,
									'post_id': post['id'],
									'v': '5.131',
								}
								comments_request = requests.get('https://api.vk.com/method/wall.getComments?',
																params=sub_params)
								post['comments_list'] = comments_request.json()

						time.sleep(2)

						#print(data['items'])

						os.remove(temp_path)

						return create_datafile(request.user, data)

					if group:

						params = {
							'domain': request.GET.get('url'),  # + ',uvoleno',
							'count': 1,
							'offset': 0,
							'access_token': token,
							'v': '5.131',
						}

						request_for_counter = requests.get(
							'https://api.vk.com/method/wall.get?', params=params)

						group_id = request_for_counter.json()['response']['items'][0]['from_id']

						params['count'] = 100

						counter = request_for_counter.json()['response']['count']
						data = {
								"count": counter,
								"items": [],
						}
						for i in range(round(counter / 100)):
							vk_request = requests.get(
								'https://api.vk.com/method/wall.get?', params=params)

							data['items'].extend(vk_request.json()['response']['items'])
							params['offset'] = 100 * (i + 1)

						sub_params = {
							'owner_id': group_id,
							'access_token': token,
							'v': '5.131',
						}

						for post in data['items']:
							sub_params['post_id'] = post['id']
							comments_request = requests.get('https://api.vk.com/method/wall.getComments?', params=sub_params)
							post['comments_list'] = comments_request.json()

						return create_datafile(request.user, data)

	else:

		form = parse_in_groups_main()

	help_text = 'Выбирается что парсить из группы. На данный момент можно парсить основную информацию(название, дату создания, тематику и т.д.), пользователей и доступность их страницы, а также посты со стены сообщества и комментарии к ним'

	context = {
		'form': form,
		'page_title': 'Основные параметры',
		'help_text': help_text,
	}

	return render(request, 'main_part/vk_parse_options_groups.html', context)

@login_required()
def data_files_list(request, owner): #списки доступных пользователю датафайлов, параметр owner передается из шаблона и определяет показывать ли файлы пользователя или общедоступные файлы

	user = request.user.app_user

	context = {

	}

	match owner:
		case 1:
			context['files'] = data_file.objects.filter(user=user)
			context['help_text'] = 'Вы можете видеть созданные вами файлы данных'
		case 2:
			#condition = (Q(user=user) | Q(is_public = True))
			context['files'] =data_file.objects.filter(is_public = True).exclude(user=user)
			context['help_text'] = 'Вы можете видеть созданные другими пользователями файлы данных'

	return render(request, 'data_files_list.html', context)


def group_parce_options(request):
	pass

@login_required()
def vk_adding_file(request):

	if request.method =='POST':

		form = vk_datafile_attrs(request.POST)

		if form.is_valid():

			file_id = request.GET.get('file')

			file = data_file.objects.get(pk=file_id)

			file.file_name = form.cleaned_data['filename']
			file.comment = form.cleaned_data['comment']
			file.is_public = form.cleaned_data['is_public']

			file.save()

			response = redirect('vk_datafile_page')
			response['Location'] += f'?file={file_id}'
			return response

	else:
		form = vk_datafile_attrs()

	help_text = 'Вы задаете название файла в программе, комментарий к нему, в котором вы можете записать подробности(что, когда и из какой группы парсили, а также сделать файл публичным(с ним смогут работать другие пользователи)'

	context = {
		'form': form,
		'help_text': help_text,
	}

	return render(request, 'main_part/vk_datafile_attrs.html', context=context)

@login_required()
def vk_datafile_page(request):
	help_text = 'На данной странице вы можете работать с файлами данных. На данный момент доступно выявление пересечения аудитории различных сообществ.'

	context = {
		'help_text': help_text,
	}
	datafile_pk = request.GET.get('file', False)
	if datafile_pk:
		datafile = get_object_or_404(data_file, pk=datafile_pk)
		context['data_file'] = data_file
		context['prefixed_datafile_id'] = datafile_pk
		context['prefixed_datafile_name'] = datafile.file_name

	return render(request, 'main_part/vk_datafile_page.html', context)

def vk_available_datafiles(request): #later i will add used_datafiles list
	user = request.user.app_user
	condition = (Q(user=user) | Q(is_public=True))
	datafiles = data_file.objects.filter(condition)
	return JsonResponse({'datafiles': list(datafiles.values())})

def vk_get_additional_datafile(request, datafile_id):

	datafile = data_file.objects.filter(pk = datafile_id)
	return JsonResponse({'datafile': list(datafile.values())})

def vk_parse_groups_suboptions(request):
	if request.method == 'POST':
		form =  parse_in_groups_optional(request.POST)
		if form.is_valid():
			form_data = form.cleaned_data
			fields = ''
			for key in form_data:
				if form_data[key] == True:
					fields += key
					fields += ','

			params = {
				'group_ids': request.GET.get('url'),  # + ',uvoleno',
				'access_token': request.GET.get('token'),
				'fields': fields,
				'v': '5.131',
			}

			data = requests.get('https://api.vk.com/method/groups.getById?', params=params)

			data = data.json()['response']

			return create_datafile(request.user, data)

	else:
		form = parse_in_groups_optional()

	help_text = 'Выбираются дополнительные данные парсинга сообществ.'

	context = {
		'form': form,
		'page_title': 'Дополнительные параметры',
		'help_text': help_text,
	}
	return render(request, 'main_part/vk_parse_options_groups.html', context)

def vk_parse_user_suboptions(request):

	if request.method == 'POST':
		form =  parse_user_suboptions(request.POST)
		temp_file = request.GET.get('temp_file', '')
		data = {
			"items": [],
		}
		if form.is_valid():

			form_data = form.cleaned_data
			fields = ''
			for key in form_data:
				if form_data[key] == True:
					fields += key
					fields += ','
			if temp_file:

				temp_path = os.path.join(os.path.dirname(__file__), 'data_files_folder',
				                         'temporary_groups_ids_files', temp_file)

				with open(temp_path, 'r', encoding='utf-8') as f:
					group_ids = f.readlines()[0][:-1].split(',')

				for id in group_ids:
					#print(id[15:])
					params = {
						'group_id': id[15:],
						'count': 0,
						'offset': 0,
						'access_token': request.GET.get('token'),
						'v': '5.131',
					}

					request_for_counter = requests.get(
						'https://api.vk.com/method/groups.getMembers?', params=params)

					params['fields'] = fields

					params.pop('count')

					# print(request_for_counter)
					#print(request_for_counter.json())

					#print('каунтер', request_for_counter.json())
					if 'error' in request_for_counter.json():
						if request_for_counter.json()['error']['error_msg'] == 'One of the parameters specified was missing or invalid: group_id not domain' or request_for_counter.json()['error']['error_msg'] == 'Access denied: group hide members':
							continue
					counter = request_for_counter.json()['response']['count']
					# print(range(ceil(round(counter / 1000))))

					if counter < 1001:
						vk_request = requests.get(
							'https://api.vk.com/method/groups.getMembers?', params=params)
						data['items'].extend(vk_request.json()['response']['items'])

					else:
						for i in range(round(counter / 1000)):
							vk_request = requests.get(
								'https://api.vk.com/method/groups.getMembers?',
								params=params)
							#print(vk_request.json())
							data['items'].extend(vk_request.json()['response']['items'])
							params['offset'] = 1000 * (i + 1)
							time.sleep(1)

					time.sleep(1)

					if params['fields']:

						for item in data['items']:
							item.pop('first_name')
							item.pop('last_name')

					#print(type(data['items']))

				data['items'] = list(set(data['items']))
				return create_datafile(request.user, data)

			params = {
				'group_id': request.GET.get('url'),  # + ',uvoleno',
				'count': 0,
				'offset': 0,
				'access_token': request.GET.get('token'),
				'v': '5.131',
			}

			request_for_counter = requests.get('https://api.vk.com/method/groups.getMembers?', params=params)

			params['fields'] = fields

			params.pop('count')

			#print(request_for_counter)

			counter = request_for_counter.json()['response']['count']
			data["count"] = counter
			#print(range(ceil(round(counter / 1000))))

			if counter < 1001:
				vk_request = requests.get('https://api.vk.com/method/groups.getMembers?', params=params)
				data['items'].extend(vk_request.json()['response']['items'])

			else:
				for i in range(round(counter / 1000)):

					vk_request = requests.get('https://api.vk.com/method/groups.getMembers?', params=params)
					data['items'].extend(vk_request.json()['response']['items'])
					params['offset'] = 1000 * (i + 1)

			if params['fields']:

				for item in data['items']:
					item.pop('first_name')
					item.pop('last_name')

			'''
			current_user = str(request.user.app_user.id)
			
			new_id = str(data_file.objects.filter(user=current_user).last().id + 1)

			file_name = 'main_part/data_files_folder/' + current_user + '_' + new_id + '.json'

			with open(file_name, 'w', encoding='utf-8') as f:
				json.dump(data, f, ensure_ascii=False)

			file = data_file.objects.create(data=file_name, user=request.user.app_user)
			file = file.pk  # id созданного файла

			response = redirect('vk_adding_file')
			response['Location'] += f'?file={file}'
			return response
			'''

			return create_datafile(request.user, data)

	else:
		form = parse_user_suboptions()
	context = {
		'form': form,
		'page_title': 'Дополнительные параметры'
	}
	return render(request, 'main_part/vk_parse_options_groups.html', context)

def create_datafile(user, data):

	current_user = str(user.app_user.id)

	new_id = str(data_file.objects.filter(user=current_user).last().id + 1)

	file_name = 'main_part/data_files_folder/' + current_user + '_' + new_id + '.json'

	with open(file_name, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False)



	file = data_file.objects.create(data=file_name, user=user.app_user)
	file = file.pk  # id созданного файла

	response = redirect('vk_adding_file')
	response['Location'] += f'?file={file}'
	return response

def vk_audience_intersection(request, ids_string):

	ids_string = ids_string[:-1] #удаляем последнюю запятую

	id_list = ids_string.split(',')
	dataframe_list = []
	for id in id_list:
		file = data_file.objects.get(id=id)

		with open(file.data.path) as f:
			data = json.load(f)

			df = pd.DataFrame(data['items'])

			if 'id' in df.columns:
				df = df['id'].to_frame()
				df = df.rename(columns={'id': 0})

			else:

				df = df.rename(columns={0: 0})

			dataframe_list.append(df)
			df.index=list(df.index)

	df0 = dataframe_list[0]
	for df in dataframe_list:

		df0 = pd.merge(df0, df)

	last_file = user_intersection_file.objects.last()

	if last_file:
		last_file = last_file.pk

	else:
		last_file = 0

	new_name = str(last_file+1) + '.csv'

	user_intersection_file.objects.create(data=new_name)

	temp_path = os.path.join(os.path.dirname(__file__), 'data_files_folder', 'temporary_user_intersection_files', new_name)

	df0.to_csv(temp_path)

	return FileResponse(open(temp_path, 'rb'))

def about(request):
	context = {



	}
	return render(request, 'main_part/about.html', context=context)

def vk_user_start(request):

	if request.method == 'POST':

		token = request.GET.get('token')

	if request.method == 'POST' and 'object_vk_button' in request.POST:

		form_object = vk_start_form_file_select(request.POST)
		form_url = vk_start_form_url_input()
		form_word = vk_start_form_word_search()

		if form_object.is_valid():

			file = request.FILES['file']
			decoded_file = file.read().decode('utf-8')
			io_string = io.StringIO(decoded_file)
			reader = csv.reader(io_string, delimiter=',')
			user_ids = ''
			for line in reader:
				print(line)
				if len(line)>1:
					line.pop(0)
				if line[0] == '0':
					continue
				user_ids +=line[0]
				user_ids += ','
			#print(str(datetime.datetime.now().timestamp()).split('.')[0])


			new_temp_name = str(request.user.app_user.pk)+ '_' + str(datetime.datetime.now().timestamp()).split('.')[0] + '.txt'

			temp_path = os.path.join(os.path.dirname(__file__), 'data_files_folder',
			                 'temporary_users_ids_files', new_temp_name)

			with open(temp_path, 'w', encoding='utf-8') as f:
				f.write(user_ids)

			#print(temp_path)
			#pass
			response = redirect('parse_options_users')
			response['Location'] += f'?token={token}&temp_file={new_temp_name}'
			return response



	elif request.method == 'POST' and 'url_vk_button' in request.POST:

		form_url = vk_start_form_url_input(request.POST)
		form_object = vk_start_form_file_select()
		form_word = vk_start_form_word_search()

		if form_url.is_valid():
			group = form_url.cleaned_data['url_to_object'] # возвращает введенную в форму ссылку
			group = group[15:]
			response = redirect('parse_options_groups')
			response['Location'] += f'?url={group}&token={token}'
			return response

	elif request.method == 'POST' and 'word_vk_button' in request.POST:

		form_word = vk_start_form_word_search(request.POST)
		form_object = vk_start_form_file_select()
		form_url = vk_start_form_url_input()

		pass


	else:
		form_object = vk_start_form_file_select()
		form_url = vk_start_form_url_input()
		form_word = vk_start_form_word_search()

	help_text = ''

	context = {
		'form_object': form_object,
		'form_url': form_url,
		'form_word': form_word,
		'help_text': help_text,
	}

	return render(request, 'main_part/vk_user_start.html', context=context)

def parse_options_users(request):

	if request.method == 'POST':

		temp_file = request.GET.get('temp_file')
		token = request.GET.get('token')
		form = parse_in_users_main(request.POST)

		if form.is_valid():

			option = request.POST['parse_option']
			temp_path = os.path.join(os.path.dirname(__file__), 'data_files_folder',
			                         'temporary_users_ids_files', temp_file)

			with open(temp_path, 'r', encoding='utf-8') as f:
				user_ids = f.readlines()[0][:-1].split(',') #читается файл, берется первая строка, в которую и записаны данные, у нее отбрасывается последний знак-запятая, и генерируется массив идентификаторов


			match option:
				case 'subscribed_on':

					params = {
						'access_token': token,
						'extended': 1,
						'fields': 'name,description',
						'v': '5.131',
					}

					data = {
						'items':{

						}
					}

					for id in user_ids:
						params['user_id'] = id
						vk_request = requests.get('https://api.vk.com/method/users.getSubscriptions?', params=params)
						print(vk_request.json())
						if 'error' in vk_request.json():
							if vk_request.json()['error']['error_msg'] == 'This profile is private' or vk_request.json()['error']['error_msg'] == 'User was deleted or banned':
								continue
						data['items'].update({id: vk_request.json()['response']['items']})
						time.sleep(1)

					os.remove(temp_path)

					return create_datafile(request.user, data)



	else:

		form = parse_in_users_main()

	help_text = ''

	context = {
		'form': form,
		'page_title': 'Основные параметры',
		'help_text': help_text,
	}

	return render(request, 'main_part/vk_parse_options_users.html', context)

def Datafiles_list(request):
	if request.method == 'GET':
		user = request.user
		datafiles = data_file.objects.filter(user=user.app_user)
		serializer = DataFilesSerializer(datafiles, many=True)
		#print(dir(serializer.data))
		return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})


def geting_not_closed_users(request, datafile_id):
	datafile = data_file.objects.get(pk=datafile_id)
	with open(datafile.data.path) as data:
		users = json.load(data)
		#print(type(users))
		try:
			token = get_user_token(request.user, url_for_token)
		except:
			print(Exception.with_traceback())

		params = {
			'access_token': token,
			'v': '5.131',
			'fields': 'is_closed',
		}
		number_of_requests = len(users['items'])//1000
		if len(users['items'])%1000 != 0:
			number_of_requests += 1

		closed_pages = []

		for i in range(number_of_requests):

			if i == number_of_requests:

				start = i * 1000
				end = len(users['items']) - 1

				user_ids = ','.join(str(id) for id in users['items'][start:end])
				params['user_ids'] = user_ids

				request_vk = requests.get(
					'https://api.vk.com/method/users.get?', params=params)

				# print(request.json())

				for item in request_vk.json()['response']:
					if item['is_closed'] == True:
						closed_pages.append(item['id'])

				continue


			start = i * 1000
			end = (i+1) * 1000-1
			user_ids = ','.join(str(id) for id in users['items'][start:end])
			params['user_ids'] = user_ids

			request_vk = requests.get(
				'https://api.vk.com/method/users.get?', params=params)

			#print(request.json())

			for item in request_vk.json()['response']:
				if item['is_closed'] == True:
					closed_pages.append(item['id'])

		#print(closed_pages)

		for closed_page in closed_pages:
			users['items'].remove(closed_page)

		return create_datafile(request.user, users)