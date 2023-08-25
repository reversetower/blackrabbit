#mainsite/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mainsite import views

router = DefaultRouter()
router.register(r"registerapi", views.RegisterAPI, basename="registerapi")
router.register(r"loginapi", views.LoginAPI, basename="loginapi")
router.register(r"logoutapi", views.Logout, basename="logoutapi")
router.register(r"userdataeditapi", views.UserDataEdit, basename="userdataeditapi")
router.register(r"newscrawlerapi", views.NewsCrawlerAPI, basename="newscrawlerapi")
router.register(r"getnewslistapi", views.GetNewsListAPI, basename="getnewslistapi")

urlpatterns = [
    path("", include(router.urls)),
]