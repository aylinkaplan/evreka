import graphene

import device.schema


class Query(device.schema.Query, graphene.ObjectType):
    pass


class Mutation(device.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
