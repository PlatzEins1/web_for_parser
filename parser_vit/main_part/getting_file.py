import json
import requests
import time
from .vk_urls import url_get_members


access_token = "vk1.a.sqNszMOOdSHzehnpU1rK9KGA0x55c6lPw55XXEgKN9hj9CZ9dQxSIHYbzz5zgyrJhKkAVmyriAEQ2e50wJfIHsmKzdDggdpf3X6h7bUYaX8C5dtx_HwDMg9SmzTYLIJYFco8WmUHjOAG5B53WD0_QfIqMEpsgmQQO1_LxV6GZCULYqUhON-mg7NBDe724BRn"
v = "5.131"
id = ''
count = 1000
url_get_members
offset = 0




def first_req(access_token,count,url=url_get_members,offset=offset,id=id):
	param = {'group_id':f'{id}','sort':'id_asc','offset':f'{offset}','count':{count},'access_token':f'{access_token}','v':'5.131'}
	first_request = requests.get(url=url,params=param)
	src = first_request.json()
	print(src)
	record(src=src)
	all_users = src['response']['count']
	return all_users


def get_users(all_users,id=id):
	for i in range(1,count+1):
		offset = count*i
		param = {'group_id':f'{id}','sort':'id_asc','offset':f'{offset}','count':{count},'access_token':f'{access_token}','v':'5.131'}
		r = requests.get(url=url_get_members,params=param)
		time.sleep(3)
		src = r.json()
		print(src)
		record(src=src)
		if offset >= all_users:
			break
		return src

def record(src):
	with open(f'output_{id}.csv','a+') as outfile:
		json.dump(src['response']['items'],outfile)


with open('data_set.txt','r') as dataset_file:
	for item in dataset_file:
		f_item = item.replace('https://vk.com/','')
		f_item_1 = f_item.strip()
		try:
			f1 = first_req(access_token=access_token,count=1000,id=f_item_1)
		except:
			print("СТОП")
		try:
			get_users(all_users=f1,id=f_item_1)
		except:
			print("СТОП")
