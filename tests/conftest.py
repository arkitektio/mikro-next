import pytest
from mikro_next.deployed import DeployedMikroNext, deployed


@pytest.fixture(scope="session")
def deployed_app() -> DeployedMikroNext:
    app = deployed()
    app.deployment.project.overwrite = True
    app.deployment.health_on_enter = True
    with app:
        yield app
