from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import project_list, contact_list, home_data, about_data, download_resume, experience_view

urlpatterns = [
    # Custom data endpoints
    path('home/', home_data, name='home-data'),
    path('about/', about_data, name='about-data'),

    # Project-related endpoints
    path('projects/', project_list, name='project-list'),
    # path('projects/<int:pk>/', project_detail, name='project-detail'),

    # Contact-related endpoints
    path('contacts/', contact_list, name='contact-list'),
    # path('contacts/<int:pk>/', contact_detail, name='contact-detail'),
    path('download-resume/', download_resume, name='download_resume'),
    path('experience/',experience_view,name='experience-view')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)