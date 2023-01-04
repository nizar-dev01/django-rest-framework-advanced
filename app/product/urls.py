from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("", views.BrandViewSet, basename="brand")

app_name = "product"

urlpatterns = [
    path("create/", views.CreateProduct.as_view(), name="create"),
    path("update/<slug:brand>/", views.UpdateProduct.as_view(), name="update"),
    path("list/", views.ListProduct.as_view(), name="list"),
    path("detail/<slug:brand>/", views.GetProduct.as_view(), name="detail"),
    path("destroy/<slug:brand>/", views.DeleteProduct.as_view(), name="destroy"),
    path("brands/", include(router.urls))
]
