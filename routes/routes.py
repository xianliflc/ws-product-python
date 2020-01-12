from flask_restful import Api
from routes.daily_stats import StatsDailyResource
from routes.hourly_stats import StatsHourlyResource
from routes.poi import PoiResource
from routes.hourly_events import EventsHourlyResource
from routes.daily_events import EventsDailyResource

def init_routes(api_app):
    api_rest = Api(api_app)

    api_rest.add_resource(StatsDailyResource, '/stats/daily')
    api_rest.add_resource(StatsHourlyResource, '/stats/hourly')
    api_rest.add_resource(PoiResource, '/poi')
    api_rest.add_resource(EventsHourlyResource, '/events/hourly')
    api_rest.add_resource(EventsDailyResource, '/events/daily')
