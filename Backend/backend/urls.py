"""backend URL Configuration

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
# from django.contrib import admin
# from django.urls import path
from django.urls import include, path
from rest_framework import routers
from backend.vkstock import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'types', views.TypeViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'sources', views.SourceViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'post_images', views.PostImageViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'rendered_posts', views.RenderedPostViewSet)
router.register(r'rendered_images', views.RenderedImageViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/1.0/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
