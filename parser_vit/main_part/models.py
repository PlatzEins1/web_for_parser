from django.db import models
from django.contrib.auth.models import User, UserManager
from django.urls import reverse

class app_user(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50, blank=True)
	last_name  = models.CharField(max_length=50, blank=True)
	token = models.CharField(max_length=300, blank=True, default='abscence of token')
	token_date = models.DateTimeField(blank=True, null=True, default='1970-01-01 04:00:02')

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name = 'Пользователь приложения'
		verbose_name_plural = 'Пользователи приложения'

class data_file (models.Model):
	file_name = models.CharField(max_length=100)
	file_created_at = models.DateTimeField(auto_now_add=True)
	data = models.FileField(upload_to='main_part/data_files_folder/')
	comment = models.TextField(blank=True, max_length=500)
	user =models.ForeignKey('app_user', on_delete=models.PROTECT, blank=True, null = True)
	is_public = models.BooleanField(blank=True, null = True)

	class Meta:
		verbose_name = 'Файл выгрузки'
		verbose_name_plural = 'Файлы выгрузки'

	def get_absolute_url(self):
		return reverse('vk_datafile_page', kwargs = {'datafile_pk': self.pk})

class user_intersection_file(models.Model):
	file_created_at = models.DateTimeField(auto_now_add=True)
	data = models.FileField(upload_to='main_part/data_files_folder/temporary_user_intersection_files/')