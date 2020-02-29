from django.urls import path, include
from back_end import views
from back_end.routers import ApiRouter, ApiRouterExtended, AdminRouter
from rest_framework.routers import DefaultRouter

router_1 = ApiRouter()
router_1.register(r'ActualTotalLoad', views.ActualTotalLoadViewSet)
router_1.register(r'DayAheadTotalLoadForecast',
                  views.DayAheadTotalLoadForecastViewSet)
router_1.register(r'ActualvsForecast', views.ActualvsForecastViewSet)


router_4 = DefaultRouter()
router_4.register(r'MapCode', views.MapCodeViewSet)

router_2 = ApiRouterExtended()
router_2.register(r'AggregatedGenerationPerType',
                  views.AggregatedGenerationPerTypeViewSet)

router_3 = AdminRouter()
router_3.register(r'Admin', views.AdminViewSet)

urlpatterns = [
    path('Login', views.sth),
    path('Logout', views.sth),
    path('', include(router_4.urls)),
    path('', include(router_1.urls)),
    path('', include(router_2.urls)),
    path('', include(router_3.urls)),
    path('HealthCheck', views.health_check),
    path('Reset', views.reset_database),
]
