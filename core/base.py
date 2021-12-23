from fastapi import FastAPI, Depends

# import models
from common import ApiVersion


async def _common_parameters(version: ApiVersion) -> dict:
    """Helper function to get all the common parameters for all REST endpoints."""
    return {'version': version}


# FastAPI Router
router = FastAPI(
    dependencies=[Depends(_common_parameters)]
)
router.router.prefix = '/api/{version}'  # FastAPI do not allow mentioning prefix during router initialization

# Load Endpoints
# models.register_model_endpoints(router)  # Model Endpoints
