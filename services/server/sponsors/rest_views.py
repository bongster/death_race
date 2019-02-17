from rest_framework import generics
from .serializers import SponsorSerializer
from .models import Sponsor

class SponsorListView(generics.ListCreateAPIView):
    serializer_class = SponsorSerializer
    queryset = Sponsor.objects.all()


class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SponsorSerializer
    queryset = Sponsor.objects.all()
