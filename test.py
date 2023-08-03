from rath.links.sign_local_link import ComposedSignTokenLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from mikro_next.mikro_next import MikroNext
from mikro_next.rath import MikroNextRath, DictingLink, FileExtraction, UploadLink, AuthTokenLink, SplitLink, MikroNextLinkComposition
from mikro_next.datalayer import DataLayer
from rath.operation import OperationType
import pytest
from tests.utils import build_relative
from mikro_next.api.schema import from_array_like
import xarray as xr
import numpy as np
import datetime

async def aretrieve_payload(o):
    return {
        "sub": 1,
        "iss": "XXXX",
        "iat": int(datetime.datetime.utcnow().timestamp()),  # issued at
        "exp": int((datetime.datetime.utcnow() + datetime.timedelta(days=1)).timestamp()) ,
        "preferred_username": "farter",
        "client_id": "XXXX",
        "scope": "openid profile email",
        "roles": ["XXXX"],
    }

rel_path = build_relative("integration/private_key.pem")
print(rel_path)
x = ComposedSignTokenLink(
    private_key=rel_path,
    payload_retriever=aretrieve_payload,
)

datalayer = DataLayer(
    endpoint_url="http://localhost:8457",
)

y = MikroNextRath(
    link=MikroNextLinkComposition(
        auth=x,
        upload=UploadLink(datalayer=datalayer),
        split=SplitLink(
                left=AIOHttpLink(endpoint_url="http://localhost:8456/graphql"),
                right=GraphQLWSLink(ws_endpoint_url="ws://mikro_next:8456/graphql"),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
    ),
)

mikro = MikroNext(
    datalayer=datalayer,
    rath=y,
)


with mikro:

    print(from_array_like(np.zeros((200, 200, 10)), name="Farter"))

    