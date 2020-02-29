from django.shortcuts import render
from django.db.models import Sum
from django.db import connection, transaction
from django.conf import settings
from django.db.utils import OperationalError
from rest_framework import viewsets
from back_end.models import *
from back_end.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from back_end.parsers import CSVParser
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from back_end.inserters import importer

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
            ).order_by(
                'DateTime'
            )
        except:
            return Response(None, status=400)

        serializer = self.get_serializer(queryset, many=True, exclude={
                                         'ActualTotalLoadByDayValue', 'ActualTotalLoadByMonthValue'})
        return Response(serializer.data)

    def month(self, request, area_name, resolution, date):
        try:
            year, month = date.split('-')

            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month
            ).values(
                'AreaName', 'AreaTypeCodeId__AreaTypeCodeText', 'MapCodeId__MapCodeText', 'ResolutionCodeId__ResolutionCodeText', 'Year', 'Month', 'Day'
            ).annotate(
                ActualTotalLoadByDayValue=Sum('TotalLoadValue')
            ).order_by(
                'Year', 'Month', 'Day'
            )
        except:
            return Response(None, status=400)

        serializer = self.get_serializer(queryset, many=True, exclude={
                                         'ActualTotalLoadValue', 'ActualTotalLoadByMonthValue', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

    def year(self, request, area_name, resolution, date):
        try:
            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=date
            ).values(
                'AreaName', 'AreaTypeCodeId__AreaTypeCodeText', 'MapCodeId__MapCodeText', 'ResolutionCodeId__ResolutionCodeText', 'Year', 'Month'
            ).annotate(
                ActualTotalLoadByMonthValue=Sum('TotalLoadValue')
            )
        except:
            return Response(None, status=400)

        serializer = self.get_serializer(queryset, many=True, exclude={
                                         'ActualTotalLoadValue', 'ActualTotalLoadByDayValue', 'Day', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

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
                ).order_by(
                    'DateTime'
                )
            else:
                queryset = self.get_queryset(
                    AreaName=area_name, ProductionId__ProductionTypeText=production_type, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day
                ).order_by(
                    'DateTime'
                )
        except:
            return Response(None, status=400)

        serializer = self.get_serializer(queryset, many=True, exclude={
                                         'ActualGenerationOutputByDayValue', 'ActualGenerationOutputByMonthValue'})
        return Response(serializer.data)

    def month(self, request, area_name, production_type, resolution, date):
        try:
            year, month = date.split('-')

            if (production_type == 'AllTypes'):
                queryset = self.get_queryset(
                    AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month
                ).values(
                    'AreaName', 'AreaTypeCodeId__AreaTypeCodeText', 'MapCodeId__MapCodeText', 'ResolutionCodeId__ResolutionCodeText', 'Year', 'Month', 'Day'
                ).annotate(
                    AggregatedGenerationOutputByDayValue=Sum(
                        'ActualGenerationOutput')
                ).order_by(
                    'Year', 'Month', 'Day'
                )
            else:
                queryset = self.get_queryset(
                    AreaName=area_name, ProductionId__ProductionTypeText=production_type, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month
                ).values(
                    'AreaName', 'AreaTypeCodeId__AreaTypeCodeText', 'MapCodeId__MapCodeText', 'ResolutionCodeId__ResolutionCodeText', 'ProductionTypeId__ProductionCodeText', 'Year', 'Month', 'Day'
                ).annotate(
                    AggregatedGenerationOutputByDayValue=Sum(
                        'ActualGenerationOutput')
                ).order_by(
                    'Year', 'Month', 'Day'
                )
        except:
            return Response(None, status=400)

        serializer = self.get_serializer(queryset, many=True, exclude={
                                         'ActualGenerationOutputValue', 'ActualGenerationOutputByMonthValue', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

    def year(self, request, area_name, production_type, resolution, date):
        try:
            if (production_type == 'AllTypes'):
                queryset = self.get_queryset(
                    AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=date
                ).values(
                    'AreaName', 'AreaTypeCodeId__AreaTypeCodeText', 'MapCodeId__MapCodeText', 'ResolutionCodeId__ResolutionCodeText', 'Year', 'Month'
                ).annotate(
                    AggregatedGenerationOutputByMonthValue=Sum(
                        'ActualGenerationOutput')
                )
            else:
                queryset = self.get_queryset(
                    AreaName=area_name, ProductionId__ProductionTypeText=production_type, ResolutionCodeId__ResolutionCodeText=resolution, Year=date
                ).values(
                    'AreaName', 'AreaTypeCodeId__AreaTypeCodeText', 'MapCodeId__MapCodeText', 'ResolutionCodeId__ResolutionCodeText', 'ProductionTypeId__ProductionCodeText', 'Year', 'Month'
                ).annotate(
                    AggregatedGenerationOutputByMonthValue=Sum(
                        'ActualGenerationOutput')
                )
        except:
            return Response(None, status=400)

        serializer = self.get_serializer(queryset, many=True, exclude={
                                         'ActualGenerationOutputValue', 'ActualGenerationOutputByDayValue', 'Day', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

# DayAheadTotalLoadForecastViewSet
class DayAheadTotalLoadForecastViewSet(GetOnlyModelViewSet):
    queryset = DayAheadTotalLoadForecast
    serializer_class = DayAheadTotalLoadForecastSerializer

    def date(self, request, area_name, resolution, date):
        try:
            year, month, day = date.split('-')

            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day
            ).order_by(
                'DateTime'
            )
        except:
            return Response(None, status=400)

        serializer = self.get_serializer(queryset, many=True, exclude={
                                         'DayAheadTotalLoadForecastByDayValue', 'DayAheadTotalLoadForecastByMonthValue'})
        return Response(serializer.data)

    def month(self, request, area_name, resolution, date):
        try:
            year, month = date.split('-')

            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month
            ).values(
                'AreaName', 'AreaTypeCodeId__AreaTypeCodeText', 'MapCodeId__MapCodeText', 'ResolutionCodeId__ResolutionCodeText', 'Year', 'Month', 'Day'
            ).annotate(
                DayAheadTotalLoadForecastByDayValue=Sum('TotalLoadValue')
            ).order_by(
                'Year', 'Month', 'Day'
            )
        except:
            return Response(None, status=400)

        serializer = self.get_serializer(queryset, many=True, exclude={
                                         'DayAheadTotalLoadForecastValue', 'DayAheadTotalLoadForecastByMonthValue', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

    def year(self, request, area_name, resolution, date):
        try:
            queryset = self.get_queryset(
                AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=date
            ).values(
                'AreaName', 'AreaTypeCodeId__AreaTypeCodeText', 'MapCodeId__MapCodeText', 'ResolutionCodeId__ResolutionCodeText', 'Year', 'Month'
            ).annotate(
                DayAheadTotalLoadForecastByMonthValue=Sum('TotalLoadValue')
            )
        except:
            return Response(None, status=400)

        serializer = self.get_serializer(queryset, many=True, exclude={
                                         'DayAheadTotalLoadForecastValue', 'DayAheadTotalLoadForecastByDayValue', 'Day', 'DateTimeUTC', 'UpdateTimeUTC'})
        return Response(serializer.data)

# ActualvsForecastViewSet
class ActualvsForecastViewSet(viewsets.ViewSet):

    def join_dataset_results(self, area_name, resolution, date, exclude_forecast, actual_field):
        queryset = ActualvsForecast.objects.raw(
            """  
                SELECT a.AreaName, a.AreaTypeCodeId, a.MapCodeId, a.ResolutionCodeId, a.Year, a.Month, a.Day, b.TotalLoadValue as ForecastValue, a.TotalLoadValue
                FROM `back_end_actualtotalload` as a
                INNER JOIN `back_end_dayaheadtotalloadforecast` as b
                ON a.DateTime = b.DateTime AND a.ResolutionCodeId = b.ResolutionCodeId AND a.AreaCodeId = b.AreaCodeId AND a.AreaTypeCodeId = b.AreaTypeCodeId AND a.MapCodeId = b.MapCodeId 
            """
        ).filter(
            AreaName=area_name,
            ResolutionCodeId__ResolutionCodeText=resolution,
            Year=year,
            Month=month,
            Day=day
        )

        serializer = ActualvsForecast(queryset, many=True)

        return Response(serializer.data)

    def date(self, request, area_name, resolution, date):

        # year, month, day = date.split('-')

        # queryset_actual = ActualTotalLoad.objects.filter(
        #     AreaName=area_name,
        #     ResolutionCodeId__ResolutionCodeText=resolution,
        #     Year=year,
        #     Month=month,
        #     Day=day
        # )

        # queryset_forecast = DayAheadTotalLoadForecast.objects.filter(
        #     AreaName=area_name,
        #     ResolutionCodeId__ResolutionCodeText=resolution,
        #     Year=year,
        #     Month=month,
        #     Day=day
        # )

        # queryset = queryset_actual.union(queryset_forecast)

        # #serializer = ActualvsForecastSerializer(queryset, many=True)

        # return Response(queryset.values())
        cursor = connection.cursor()
        cursor.execute(
            """  
                SELECT a.AreaName, c.AreaTypeCodeText, d.MapCodeText, e.ResolutionCodeText, a.Year, a.Month, a.Day, b.TotalLoadValue as ForecastValue, a.TotalLoadValue
                FROM `back_end_actualtotalload` as a
                INNER JOIN `back_end_dayaheadtotalloadforecast` as b
                ON a.DateTime = b.DateTime AND a.ResolutionCodeId = b.ResolutionCodeId AND a.AreaCodeId = b.AreaCodeId AND a.AreaTypeCodeId = b.AreaTypeCodeId AND a.MapCodeId = b.MapCodeId
                INNER JOIN `back_end_areatypecode` as c
                ON a.AreaTypeCodeId = c.Id
                INNER JOIN `back_end_mapcode` as d
                ON a.MapCodeId = d.Id
                INNER JOIN `back_end_resolutioncode` as e
                ON a.ResolutionCodeId = e.Id
            """
        )
        columns = [col[0] for col in cursor.description]
        res = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return Response(res)

    def month(self, request, area_name, resolution, date):
        return self.join_dataset_results(area_name, resolution, date, {'DayAheadTotalLoadForecastValue', 'DayAheadTotalLoadForecastByMonthValue', 'UpdateTimeUTC'}, 'ActualTotalLoadByDayValue')

    def year(self, request, area_name, resolution, date):
        return self.join_dataset_results(area_name, resolution, date, {'DayAheadTotalLoadForecastValue', 'DayAheadTotalLoadForecastByDayValue', 'UpdateTimeUTC'}, 'ActualTotalLoadByMonthValue')

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
        # f.write(line)
        # file_obj.file.write(line)
        barser = CSVParser()
        datata = barser.parse(file_obj.file)
        rec_in_file = barser.total_records_in_file

        serializer = self.get_serializer(data=datata, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        totalRecords = MapCode.objects.all().count()
        rec_imported = rec_in_file
        d = {'totalRecordsInFile': rec_in_file, 'totalRecordsImported': rec_imported,
             'totalRecordsInDatabase': totalRecords}
        return Response(d)

    # def post(self, request, *args, **kwargs):
    #	if request.DATA['batch']:
    #		json = request.DATA['batchData']
    #		stream = StringIO(json)
    #		data = JSONParser().parse(stream)
    #		request._data = data
    #	return super(CharacterDatumList, self).post(request, *args, **kwargs)

# AdminViewSet
class AdminViewSet(viewsets.ViewSet):
    http_method_names = ['get', 'post']

    def create(self, request):
        return Response({"METHOD": "CREATE"})

    def retrieve(self, request, username):
        return Response({"METHOD": "RETRIEVE"})

    def update(self, request, username):
        return Response({"METHOD": "UPDATE"})

    @action(methods=['post'], detail=False)
    def ActualTotalLoad(self, request):
        file_obj = request.data['file']
        barser = CSVParser()
        datata = barser.parse(file_obj.file)
        rec_in_file = barser.total_records_in_file
        rec_imported = importer(datata, 'back_end_actualtotalload')

        #serializer = ActualTotalLoadSerializer(data=datata, many=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        totalRecords = ActualTotalLoad.objects.all().count()
        #rec_imported = rec_in_file
        d = {'totalRecordsInFile': rec_in_file, 'totalRecordsImported': rec_imported,
             'totalRecordsInDatabase': totalRecords}
        return Response(d)

    @action(methods=['post'], detail=False)
    def AggregatedGenerationPerType(self, request):
        file_obj = request.data['file']
        barser = CSVParser()
        datata = barser.parse(file_obj.file)
        rec_in_file = barser.total_records_in_file
        rec_imported = importer(datata, 'back_end_aggregatedgenerationpertype')
        #serializer = AggregatedGenerationPerTypeSerializer(data=datata, many=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        totalRecords = AggregatedGenerationPerType.objects.all().count()
        #rec_imported = rec_in_file
        d = {'totalRecordsInFile': rec_in_file, 'totalRecordsImported': rec_imported,
             'totalRecordsInDatabase': totalRecords}
        return Response(d)

    @action(methods=['post'], detail=False)
    def DayAheadTotalLoadForecast(self, request):
        file_obj = request.data['file']
        barser = CSVParser()
        datata = barser.parse(file_obj.file)
        rec_in_file = barser.total_records_in_file
        rec_imported = importer(datata, 'back_end_dayaheadtotalloadforecast')
        #serializer = DayAheadTotalLoadForecastSerializer(data=datata, many=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        totalRecords = DayAheadTotalLoadForecast.objects.all().count()
        #rec_imported = rec_in_file
        d = {'totalRecordsInFile': rec_in_file, 'totalRecordsImported': rec_imported,
             'totalRecordsInDatabase': totalRecords}
        return Response(d)


# DUMMY
@api_view(http_method_names=['GET'])
def sth(request):
    pass


@api_view(http_method_names=['POST'])
def reset_database(request):
    return Response(None)
    # try:
    #     with transaction.atomic():
    #         ActualTotalLoad.objects.all().delete()
    #         AggregatedGenerationPerType.objects.all().delete()
    #         DayAheadTotalLoadForecast.objects.all().delete()
    #         return Response({"status" : "OK"})
    # except:
    #     return Response(None)


@api_view(http_method_names=['GET'])
def health_check(request):
    try:
        connection.cursor()
    except OperationalError:
        return Response(None)
    else:
        return Response({"status": "OK"})
