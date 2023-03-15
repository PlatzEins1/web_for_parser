from rest_framework import serializers
from ..models import data_file

class DataFilesSerializer(serializers.ModelSerializer):
	data = serializers.CharField(source='data.path')
	class Meta:
		model = data_file
		fields = '__all__'