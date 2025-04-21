from rest_framework import serializers
from .models import registration

class Serialize_registers(serializers.ModelSerializer):
    class Meta:
        model = registration
        fields = ['id','email']
        fields = '__all__'