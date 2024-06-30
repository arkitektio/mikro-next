try:
    from rath.contrib.fakts.links.aiohttp import FaktsAIOHttpLink
    from rath.links.split import SplitLink
    from rath.contrib.fakts.links.graphql_ws import FaktsGraphQLWSLink
    from rath.contrib.herre.links.auth import HerreAuthLink
    from fakts import Fakts
    from herre import Herre
    from rekuest_next.postmans.graphql import GraphQLPostman
    from arkitekt_next.service_registry import get_default_service_builder_registry, Params
    from arkitekt_next.model import Requirement


    from mikro_next.mikro_next import MikroNext
    from mikro_next.rath import MikroNextLinkComposition, MikroNextRath
    from rath.links.split import SplitLink
    from rath.contrib.fakts.links.aiohttp import FaktsAIOHttpLink
    from rath.contrib.fakts.links.graphql_ws import FaktsGraphQLWSLink
    from rath.contrib.herre.links.auth import HerreAuthLink
    from mikro_next.contrib.fakts.datalayer import FaktsDataLayer
    from mikro_next.links.upload import UploadLink
    from mikro_next.datalayer import DataLayer
    from graphql import OperationType
    from herre import Herre
    from fakts import Fakts


    class ArkitektNextMikroNext(MikroNext):
        rath: MikroNextRath
        datalayer: DataLayer


    def builder_mikro(fakts: Fakts, herre: Herre,  params: Params):
        datalayer = FaktsDataLayer(fakts_group="datalayer", fakts=fakts)

        return ArkitektNextMikroNext(
            rath=MikroNextRath(
                link=MikroNextLinkComposition(
                    auth=HerreAuthLink(herre=herre),
                    upload=UploadLink(
                        datalayer=datalayer,
                    ),
                    split=SplitLink(
                        left=FaktsAIOHttpLink(fakts_group="mikro", fakts=fakts),
                        right=FaktsGraphQLWSLink(fakts_group="mikro", fakts=fakts),
                        split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                    ),
                )
            ),
            datalayer=datalayer
        )
    
    def fake_builder(fakts,herre, params):
        return  FaktsDataLayer(fakts_group="datalayer", fakts=fakts)
        
    service_builder_registry = get_default_service_builder_registry()
    service_builder_registry.register("mikro", builder_mikro,Requirement(
            service="live.arkitekt.mikro",
            description="An instance of ArkitektNext Mikro to make requests to the user's data",
            optional=True,
        ),)
    service_builder_registry.register("datalayer", fake_builder, Requirement(
            service="live.arkitekt.datalayer",
            description="An instance of ArkitektNext Datalayer to make requests to the user's data",
            optional=True,
        ),)
    imported = True

except ImportError as e:

    imported = False
    raise e