from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string that contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='', view=views.get_dealerships, name='index'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),



    #path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    #path('<int:course_id>/submit/', views.submit, name='submit'),


    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)