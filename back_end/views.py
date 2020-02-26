from django.shortcuts import render
from rest_framework import viewsets
from back_end.models import *
from back_end.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

#Get-Only Template
class GetOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
	http_method_names=['get']

#ActualTotalLoadViewSet
class ActualTotalLoadViewSet(GetOnlyModelViewSet):
	queryset = MapCode.objects.all()
	serializer_class = MapCodeSerializer

	def date(self, request, area_name, resolution, date):
		year, month, day = date.split('-')
		queryset = ActualTotalLoad.objects.filter(AreaName=area_name, ResolutionCodeId__ResolutionCodeText=resolution, Year=year, Month=month, Day=day)
		if not queryset:
			return Response({"No data"}, status=403)
		serializer = ActualTotalLoadSerializer(queryset, many=True, context = {
			'area_name' : area_name,
			'dataset' : "ActualTotalLoad",
			'date' : date
		})
		return Response(serializer.data)
	
	def month(self, request, area_name, resolution, date):
		return Response("Hallo World!")
	
	def year(self, request, area_name, resolution, date):
		return Response("Hallo World!")


#MapCodeViewSet
class MapCodeViewSet(viewsets.ModelViewSet):
	queryset = MapCode.objects.all()
	serializer_class = MapCodeSerializer


#DayAheadTotalLoadForecastViewSet
class DayAheadTotalLoadForecastViewSet(GetOnlyModelViewSet):
	queryset = MapCode.objects.all()
	serializer_class = MapCodeSerializer

	def date(self, request, area_name, resolution, date):
		return Response("Hallo World!")
	
	def month(self, request, area_name, resolution, date):
		return Response("Hallo World!")
	
	def year(self, request, area_name, resolution, date):
		return Response("Hallo World!")

#ActualvsForecastViewSet
class ActualvsForecastViewSet(GetOnlyModelViewSet):
	queryset = MapCode.objects.all()
	serializer_class = MapCodeSerializer

	def date(self, request, area_name, resolution, date):
		return Response("Hallo World!")
	
	def month(self, request, area_name, resolution, date):
		return Response("Hallo World!")
	
	def year(self, request, area_name, resolution, date):
		return Response("Hallo World!")

#AggregatedGenerationPerTypeViewSet
class AggregatedGenerationPerTypeViewSet(GetOnlyModelViewSet):
	queryset = MapCode.objects.all()
	serializer_class = MapCodeSerializer(queryset, many=True)

	def date(self, request, area_name, production_type, resolution, date):
		return Response("Hallo World!")
	
	def month(self, request, area_name, production_type, resolution, date):
		return Response("Hallo World!")
	
	def year(self, request, area_name, production_type, resolution, date):
		return Response("Hallo World!")

#AdminViewSet
class AdminViewSet(viewsets.ModelViewSet):
	http_method_names = ['get', 'post']
	
	queryset = MapCode.objects.all()
	
	def list(self, request):
		pass
	
	def retrieve(self, request, username):
		pass
		
	@action(methods=['post'], detail=False)
	def ActualTotalLoad(self, request):
		pass
	
	@action(methods=['post'], detail=False)
	def AggregatedGenerationPerType(self, request):
		pass
	
	@action(methods=['post'], detail=False)
	def DayAheadTotalLoadForecast(self, request):
		pass

#DUMMY
@api_view(http_method_names=['GET'])
def sth(request):
	pass
