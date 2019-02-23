from django.urls import path, include


from .rest_views import TeamListView, TeamDetailView

urlpatterns = [
    path('<int:pk>', TeamDetailView.as_view()),
    path('', TeamListView.as_view()),
]