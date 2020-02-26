from rest_framework import serializers
from back_end.models import *

class BaseDatasetSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(BaseDatasetSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            self.fields = fields
    
    Source = serializers.ReadOnlyField(default="entso-e")
    Dataset = serializers.ReadOnlyField(default="Dataset")
    AreaTypeCode = serializers.SlugRelatedField(read_only=True, source="AreaTypeCodeId", slug_field="AreaTypeCodeText")
    MapCode = serializers.SlugRelatedField(read_only=True, source="MapCodeId", slug_field="MapCodeText")
    ResolutionCode = serializers.SlugRelatedField(read_only=True, source="ResolutionCodeId", slug_field="ResolutionCodeText")

class ActualTotalLoadSerializer(BaseDatasetSerializer):
    DateTimeUTC = serializers.DateTimeField(read_only=True, source="DateTime", format="%Y-%m-%d %H:%M:%S.%f")
    UpdateTimeUTC = serializers.DateTimeField(read_only=True, source="UpdateTime", format="%Y-%m-%d %H:%M:%S.%f")
    ActualTotalLoadValue = serializers.FloatField(read_only=True, source="TotalLoadValue")

    class Meta:
        model = ActualTotalLoad
        fields = ['Source', 'Dataset', 'AreaName', 'AreaTypeCode', 'MapCode', 'ResolutionCode', 'Year', 'Month', 'Day', 'DateTimeUTC', 'ActualTotalLoadValue', 'UpdateTimeUTC']

class MapCodeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(MapCodeSerializer, self).__init__(many=many, *args, **kwargs)
    Source = serializers.ReadOnlyField(default="entso-e")
    Dataset = serializers.ReadOnlyField(default="MapCode")
    Id = serializers.IntegerField(write_only=True)
    EntityModifiedAt = serializers.CharField(write_only=True)
    MapCodeNote = serializers.CharField(write_only=True)
    class Meta:
        model = MapCode
        fields = ['Id', 'Source', 'Dataset', 'EntityCreatedAt',"EntityModifiedAt", 'MapCodeText', 'MapCodeNote']
        # extra_kwargs = {
        #     'Id' : {'write_only' : True},
        #     'EntityModifiedAt' : {'write_only' : True},
        #     'MapCodeNote' : {'write_only' : True}
        # }


class MapCodeSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = MapCode
        fields = ['Id', 'EntityCreatedAt',"EntityModifiedAt",'MapCodeText', 'MapCodeNote']