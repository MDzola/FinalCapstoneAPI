from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from ItemFinder.models import *
from ItemFinder.views import register_user, login_user
from ItemFinder.views import SpareItems, Equipments, ItemCategories, RequisitionOrders, RequisitionItems

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'spareitems', SpareItems, 'spareitem')
router.register(r'equipments', Equipments, 'equipment')
router.register(r'itemcategories', ItemCategories , 'itemcategory')
router.register(r'requisitionorders', RequisitionOrders, 'requisitionorder')
router.register(r'requisitionitems', RequisitionItems, 'requisitionitem')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]