import graphene
from django.db.models import OuterRef, Subquery
from graphene_django import DjangoObjectType
from device.models import Device, Location


class DeviceType(DjangoObjectType):
    class Meta:
        model = Device
        fields = '__all__'


class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        fields = '__all__'


class DeviceWithLastLocationType(graphene.ObjectType):
    id = graphene.ID()
    last_location_id = graphene.ID()
    last_location_latitude = graphene.Float()
    last_location_longitude = graphene.Float()
    last_location_created_at = graphene.DateTime()


class Query(graphene.ObjectType):
    devices = graphene.List(DeviceType)
    locations = graphene.List(LocationType)
    device_location_history = graphene.List(LocationType, device_id=graphene.Int(required=True))
    device_last_locations = graphene.List(DeviceWithLastLocationType)

    def resolve_devices(self, info, **kwargs):
        return Device.objects.all()

    def resolve_locations(self, info, **kwargs):
        return Location.objects.all()

    def resolve_device_location_history(root, info, device_id):
        try:
            device = Device.objects.get(pk=device_id)
        except Device.DoesNotExist:
            return None
        return Location.objects.filter(device=device).order_by('-created_at')

    def resolve_device_last_locations(root, info):
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

        return [
            {
                'id': device['id'],
                'last_location_id': device['last_location_id'],
                'last_location_latitude': device['last_location_latitude'],
                'last_location_longitude': device['last_location_longitude'],
                'last_location_created_at': device['last_location_created_at'],
            }
            for device in devices_with_last_location
        ]


class CreateDevice(graphene.Mutation):
    device = graphene.Field(DeviceType)

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        device = Device(name=name)
        device.save()
        return CreateDevice(device=device)


class UpdateDevice(graphene.Mutation):
    ok = graphene.Boolean()
    device = graphene.Field(DeviceType)

    class Arguments:
        device_id = graphene.ID()
        name = graphene.String()

    def mutate(self, info, device_id, name):
        device = Device.objects.get(id=device_id)
        device.name = name
        device.save()
        return UpdateDevice(ok=True, device=device)


class DeleteDevice(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        device_id = graphene.ID()

    def mutate(self, info, device_id):
        device = Device.objects.get(id=device_id)
        device.delete()
        return DeleteDevice(ok=True)


class Mutation(graphene.ObjectType):
    create_device = CreateDevice.Field()
    update_device = UpdateDevice.Field()
    delete_device = DeleteDevice.Field()
