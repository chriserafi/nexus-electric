from rest_framework import serializers
from back_end.models import *
import datetime

# Base Serializer
class BaseDatasetSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        #fields_include = kwargs.pop('include', {})
        fields_exclude = kwargs.pop('exclude', {})
        super(BaseDatasetSerializer, self).__init__(*args, **kwargs)
        
        for field in fields_exclude:
            self.fields.pop(field)
    
    Source = serializers.ReadOnlyField(default="entso-e")
    Dataset = serializers.ReadOnlyField(default="Dataset")
    # Id = serializers.IntegerField(write_only=True)
    # EtityCreatedAt = serializers.DateTimeField(write_only=True)
    # EntityModifiedAt = serializers.DateTimeField(write_only=True)
    # ActionTaskID = serializers.IntegerField(write_only=True)
    # Status = serializers.CharField(write_only=True)
    # Year = serializers.IntegerField(write_only=True)
    # Month = serializers.IntegerField(write_only=True)
    # Day = serializers.IntegerField(write_only=True)
    # DateTime = serializers.DateTimeField(write_only=True, format="%Y-%m-%d %H:%M:%S.%f")
    DateTimeUTC = serializers.DateTimeField(read_only=True, source="DateTime", format="%Y-%m-%d %H:%M:%S.%f")
    # AreaName = serializers.CharField(write_only=True)
    # UpdateTime =  serializers.DateTimeField(write_only=True, format="%Y-%m-%d %H:%M:%S.%f")


    UpdateTimeUTC = serializers.DateTimeField(read_only=True, source="UpdateTime", format="%Y-%m-%d %H:%M:%S.%f")
    AreaTypeCode = serializers.SlugRelatedField(read_only=True, source="AreaTypeCodeId", slug_field="AreaTypeCodeText")
    MapCode = serializers.SlugRelatedField(read_only=True, source="MapCodeId", slug_field="MapCodeText")
    ResolutionCode = serializers.SlugRelatedField(read_only=True, source="ResolutionCodeId", slug_field="ResolutionCodeText")
    # RowHash = serializers.CharField(write_only=True)

# Actual Total Load
class ActualTotalLoadSerializer(BaseDatasetSerializer):
    ActualTotalLoadValue = serializers.FloatField(read_only=True,source="TotalLoadValue", required=False)
    ActualTotalLoadByDayValue = serializers.FloatField(read_only=True, required=False)
    ActualTotalLoadByMonthValue = serializers.FloatField(read_only=True, required=False)

    #AreaTypeCodeId = serializers.SlugRelatedField(source='AreaTypeCode',slug_field="Id")

    #AreaTypeCodeId = serializers.PrimaryKeyRelatedField(queryset=AreaTypeCode.objects.all())
    #MapCodeId = serializers.PrimaryKeyRelatedField(queryset=MapCode.objects.all())
    #AreaCodeId = serializers.PrimaryKeyRelatedField(queryset=AllocatedEICDetail.objects.all())
    #ResolutionCodeId = serializers.PrimaryKeyRelatedField(queryset=ResolutionCode.objects.all())

    
    def to_internal_value(self, data):
        tmpcreate = data['EntityCreatedAt']
        tmpmodified = data['EntityModifiedAt']
        tmpdatetime = data['DateTime']
        tmpupdatime = data['UpdateTime']
        data['AreaTypeCodeId'] = AreaTypeCode.objects.get(Id=data['AreaTypeCodeId'])
        data['MapCodeId'] = MapCode.objects.get(Id=data['MapCodeId'])
        data['AreaCodeId'] = AllocatedEICDetail.objects.get(Id=data['AreaCodeId'])
        data['ResolutionCodeId'] = ResolutionCode.objects.get(Id=data['ResolutionCodeId'])
        data['EntityCreatedAt'] = datetime.datetime.strptime((tmpcreate[:26]+tmpcreate[27:]).strip(), '%Y-%m-%d  %H:%M:%S.%f %z')
        data['EntityModifiedAt'] = datetime.datetime.strptime((tmpmodified[:26]+tmpmodified[27:]).strip(), '%Y-%m-%d  %H:%M:%S.%f %z')
        data['EntityModifiedAt'] = datetime.datetime.strptime((tmpdatetime[:26]+tmpdatetime[27:]).strip(), '%Y-%m-%d  %H:%M:%S.%f')
        data['EntityModifiedAt'] = datetime.datetime.strptime((tmpupdatime[:26]+tmpupdatime[27:]).strip(), '%Y-%m-%d  %H:%M:%S.%f')
        
        return data
    class Meta:
        model = ActualTotalLoad
        fields = ['Source', 'Dataset', 'AreaName', 'AreaTypeCode', 'MapCode', 
                'ResolutionCode','Year', 'Month', 'Day', 'DateTimeUTC', 'ActualTotalLoadValue', 
                'ActualTotalLoadByDayValue', 'ActualTotalLoadByMonthValue', 'UpdateTimeUTC']

