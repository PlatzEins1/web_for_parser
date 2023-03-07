from django.urls import path
from .views import main, login_user, vk_group_start, vk_data_operations, parse_options, parse_options_groups, user_logout, data_files_list,  \
	getting_access_token, vk_parse_subject, group_parce_options, vk_adding_file, vk_datafile_page, vk_available_datafiles, vk_get_additional_datafile, \
	vk_parse_groups_suboptions, vk_parse_user_suboptions, vk_audience_intersection, about, vk_user_start, parse_options_users, geting_not_closed_users

urlpatterns = [
	path('', main, name = 'main_page'),
	path('login', login_user, name = 'login_page'),
	path('logout', user_logout, name = 'logout'),
	path('vk_group_start', vk_group_start, name = 'vk_group_start'),
	path('data_operations', vk_data_operations, name = 'vk_data_operations'),
	path('parse_options', parse_options, name = 'parse_options'),
	path('parse_options_groups', parse_options_groups, name = 'parse_options_groups'),
	path('group_parce_options', group_parce_options, name = 'group_parce_options'),
	path('data_files_list/<int:owner>',data_files_list, name = 'data_files_list'),
	path('getting_access_token', getting_access_token, name = 'getting_access_token'),
	path('vk_parse_subject', vk_parse_subject, name = 'vk_parse_subject'),
	path('vk_adding_file', vk_adding_file, name = 'vk_adding_file'),
	path('vk_datafile_page', vk_datafile_page, name = 'vk_datafile_page'),
	path('vk_parse_groups_suboptions', vk_parse_groups_suboptions, name='vk_parse_groups_suboptions'),
	path('vk_available_datafiles', vk_available_datafiles, name = 'vk_available_datafiles'),
	path('vk_get_additional_datafile/<int:datafile_id>', vk_get_additional_datafile, name = 'vk_get_additional_datafile'),
	path('vk_parse_user_suboptions', vk_parse_user_suboptions, name='vk_parse_user_suboptions'),
	path('vk_audience_intersection/<str:ids_string>', vk_audience_intersection, name='vk_audience_intersection'),
	path('about', about, name='about'),
	path('vk_user_start', vk_user_start, name='vk_user_start'),
	path('parse_options_users', parse_options_users, name='parse_options_users'),
	path('geting_not_closed_users/<int:datafile_id>', geting_not_closed_users, name='geting_not_closed_users'),


	#path('donations', name = 'donations_page'),
]

