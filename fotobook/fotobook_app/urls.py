from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('dashboard', views.dashboard, name='dashboard'), 
    path('spotlight/<int:image_id>/delete', views.delete, name='delete'),
    path('spotlight/<int:image_id>/', views.spotlight, name="spotlight"),
    path('register', views.register, name='register'),
    path('myaccount/<int:user_id>/edit', views.edit, name='edit'),
    path('user/<int:user_id>/update', views.update, name='update'),
    path('CreateAccount', views.create, name='create'),
    path('login', views.login, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)