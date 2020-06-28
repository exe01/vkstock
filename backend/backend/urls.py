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
from backend.stock_api import views as api_views


router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'groups', api_views.GroupViewSet)
router.register(r'types', api_views.TypeViewSet)
router.register(r'projects', api_views.ProjectViewSet)
router.register(r'sources', api_views.SourceViewSet)
router.register(r'posts', api_views.PostViewSet)
router.register(r'post_images', api_views.PostImageViewSet)
router.register(r'comments', api_views.CommentViewSet)
router.register(r'rendered_posts', api_views.RenderedPostViewSet)
router.register(r'rendered_images', api_views.RenderedImageViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/1.0/render_post', api_views.RenderPost.as_view()),
    path('api/1.0/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
