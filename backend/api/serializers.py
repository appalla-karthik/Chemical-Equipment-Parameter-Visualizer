from rest_framework import serializers
from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id','uploaded_at','original_filename','summary_json','pdf_report','file']
        read_only_fields = ['id','uploaded_at','summary_json','pdf_report']
