from decimal import Decimal
from datetime import date, time, datetime
from dateutil import parser
from json import JSONDecoder, JSONEncoder, JSONDecodeError


class XJSONEncoder(JSONEncoder):

    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%H:%M:%S.%f'

    def default(self, obj):
        if isinstance(obj, Decimal):
            return {
                '__type__': 'decimal',
                'value': str(obj),
            }
        if isinstance(obj, datetime):
            return {
                '__type__': 'datetime',
                'value': obj.isoformat(),
            }
        if isinstance(obj, date):
            return {
                '__type__': 'date',
                'value': obj.strftime(self.DATE_FORMAT),
            }
        if isinstance(obj, time):
            return {
                '__type__': 'time',
                'value': obj.strftime(self.TIME_FORMAT),
            }
        return super().default(obj)


class XJSONDecoder(JSONDecoder):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self.object_hook, **kwargs)

    def object_hook(self, obj):
        typ = obj.get('__type__')
        if not typ:
            return obj
        if typ == 'decimal':
            return Decimal(obj['value'])
        if typ == 'date':
            value = obj['value']
            return date(
                year=int(value[0:4]),
                month=int(value[5:7]),
                day=int(value[8:10]),
            )
        if typ == 'time':
            value = obj['value']
            return time(
                hour=int(value[0:2]),
                minute=int(value[3:5]),
                second=int(value[6:8]),
                microsecond=int(value[9:15]),
            )
        if typ == 'datetime':
            return parser.parse(obj['value'])
        return obj

