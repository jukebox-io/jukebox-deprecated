#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from pydantic import EmailStr, Json

from jukebox.core.model import Model


class Account(Model):
    uid: str
    name: str
    email: EmailStr
    active: bool
