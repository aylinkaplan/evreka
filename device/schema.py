import graphene
from graphene_django.types import DjangoObjectType
from .models import Device, Location


class DeviceType(DjangoObjectType):
    class Meta:
        model = Device


class LocationType(DjangoObjectType):
    class Meta:
        model = Location


class Query(graphene.ObjectType):
    devices = graphene.List(DeviceType)
    locations = graphene.List(LocationType, device_id=graphene.Int())

    def resolve_devices(self, info, **kwargs):
        return Device.objects.all()

    def resolve_locations(self, info, device_id, **kwargs):
        return Location.objects.filter(device_id=device_id)


class Mutation(graphene.ObjectType):
    create_device = graphene.Field(DeviceType, name=graphene.String())
    delete_device = graphene.Field(graphene.Boolean, device_id=graphene.Int())

    def resolve_create_device(self, info, name):
        return Device.objects.create(name=name)

    def resolve_delete_device(self, info, device_id):
        Device.objects.filter(id=device_id).delete()
        return True


schema = graphene.Schema(query=Query, mutation=Mutation)
