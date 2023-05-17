#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from fastapi import FastAPI

from .globals import ID_VERSION

app = FastAPI(
    title="JukeBox Music App",
    version=ID_VERSION,
)
