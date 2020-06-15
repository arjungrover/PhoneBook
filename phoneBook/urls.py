from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers

from user.views import SignupViewSet, LoginView
from contacts.views import ContactViewSet, SpamViewSet, GetUsersByName, GetUsersByNumber

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'search_name', GetUsersByName.as_view(), name="search_name"),
    url(r'search_number', GetUsersByNumber.as_view(), name='search_number'),
]

router = routers.SimpleRouter()
router.register(r'signup', SignupViewSet, basename="signup")
urlpatterns = urlpatterns + router.urls
router.register(r'add-contacts', ContactViewSet, basename="addcontacts")
urlpatterns = urlpatterns + router.urls
router.register(r'add-spam', SpamViewSet, basename="addspam")
urlpatterns = urlpatterns + router.urls

obtain_auth_token = LoginView.as_view()
