import json

__author__ = 'sparky'
import yaml
import Inspect.models as core_models
from abc import (ABCMeta,
                 abstractmethod)

class BaseReport(object):
    '''Base Report Class'''
    __metaclass__ = ABCMeta

    path = None

    _filter_extensions = ('exact', 'iexact', 'contains', 'icontains', 'in', 'gt', 'gte', 'lt', 'lte', 'startswith',
                          'istartswith', 'endswith', 'iendswith', 'range', 'isnull', 'search', 'regex', 'iregex',
                          # special ones for dates
                          'year', 'month', 'day', 'week_day', 'hour', 'minute', 'second')
    def __init__(self):
        if self.path is None:
            raise ValueError('Please specify the location of the yaml file')
        self.data = []
        self.load_yaml()

    def load_yaml(self, target=None):
        if target is None:
            target = self.path
        data_map = yaml.load(open(target))
        return_value = []
        for klass, value in data_map.iteritems():
            target_klass = getattr(core_models, klass)
            # Now we build a filter
            filter_args = {}
            cols = []
            for field, val in value.iteritems():
                if val is None:
                    cols.append(field)
                elif val.startswith(self._filter_extensions): # we have a filter extension e.g. lt 2
                    k, v = val.split(' ', 1)
                    # in takes a list. which we have to safely convert from a string
                    # to a list type. We use json here rather eval because we don't want
                    # to run any code. Don't know if this will handle dates
                    if k == 'in':
                        v = json.loads(v)
                    # range has a start and end value corner case
                    # Also this currently won't handle a date range. Just ints
                    if k == 'range':
                        start, end = v.split(',')
                        v = (int(start), int(end),)
                    k = '{0}__{1}'.format(field, k)
                    filter_args.update({k: v})
                elif ':' in val: # We have some sort of Class.attribute:attribute=value filter
                    klass_attr = val.split(':')[0].split('.')
                    attr_val = val.split(':')[1]
                    klass = getattr(core_models, klass_attr[0])
                    f_args = {x[0]:x[1] for x in [attr_val.split('=')]}
                    data = klass.objects.filter(**f_args).values(klass_attr[1])
                    filter_args.update(data[0])

                elif val is not None:
                    filter_args[field] = val
            if filter_args:
                data = target_klass.objects.filter(**filter_args).values(*cols)
                return_value.append(data)
            else:
                data = target_klass.objects.all().values(*cols)
                return_value.append(data)
        self.data = return_value

    @abstractmethod
    def generate_report(self):
        """generate a custom report"""
        return None
