from rest_framework import serializers
from . models import *

class PBI_registerd_datas(serializers.ModelSerializer):
    class Meta:
        model=register_table
        fields='__all__'