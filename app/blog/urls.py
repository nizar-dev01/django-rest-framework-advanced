from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("create", views.CreateBlogView.as_view(), name="create"),
    path("update/<slug:slug>/", views.UpdateBlogView.as_view(), name="update"),
    path("list", views.ListBlogView.as_view(), name="list"),
    path("get/<slug:slug>", views.GetBlogView.as_view(), name="get"),
    path("delete/<slug:slug>", views.DeleteBlogView.as_view(), name="delete")
]
