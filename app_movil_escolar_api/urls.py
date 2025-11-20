from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views.bootstrap import VersionView
#from sistema_escolar_api.views import bootstrap
from app_movil_escolar_api.views import users,alumno, maestro
from app_movil_escolar_api.views import auth


urlpatterns = [
    #Create Admin User
        path('admin/', users.AdminView.as_view()),
    #Create Alumno User
        path('alumno/', alumno.AlumnosView.as_view()),
    #Create Maestro User
        path('maestro/', maestro.MaestrosView.as_view()),
    #Admin Data
        path('lista-admins/', users.AdminAll.as_view()),
    #Maestro Data
        path('lista-maestros/', maestro.MaestrosAll.as_view()),
    #Alumno Data
        path('lista-alumnos/', alumno.AlumnosAll.as_view()),
    #Total Users
        path('total-usuarios/', users.TotalUsers.as_view()),
    #Login and Logout
        path('login/', auth.CustomAuthToken.as_view()),
        path('logout/', auth.Logout.as_view()), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
