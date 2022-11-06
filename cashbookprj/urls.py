"""cashbookprj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import cashbookapp.views
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns =[
    path('admin/', admin.site.urls),
    path('', cashbookapp.views.main, name='main'),
    path('write/', cashbookapp.views.write, name='write'),
    path('read/', cashbookapp.views.read, name='read'),
    path('detail/<str:id>/', cashbookapp.views.detail, name='detail'),
    path('edit/<str:id>/', cashbookapp.views.edit, name='edit'),
    path('delete/<str:id>/', cashbookapp.views.delete, name='delete'),
    path('update_comment/<str:id>/<str:com_id>/', cashbookapp.views.update_comment, name='update_comment'),
    path('cashbookapp/delete_comment/<int:post_id>/<int:com_id>', cashbookapp.views.delete_comment, name='delete_comment'),
    path('hashtag/', cashbookapp.views.hashtag, name='hashtag'),
    path('hashtag_search/', cashbookapp.views.hashtag_search, name="hashtag_search"),
    path('like/<str:id>/', cashbookapp.views.likes, name="likes"), #좋아요 url
    path('',include('account.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

