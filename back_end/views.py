from django.shortcuts import render
from django.db.models import Sum
from rest_framework import viewsets
from back_end.models import *
from back_end.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from back_end.parsers import CSVParser
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

# Get-Only Template
class GetOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    http_method_names = ['get']

    def get_queryset(self, **kwargs):
        return self.queryset.objects.filter(**kwargs)

# ActualTotalLoadViewSet
class ActualTotalLoadViewSet(GetOnlyModelViewSet):
    queryset = ActualTotalLoad
    serializer_class = ActualTotalLoadSerializer

    def date(self, request, area_name, resolution, date):
        try:
            year, month, day = date.split('-')
        
            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day
            )
        except:
            return Response(None, status=400)
            
        serializer = self.get_serializer(queryset, many=True, exclude={'ActualTotalLoadByDayValue', 'ActualTotalLoadByMonthValue'})
        return Response(serializer.data)

    def month(self, request, area_name, resolution, date):
        try:
            year, month = date.split('-')

            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month
            ).annotate(
                ActualTotalLoadByDayValue = Sum('TotalLoadValue')
            )
        except:
            return Response(None, status=400)
            
        serializer = self.get_serializer(queryset, many=True, exclude={'ActualTotalLoadValue', 'ActualTotalLoadByMonthValue', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

    def year(self, request, area_name, resolution, date):
        try:
            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=date
            ).annotate(
                ActualTotalLoadByMonthValue = Sum('TotalLoadValue')
            )
        except:
            return Response(None, status=400)
            
        serializer = self.get_serializer(queryset, many=True, exclude={'ActualTotalLoadValue', 'ActualTotalLoadByDayValue', 'Day', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

# MapCodeViewSet
class MapCodeViewSet(viewsets.ModelViewSet):
    queryset = MapCode.objects.all()
    serializer_class = MapCodeSerializer
    @parser_classes([JSONParser])
    def create(self, request, format=None):
        file_obj = request.data['file']
        #ftype = request.data['ftype']
        #caption = request.data['caption']
        #f = open(file_obj.file, "r")

        #f = open(file_obj, "r")
        #line = file_obj.file.read().decode("utf-8")
        #line = line.replace('\0','')
        #f = open("temp.csv", 'r+') 
        #f.write(line)
        #file_obj.file.write(line)
        barser=CSVParser()
        datata = barser.parse(file_obj.file)
        rec_in_file = barser.total_records_in_file

        serializer = self.get_serializer(data=datata, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        totalRecords = MapCode.objects.all().count()
        rec_imported = rec_in_file
        d = {'totalRecordsInFile': rec_in_file, 'totalRecordsImported': rec_imported, 'totalRecordsInDatabase': totalRecords}
        return Response(d)

    # def post(self, request, *args, **kwargs):
    #	if request.DATA['batch']:
    #		json = request.DATA['batchData']
    #		stream = StringIO(json)
    #		data = JSONParser().parse(stream)
    #		request._data = data
    #	return super(CharacterDatumList, self).post(request, *args, **kwargs)

# DayAheadTotalLoadForecastViewSet
class DayAheadTotalLoadForecastViewSet(GetOnlyModelViewSet):
    queryset = DayAheadTotalLoadForecast
    serializer_class = DayAheadTotalLoadForecastSerializer

    def date(self, request, area_name, resolution, date):
        try:
            year, month, day = date.split('-')
        
            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day
            )
        except:
            return Response(None, status=400)
            
        serializer = self.get_serializer(queryset, many=True, exclude={'DayAheadTotalLoadForecastByDayValue', 'DayAheadTotalLoadForecastByMonthValue'})
        return Response(serializer.data)

    def month(self, request, area_name, resolution, date):
        try:
            year, month = date.split('-')

            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month
            ).annotate(
                ActualGenerationOutputByDayValue = Sum('ActualGenerationOutput')
            )
        except:
            return Response(None, status=400)
            
        serializer = self.get_serializer(queryset, many=True, exclude={'DayAheadTotalLoadForecastValue', 'DayAheadTotalLoadForecastByMonthValue', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

    def year(self, request, area_name, resolution, date):
        try:
            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=date
            ).annotate(
                ActualGenerationOutputByMonthValue = Sum('ActualGenerationOutput')
            )
        except:
            return Response(None, status=400)
            
        serializer = self.get_serializer(queryset, many=True, exclude={'DayAheadTotalLoadForecastValue', 'DayAheadTotalLoadForecastByDayValue', 'Day', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

# ActualvsForecastViewSet
class ActualvsForecastViewSet(GetOnlyModelViewSet):
    
    def join_dataset_results(area_name, resolution, date, exclude_forecast, actual_field):
        try:
            year, month, day = date.split('-')
        
            queryset_actual = ActualTotalLoad.object.filter(
                AreaName=area_name, 
                ResolutionCodeId__ResolutionCodeText=resolution, 
                Year=year, 
                Month=month, 
                Day=day
            )

            queryset_forecast = DayAheadTotalLoadForecast.object.filter(
                AreaName=area_name, 
                ResolutionCodeId__ResolutionCodeText=resolution, 
                Year=year, 
                Month=month, 
                Day=day
            )
        except:
            return Response(None, status=400)
        
        serializer_forecast = DayAheadTotalLoadForecastSerializer(queryset_forecast, exclude=exclude_forecast)
        serializer_actual = ActualTotalLoadSerializer(queryset_actual)

        return Response(serializer_forecast.data + serializer_actual.data[actual_field])
        

    def date(self, request, area_name, resolution, date):
        return join_dataset_results(area_name, resolution, date, {'DayAheadTotalLoadForecastByDayValue', 'DayAheadTotalLoadForecastByMonthValue', 'UpdateTimeUTC'}, 'ActualTotalLoadValue')

    def month(self, request, area_name, resolution, date):
        return join_dataset_results(area_name, resolution, date, {'DayAheadTotalLoadForecastValue', 'DayAheadTotalLoadForecastByMonthValue', 'UpdateTimeUTC'}, 'ActualTotalLoadByDayValue')

    def year(self, request, area_name, resolution, date):
        return join_dataset_results(area_name, resolution, date, {'DayAheadTotalLoadForecastValue', 'DayAheadTotalLoadForecastByDayValue', 'UpdateTimeUTC'}, 'ActualTotalLoadByMonthValue')

# AggregatedGenerationPerTypeViewSet
class AggregatedGenerationPerTypeViewSet(GetOnlyModelViewSet):
    queryset = AggregatedGenerationPerType
    serializer_class = AggregatedGenerationPerTypeSerializer

    def date(self, request, area_name, production_type, resolution, date):
        try:
            year, month, day = date.split('-')

            if (production_type == 'AllTypes'):
                queryset = self.get_queryset(
                    AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day
                )
            else:
                queryset = self.get_queryset(
                    AreaName=area_name, ProductionId__ProductionTypeText=production_type, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day
                )
        except:
            return Response(None, status=400)
            
        serializer = self.get_serializer(queryset, many=True, exclude={'AggregatedGenerationOutputByDayValue', 'AggregatedGenerationOutputByDayValue'})
        return Response(serializer.data)

    def month(self, request, area_name, production_type, resolution, date):
        try:
            year, month = date.split('-')

            if (production_type == 'AllTypes'):
                queryset = self.get_queryset(
                    AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day
                ).annotate(
                    AggregatedGenerationOutputByDayValue=Sum('ActualGenerationOutput')
                )
            else:
                queryset = self.get_queryset(
                    AreaName=area_name, ProductionId__ProductionTypeText=production_type, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day
                ).annotate(
                    AggregatedGenerationOutputByDayValue=Sum('ActualGenerationOutput')
                )
        except:
            return Response(None, status=400)
            
        serializer = self.get_serializer(queryset, many=True, exclude={'AggregatedGenerationOutputValue', 'AggregatedGenerationOutputByMonthValue', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

    def year(self, request, area_name, production_type, resolution, date):
        try:
            if (production_type == 'AllTypes'):
                queryset = self.get_queryset(
                    AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day
                ).annotate(
                    AggregatedGenerationOutputByMonthValue=Sum('ActualGenerationOutput')
                )
            else:
                queryset = self.get_queryset(
                    AreaName=area_name, ProductionId__ProductionTypeText=production_type, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day
                ).annotate(
                    AggregatedGenerationOutputByMonthValue=Sum('ActualGenerationOutput')
                )
        except:
            return Response(None, status=400)
            
        serializer = self.get_serializer(queryset, many=True, exclude={'AggregatedGenerationOutputValue', 'AggregatedGenerationOutputByDayValue', 'Day', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

# AdminViewSet
class AdminViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']

    queryset = MapCode.objects.all()

    def list(self, request):
        pass

    def retrieve(self, request, username):
        pass

    @action(methods=['post'], detail=False)
    def ActualTotalLoad(self, request):
        file_obj = request.data['file']
        barser=CSVParser()
        datata = barser.parse(file_obj.file)
        rec_in_file = barser.total_records_in_file
        serializer = ActualTotalLoadSerializer(data=datata, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        totalRecords = ActualTotalLoad.objects.all().count()
        rec_imported = rec_in_file
        d = {'totalRecordsInFile': rec_in_file, 'totalRecordsImported': rec_imported, 'totalRecordsInDatabase': totalRecords}
        return Response(d)

    @action(methods=['post'], detail=False)
    def AggregatedGenerationPerType(self, request):
        pass

    @action(methods=['post'], detail=False)
    def DayAheadTotalLoadForecast(self, request):
        pass

# DUMMY
@api_view(http_method_names=['GET'])
def sth(request):
    pass
