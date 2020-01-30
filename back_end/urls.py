from django.urls import path, include
from back_end import views
from back_end.routers import ApiRouter, ApiRouterExtended, AdminRouter


router_1 = ApiRouter()
router_1.register(r'ActualTotalLoad', views.ActualTotalLoadViewSet)
router_1.register(r'DayAheadTotalLoadForecast', views.DayAheadTotalLoadForecastViewSet)
router_1.register(r'ActualvsForecast', views.ActualvsForecastViewSet)

router_2 = ApiRouterExtended()
router_2.register(r'AggregatedGenerationPerType', views.AggregatedGenerationPerTypeViewSet)

router_3 = AdminRouter()
router_3.register(r'Admin', views.AdminViewSet)

urlpatterns = [
	path('Login', views.sth),
	path('Logout', views.sth),
    path('', include(router_1.urls)),
    path('', include(router_2.urls)),
    path('', include(router_3.urls)),
    path('HealthCheck', views.sth),
    path('Reset', views.sth),
]
