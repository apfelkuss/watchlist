from django.urls import path
from . import views


app_name = "films"

urlpatterns = [
        path("", views.IndexView.as_view(), name="index"),
        # ex: film/314/
        path("film/<pk>/", views.DetailView.as_view(), name="detail"),
        # ex: search/?q=django+unchained
        path("search/", views.SearchView.as_view(), name="search"),
        # ex: film/314/delete
        path("film/<pk>/delete/", views.FilmDelete.as_view(), name="delete"),
        # ex: to_watch/
        path("to_watch/", views.ToWatchView.as_view(), name="to_watch"),
        # ex: completed/
        path("completed/", views.CompletedView.as_view(), name="completed"),
        # ex: film/314/mark_as_completed/
        path("film/<pk>/mark_as_completed/", views.MarkAsCompleted.as_view(), name="mark_as_completed"),
]
