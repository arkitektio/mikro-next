from typing import Generator
import pytest
from dokker import local, Deployment
from dokker.log_watcher import LogWatcher
import os
from mikro_next.mikro_next import MikroNext
from rath.links.auth import ComposedAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from mikro_next.rath import (
    MikroNextRath,
    UploadLink,
    SplitLink,
    MikroNextLinkComposition,
)
from mikro_next.datalayer import DataLayer
from graphql import OperationType
from dataclasses import dataclass

project_path = os.path.join(os.path.dirname(__file__), "integration")
docker_compose_file = os.path.join(project_path, "docker-compose.yml")
private_key = os.path.join(project_path, "private_key.pem")


async def token_loader() -> str:
    """Asynchronous function to load a token for authentication.

    This returns the "test" token which is configured as a static token to map to
    the user "test" in the test environment. In a real application, this function
    will return an oauth2 token or similar authentication token.

    To change this mapping you can alter the static_token configuration in the
    mikro configuration file (inside the integration folder).

    """
    return "test"


@dataclass
class DeployedMikro:
    """Dataclass to hold the deployed MikroNext application and its components."""

    deployment: Deployment
    mikro_watcher: LogWatcher
    minio_watcher: LogWatcher
    mikro: MikroNext


@pytest.fixture(scope="session")
def deployed_app() -> Generator[DeployedMikro, None, None]:
    """Fixture to deploy the MikroNext application with Docker Compose.

    This fixture sets up the MikroNext application using Docker Compose,
    configures health checks, and provides a deployed instance of MikroNext
    for testing purposes. It also includes watchers for the Mikro and MinIO
    services to monitor their logs, when performing requests against the application.

    Yields:
        DeployedMikro: An instance containing the deployment, watchers, and MikroNext instance

    """
    setup = local(docker_compose_file)
    setup.add_health_check(
        url=lambda spec: f"http://localhost:{spec.find_service('mikro').get_port_for_internal(80).published}/graphql",
        service="mikro",
        timeout=5,
        max_retries=10,
    )

    watcher = setup.create_watcher("mikro")
    minio_watcher = setup.create_watcher("minio")

    with setup:
        setup.down()

        minio_url = f"http://localhost:{setup.spec.find_service('minio').get_port_for_internal(9000).published}"
        mikro_http_url = f"http://localhost:{setup.spec.find_service('mikro').get_port_for_internal(80).published}/graphql"
        mikro_ws_url = f"ws://localhost:{setup.spec.find_service('mikro').get_port_for_internal(80).published}/graphql"

        datalayer = DataLayer(
            endpoint_url=minio_url,
        )

        y = MikroNextRath(
            link=MikroNextLinkComposition(
                auth=ComposedAuthLink(token_loader=token_loader, token_refresher=token_loader),
                upload=UploadLink(datalayer=datalayer),
                split=SplitLink(
                    left=AIOHttpLink(endpoint_url=mikro_http_url),
                    right=GraphQLWSLink(ws_endpoint_url=mikro_ws_url),
                    split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                ),
            ),
        )

        mikro = MikroNext(
            datalayer=datalayer,
            rath=y,
        )

        setup.up()

        setup.check_health()

        with mikro as mikro:
            deployed = DeployedMikro(
                deployment=setup,
                mikro_watcher=watcher,
                minio_watcher=minio_watcher,
                mikro=mikro,
            )

            yield deployed
