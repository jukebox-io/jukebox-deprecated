import os

from fastapi import FastAPI, Depends

from common.api_version import ApiVersion


async def _common_parameters(version: ApiVersion) -> dict:
    """Helper function to get all the common parameters for all REST endpoints."""
    return {'version': version}


def _read_version_file() -> str:
    """Read the version file located at root dir"""
    pxm_home = os.getenv('pxm.home')
    with open(f'{pxm_home}/version.txt', 'r') as ver_file:
        return ver_file.read().strip()


# // ---------------------------------------------------------------------------------------------------- router def

# FastAPI Router
router = FastAPI(
    title='ProjectX Music API',
    version=_read_version_file(),
    dependencies=[Depends(_common_parameters)]
)
router.router.prefix = '/api/{version}'  # FastAPI do not allow mentioning prefix during router initialization
