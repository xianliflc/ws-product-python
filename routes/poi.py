from flask_restful import Resource
from flask import request, jsonify
from libs.rate_limiter import rate_limiter
from libs.query_helper import queryHelper
import libs.http_status as status
import libs.json_response as response
from libs.validator import Validator

class PoiResource(Resource):
    
    @rate_limiter(100)
    @Validator("poi_validator.PoiEventsSchema")
    def get(self, data=None, errors=None):
        if errors:
            return response.error(errors, status.HTTP_BAD_REQUEST.get('code'))
        include = [] if data['include'] is None else data['include'].strip().split(',')
        revenue = ''
        events = ''
        having = 'HAVING 1 > 0'

        try:
            max_revenue = data['max_revenue'] if 'max_revenue' in data else None
            min_revenue = data['min_revenue'] if 'min_revenue' in data else None
            max_events = data['max_events'] if 'max_events' in data else None
            min_events = data['min_events'] if 'min_events' in data else None
        except ValueError:
            return response.error({
                'message': 'Bad request'
            }, status.HTTP_BAD_REQUEST.get('code'))

        if 'revenue' in include:
            revenue = ', CAST(SUM(HS.REVENUE) AS INTEGER) AS REVENUE'
            having = having + (" AND SUM(HS.REVENUE) <= {max_revenue}". \
                format(max_revenue=str(max_revenue)) if not (max_revenue is None) else "")
            having = having + (" AND SUM(HS.REVENUE) >= {min_revenue}". \
                format(min_revenue=str(min_revenue)) if not (min_revenue is None) else "")

        if 'events' in include:
            events = ', SUM(HE.EVENTS) AS EVENTS'
            having = having + (" AND SUM(HE.EVENTS) <= {max_events}". \
                format(max_events=str(max_events)) if not (max_events is None) else "")
            having = having + (" AND SUM(HE.EVENTS) >= {min_events}". \
                format(min_events=str(min_events)) if not (min_events is None) else "")
        data = queryHelper('''
            SELECT
                P.POI_ID,
                P.NAME AS "Poi Name", 
                P.LAT,
                P.LON
                {events}
                {revenue}
            FROM POI AS P
            LEFT JOIN HOURLY_EVENTS AS HE
                ON HE.POI_ID = P.POI_ID
            LEFT JOIN HOURLY_STATS AS HS
                ON HS.POI_ID = P.POI_ID
            GROUP BY P.POI_ID
            {having}
            ORDER BY P.NAME
            '''.format(
                events=events,
                revenue=revenue,
                having=having
            )
        )

        return response.response(data, status.HTTP_OK.get('code'))
