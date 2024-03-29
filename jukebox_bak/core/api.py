#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/v1",
)


@router.get('/error')
async def error():
    raise HTTPException(404, "Hi I am a error")
