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


class DeviceWithLastLocationType(DjangoObjectType):
    last_location = graphene.Field(LocationType)

    class Meta:
        model = Device
        fields = '__all__'

    def resolve_last_location(self, info):
        last_location = Location.objects.filter(
            device=self
        ).order_by('-created_at').first()
        return last_location


class Query(graphene.ObjectType):
    devices = graphene.List(DeviceType)
    locations = graphene.List(LocationType)
    device_location_history = graphene.List(LocationType, device_id=graphene.Int(required=True))
    devices_with_last_locations = graphene.List(DeviceWithLastLocationType)

    def resolve_devices(self, info, **kwargs):
        return Device.objects.all()

    def resolve_locations(self, info, **kwargs):
        return Location.objects.all()

    def resolve_device_location_history(self, info, device_id):
        try:
            device = Device.objects.get(pk=device_id)
        except Device.DoesNotExist:
            return None
        return Location.objects.filter(device=device).order_by('-created_at')

    def resolve_devices_with_last_locations(self, info):
        return Device.objects.annotate(
            last_location_id=Subquery(
                Location.objects.filter(device=OuterRef('pk')).order_by('-created_at').values('id')[:1]
            ),
            last_location_latitude=Subquery(
                Location.objects.filter(device=OuterRef('pk')).order_by('-created_at').values('latitude')[:1]
            ),
            last_location_longitude=Subquery(
                Location.objects.filter(device=OuterRef('pk')).order_by('-created_at').values('longitude')[:1]
            ),
            last_location_created_at=Subquery(
                Location.objects.filter(device=OuterRef('pk')).order_by('-created_at').values('created_at')[:1]
            )
        ).filter(
            last_location_id__isnull=False
        )


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
