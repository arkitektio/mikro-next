from mikro_next.deployed import deployed
from mikro_next.api.schema import from_array_like
import numpy as np

app = deployed()

app.deployment.project.overwrite = True
app.deployment.health_on_enter = True

with app:
    with app.deployment.logswatcher("mikro"):
        print(from_array_like(np.zeros((200, 200, 10)), name="Farter"))
