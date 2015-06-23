import os
from Inspect.report import BaseReport


class Report(BaseReport):
    path = '{0}/report.yaml'.format(os.path.dirname(os.path.realpath(__file__)))

    def generate_report(self):
        return self.data[0]
