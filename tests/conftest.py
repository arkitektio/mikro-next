from rath.links.sign_local_link import ComposedSignTokenLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from mikro_next.mikro_next import MikroNext
from mikro_next.rath import MikroNextRath, DictingLink, FileExtraction, UploadLink, AuthTokenLink, SplitLink, MikroNextLinkComposition
from mikro_next.datalayer import DataLayer
from rath.operation import OperationType
import pytest
from .utils import build_relative
import datetime
from testcontainers.compose import DockerCompose
from functools import cached_property
from .integration.utils import wait_for_http_response
from .utils import build_relative
import xarray as xr
import os
import subprocess
from testcontainers.compose import DockerCompose


class DockerV2Compose(DockerCompose):

    @cached_property
    def docker_cmd_comment(self) -> list[str]:
        """Returns the base docker command by testing the docker compose api

        Returns:
            list[ſt]: _description_
        """
        return (
            ["docker", "compose"]
            if subprocess.run(
                ["docker", "compose", "--help"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            ).returncode
            == 0
            else ["docker-compose"]
        )

    def docker_compose_command(self):
        """
        Returns command parts used for the docker compose commands

        Returns
        -------
        list[str]
            The docker compose command parts
        """
        docker_compose_cmd = self.docker_cmd_comment
        for file in self.compose_file_names:
            docker_compose_cmd += ["-f", file]
        if self.env_file:
            docker_compose_cmd += ["--env-file", self.env_file]
        return docker_compose_cmd


@pytest.mark.integration
@pytest.fixture(scope="session")
def docker_integration() -> None:

    assert os.path.exists(build_relative("integration")), "Integration tests not found"

    with DockerV2Compose(
        filepath=build_relative("integration"),
        compose_file_name="docker-compose.yml",
    ) as compose:
        wait_for_http_response("http://localhost:8456/graphql", max_retries=5)
        yield


@pytest.fixture()
def app():

    async def aretrieve_token_payload(o):
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
        payload_retriever=aretrieve_token_payload,
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

    return MikroNext(
        datalayer=datalayer,
        rath=y,
    )

    
        
