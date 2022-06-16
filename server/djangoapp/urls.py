from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path(route='', view=views.get_dealerships, name='index'),
    path('dealer/<int:dealerId>/', views.get_dealer_reviews, name='dealer_reviews'),
    path('add/<int:dealerId>/', views.add_review, name='add_review'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    #path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    #path('<int:course_id>/submit/', views.submit, name='submit'),
    # path for dealer reviews view
    # path for add a review view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)