import os

from fastapi import FastAPI, Depends

from pxm_commons.enums import ApiVersionEnum


async def _common_parameters(version: ApiVersionEnum) -> dict:
    """Helper function to get all the common parameters for all REST endpoints."""
    return {'version': version}

# // ---------------------------------------------------------------------------------------------------- router def

# FastAPI Router
router = FastAPI(
    title='ProjectX Music API',
    version=os.getenv('pxm.version') or 'n/a',
    dependencies=[Depends(_common_parameters)]
)
router.router.prefix = '/api/{version}'  # FastAPI do not allow mentioning prefix during router initialization
