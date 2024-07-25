from django.db.models import OuterRef, Subquery
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Device, Location
from .serializers import DeviceSerializer, LocationSerializer, DeviceWithLastLocationSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=True, methods=['get'])
    def location_history(self, request, pk=None):
        device = self.get_object()
        locations = Location.objects.filter(device=device).order_by('-created_at')
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def last_locations(self, request):
        latest_location_subquery = Location.objects.filter(
            device=OuterRef('pk')
        ).order_by('-created_at').values('id', 'latitude', 'longitude', 'created_at')[:1]

        devices_with_last_location = Device.objects.annotate(
            last_location_id=Subquery(latest_location_subquery.values('id')),
            last_location_latitude=Subquery(latest_location_subquery.values('latitude')),
            last_location_longitude=Subquery(latest_location_subquery.values('longitude')),
            last_location_created_at=Subquery(latest_location_subquery.values('created_at')),
        ).filter(last_location_id__isnull=False).values(
            'id', 'last_location_id', 'last_location_latitude', 'last_location_longitude', 'last_location_created_at'
        )

        serializer = DeviceWithLastLocationSerializer(devices_with_last_location, many=True)
        return Response(serializer.data)
