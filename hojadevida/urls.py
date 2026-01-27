"""
URL configuration for hojadevida project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from paginausuario import views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.user_dashboard, name="home"),
    path("usuario/", views.user_dashboard, name="user_dashboard"),
    
    ##path('signup/',views.signup,name='signup'),
    ##path("login/", views.login_view, name="login"),
    ##path("usuario/", views.user_dashboard, name="user_dashboard"),
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),
    ##path("logout/", views.logout_view, name="logout"),
    ##path("signup/", views.signup, name="signup"),
    path('datos/', views.lista_personas, name='lista_personas'),
    path('datos/nuevo/', views.crear_persona, name='crear_persona'),
    path('datos/<int:pk>/', views.detalle_persona, name='detalle_persona'),
    path('datos/<int:pk>/editar/', views.formulario_persona, name='editar_persona'),
    path("datos/pdf/", views.datos_pdf, name="datos_pdf"),
    path('experiencia/', views.experiencia_list, name='experiencia_list'),
    path('experiencia/nueva/', views.experiencia_create, name='experiencia_create'),
    path('experiencia/editar/<int:pk>/', views.experiencia_update, name='experiencia_update'),
    path('experiencia/eliminar/<int:pk>/', views.experiencia_delete, name='experiencia_delete'),
    path('reconocimiento/', views.reconocimiento_list, name='reconocimiento_list'),
    path('reconocimiento/crear/', views.reconocimiento_create, name='reconocimiento_create'),
    path('reconocimiento/editar/<int:pk>/', views.reconocimiento_update, name='reconocimiento_update'),
    path('reconocimiento/eliminar/<int:pk>/', views.reconocimiento_delete, name='reconocimiento_delete'),
    path('curso', views.curso_list, name='curso_list'),
    path('curso/crear/', views.curso_create, name='curso_create'),
    path('curso/editar/<int:pk>/', views.curso_update, name='curso_update'),
    path('curso/eliminar2/<int:pk>/', views.curso_delete, name='curso_delete'),
    path('productoacademico', views.productoacademico_list, name='productoacademico_list'),
    path('productoacademico/crear/', views.productoacademico_create, name='productoacademico_create'),
    path('productoacademico/editar/<int:pk>/', views.productoacademico_update, name='productoacademico_update'),
    path('productoacademico/eliminar/<int:pk>/', views.productoacademico_delete, name='productoacademico_delete'),
    path('productolaboral', views.producto_laboral_list, name='producto_laboral_list'),
    path('productolaboral/crear/', views.producto_laboral_create, name='producto_laboral_create'),
    path('productolaboral/editar/<int:pk>/', views.producto_laboral_update, name='producto_laboral_update'),
    path('productolaboral/eliminar/<int:pk>/', views.producto_laboral_delete, name='producto_laboral_delete'),
    path('ventagarage', views.ventagarage_list, name='ventagarage_list'),
    path('ventagarage/crear/', views.ventagarage_create, name='ventagarage_create'),
    path('ventagarage/editar/<int:pk>/', views.ventagarage_update, name='ventagarage_update'),
    path('ventagarage/eliminar/<int:pk>/', views.ventagarage_delete, name='ventagarage_delete'),
    path("admin-secciones/", views.secciones_admin, name="secciones_admin"),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)