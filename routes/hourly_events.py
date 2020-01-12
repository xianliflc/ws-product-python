from flask_restful import Resource
from flask import request, jsonify
from libs.rate_limiter import rate_limiter
from libs.query_helper import queryHelper
import libs.http_status as status
import libs.json_response as response
from libs.validator import Validator


class EventsHourlyResource(Resource):
    
    @rate_limiter(100)
    @Validator("stats_validator.StatsSchema")
    def get(self, data=None, errors=None):
        if errors:
            return response.error(errors, status.HTTP_BAD_REQUEST.get('code'))

        start_date = data['start_date']
        end_date = data['end_date']
        limit = ' LIMIT 168'
        if 'page_number' in data and 'page_size' in data:
            offset = (data['page_number'] - 1) * data['page_size'];
            limit = " LIMIT {page_size} OFFSET {offset}".format(
                offset=str(offset),
                page_size=str(data['page_size'])
            );

        data = queryHelper('''
            SELECT date, hour, events
            FROM public.hourly_events
            WHERE date <= '{end_date}' AND date >= '{start_date}'
            ORDER BY date, hour
            {limit};
            '''.format(
                end_date=end_date,
                start_date=start_date,
                limit=limit)
        )

        return jsonify(
            {
                'success': True,
                'data': data
            }
        )