from django.conf.urls import url
from bob.views import ReportView, RestReportView

urlpatterns = [
    url(r'report/$', ReportView.as_view()),
    url(r'api/v1/$', RestReportView.as_view()),
]