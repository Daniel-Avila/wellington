from django.views import generic
from bob.report import Report
from rest_framework.views import APIView
from rest_framework.response import Response

class ReportView(generic.ListView):

    template_name = 'bob/index.html'
    context_object_name = 'report_data'

    def get_queryset(self):
        return Report().generate_report()


class RestReportView(APIView):

    def get(self, request, format=None):
        '''A simple get method to return the report data for

        consumption by a thick client. Probably implemented in Angular'''

        return Response(Report().generate_report())