# Day Ahead Total Load Forecast
class DayAheadTotalLoadForecastSerializer(BaseDatasetSerializer):
    DayAheadTotalLoadForecastValue = serializers.FloatField(read_only=True, source="TotalLoadValue")
    DayAheadTotalLoadForecastByDayValue = serializers.FloatField(read_only=True, source="TotalLoadValue")
    DayAheadTotalLoadForecastByMonthValue = serializers.FloatField(read_only=True, source="TotalLoadValue")
    
    class Meta:
        #model = DayAheadTotalLoadForecast
        fields = ['Source', 'Dataset', 'AreaName', 'AreaTypeCode', 
                'MapCode', 'ResolutionCode', 'Year', 'Month', 'Day', 
                'DateTimeUTC', 'DayAheadTotalLoadForecastValue', 'DayAheadTotalLoadForecastByDayValue', 
                'DayAheadTotalLoadForecastByMonthValue', 'UpdateTimeUTC']

# Actual vs Forecast
class ActualvsForecastSerializer(BaseDatasetSerializer):
    # DayAheadTotalLoadForecastValue = serializers.FloatField(read_only=True, source="TotalLoadValue")
    # ActualTotalLoadValue = serializers.FloatField(read_only=True, source="TotalLoadValue", required=False)

    class Meta:
        #model = ActualvsForecast
        fields = ['Source', 'Dataset', 'AreaName', 'AreaTypeCode', 
                'MapCode', 'ResolutionCode', 'Year', 'Month', 'Day', 
                'DateTimeUTC', 'DayAheadTotalLoadForecastValue', 'ActualTotalLoadValue']

# Aggregated Generation Per Type
class AggregatedGenerationPerTypeSerializer(BaseDatasetSerializer):
    ActualGenerationOutputValue = serializers.FloatField(read_only=True,source="ActualGenerationOutput")
    ProductionType = serializers.SlugRelatedField(read_only=True, source="ProductionTypeId", slug_field="ProductionTypeText")
    ActualGenerationOutputByDayValue = serializers.FloatField(read_only=True, required=False)
    ActualGenerationOutputByMonthValue = serializers.FloatField(read_only=True, required=False)
    
    class Meta:
        model = AggregatedGenerationPerType
        fields = ['Source', 'Dataset', 'AreaName', 'AreaTypeCode', 'MapCode', 
                'ResolutionCode', 'Year', 'Month', 'Day', 'DateTimeUTC', 
                'ProductionType', 'ActualGenerationOutputValue', 'ActualGenerationOutputByDayValue', 
                'ActualGenerationOutputByMonthValue', 'UpdateTimeUTC']


class MapCodeSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        #ret = super().to_internal_value(data)
        tmpcreate = data['EntityCreatedAt']
        tmpmodified = data['EntityModifiedAt']
        data['EntityCreatedAt'] = datetime.datetime.strptime((tmpcreate[:26]+tmpcreate[27:]).strip(), '%Y-%m-%d  %H:%M:%S.%f %z')
        data['EntityModifiedAt'] = datetime.datetime.strptime((tmpmodified[:26]+tmpmodified[27:]).strip(), '%Y-%m-%d  %H:%M:%S.%f %z')
        return data

    class Meta:
        model = MapCode
        fields = ['Id','EntityCreatedAt']
