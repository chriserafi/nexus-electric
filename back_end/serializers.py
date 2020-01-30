from rest_framework import serializers
from back_end.models import *


class ActualTotalLoadSerializer(serializers.ModelSerializer):
    AreaTypeCode = serializers.SlugRelatedField(read_only=True, slug_field="AreaTypeCodeText")
    MapCode = serializers.SlugRelatedField(read_only=True, slug_field="MapCodeText")
    ResolutionCode = serializers.SlugRelatedField(read_only=True, slug_field="ResolutionCodeText")
    
    class Meta:
        model = ActualTotalLoad
        fields = '__all__'

class MapCodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = MapCode
		fields = '__all__'
