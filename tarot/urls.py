from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'tarot'

urlpatterns = [
    path('',views.home,name = 'home'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('register/',views.register,name = 'register'),
    path('create_reading/', views.create_reading, name = 'create_reading'),
    path('create_reading/results/<int:pk>/',views.results,name = 'results'),
    path('review_reading/results/<int:pk>/',views.results,name = 'results'),
    path('review_reading/',views.review_reading,name = 'review_reading'),
	path('generate_reading/',views.generate_reading,name = 'generate_reading'),
    path('generate_reading/results/<int:pk>/',views.results,name = 'results')
 

]
