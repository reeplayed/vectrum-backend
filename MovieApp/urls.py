"""MovieApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from user.serializer import MyTokenObtainPairView
from user.views import google_login_view, sing_up_view
from movies.views import add_movie,ship, remove_movie, add_to_favourite, remove_from_favourite, movies_list


urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/google-login/', google_login_view, name='google_login'),
    path('api/singup/', sing_up_view, name='sing_up'),
    path('api/singup/', sing_up_view, name='sing_up'),
    path('ships/', ship),

    path('api/add-movie/', add_movie, name='add_movie'),
    path('api/remove-movie/', remove_movie, name='remove_movie'),
    path('api/add-to-favourite/', add_to_favourite, name='add_to_favourite'),
    path('api/remove-from-favourite/', remove_from_favourite, name='remove_from_favourite'),
    path('api/movies-list/', movies_list, name='movies_list'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
