from rest_framework.routers import Route, DynamicRoute, SimpleRouter
from string import Template

def _f(url):
	return Template(url).substitute(LT = '[a-zA-Z]+', LTD = '[a-zA-Z0-9]+', YYYY = '\d\d\d\d', MM = '(0[1-9]|1[0-2])', DD = '([0-2]\d|3[0-1])')

class ApiRouter(SimpleRouter):
	routes = [
		Route(
			url=_f(r'^{prefix}/(?P<area_name>$LT)/(?P<resolution>$LTD)/date/(?P<date>$YYYY-$MM-$DD)$$'),
			mapping = {'get' : 'date'},
			name='{basename}-date',
			detail=False,
			initkwargs={}
		),
		
		Route(
			url=_f(r'^{prefix}/(?P<area_name>$LT)/(?P<resolution>$LTD)/month/(?P<date>$YYYY-$MM)$$'),
			mapping = {'get' : 'month'},
			name='{basename}-month',
			detail=False,
			initkwargs={}
		),
		
		Route(
			url=_f(r'^{prefix}/(?P<area_name>$LT)/(?P<resolution>$LTD)/year/(?P<date>$YYYY)$$'),
			mapping = {'get' : 'year'},
			name='{basename}-year',
			detail=False,
			initkwargs={}
		)
	]

class ApiRouterExtended(SimpleRouter):
	routes = [
		Route(
			url=_f(r'^{prefix}/(?P<area_name>$LT)/(?P<production_type>$LT)/(?P<resolution>$LTD)/date/(?P<date>$YYYY-$MM-$DD)$$'),
			mapping = {'get' : 'date'},
			name='{basename}-date',
			detail=False,
			initkwargs={}
		),
		
		Route(
			url=_f(r'^{prefix}/(?P<area_name>$LT)/(?P<production_type>$LT)/(?P<resolution>$LTD)/month/(?P<date>$YYYY-$MM)$$'),
			mapping = {'get' : 'month'},
			name='{basename}-month',
			detail=False,
			initkwargs={}
		),
		
		Route(
			url=_f(r'^{prefix}/(?P<area_name>$LT)/(?P<production_type>$LT)/(?P<resolution>$LTD)/year/(?P<date>$YYYY)$$'),
			mapping = {'get' : 'year'},
			name='{basename}-year',
			detail=False,
			initkwargs={}
		)
	]

class AdminRouter(SimpleRouter):
	routes = [
		Route(
			url=r'^{prefix}/users$',
			mapping={'get' : 'list'},
			name='{basename}-list',
			detail=False,
			initkwargs={'suffix': 'List'}
		),
		
		Route(
			url=r'^{prefix}/users/(?P<username>[a-zA-Z]+)$',
			mapping={'get' : 'retrieve'},
			name='{basename}-detail',
			detail=True,
			initkwargs={'suffix': 'List'}
		),
		
		DynamicRoute(
			url=r'^{prefix}/{url_path}$',
			name='{basename}-{url_name}',
			detail=False,
			initkwargs={}
		)
	]
