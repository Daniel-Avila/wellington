from django.conf.urls import include, url
from django.contrib import admin
import bob.urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'Inspect.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^bob/', include(bob.urls)),
]
