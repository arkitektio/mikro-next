from mikro_next.deployed import deployed
import numpy as np
from mikro_next.api.schema import from_array_like, get_dataset


app = deployed()
app.deployment.project.overwrite = True

with app:


    with app.deployment.logswatcher("mikro"):
        get_dataset(id=65)


