import graphene

import device.schema


class Query(device.schema.Query, graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(device.schema.Mutation, graphene.ObjectType):
    # Combine the mutations from different apps
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
