#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

import pydantic


class Model(pydantic.BaseModel):
    """
    Base model for all entities
    """

    class Config(pydantic.BaseConfig):
        orm_mode = True
