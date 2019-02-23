from django.urls import path, include


from .rest_views import SponsorListView, SponsorDetailView

urlpatterns = [
    path('<int:pk>', SponsorDetailView.as_view()),
    path('', SponsorListView.as_view()),
]