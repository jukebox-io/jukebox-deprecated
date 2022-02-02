from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from pxm_commons.enums import Config
from pxm_core.docs import get_rapidoc_html
from pxm_models.models import AccessToken, UserLoginInput
from pxm_resources.api_resource import router as api_router
from pxm_security.security import login_user
from pxm_utils.config_utils import read_config

# FastAPI Router Definition
router = FastAPI(
    title='ProjectX Music API',
    version=read_config(Config.APP.VERSION) or 'n/a',
    docs_url=None, redoc_url=None  # Disable builtin docs
)

# Attach API Router
router.include_router(api_router)


# Attach api docs endpoint
@router.get('/api/docs', include_in_schema=False)
async def get_rapidoc() -> HTMLResponse:
    return get_rapidoc_html(
        openapi_url=router.openapi_url,
        title=f'{router.title} Docs'
    )


@router.post('/api/o/oauth2/token', response_model=AccessToken)
async def oauth_token(form_data: OAuth2PasswordRequestForm = Depends()) -> AccessToken:
    user_login_creds = UserLoginInput(uid=form_data.username, password=form_data.password)
    return login_user(user_login_creds)
