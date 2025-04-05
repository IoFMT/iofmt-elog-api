import urllib.parse

import aiohttp
from fastapi import HTTPException, Request, APIRouter
from fastapi.responses import RedirectResponse

from libs import config

router = APIRouter(include_in_schema=False)


async def get_user_info(access_token: str):
    """Retrieves user information from Microsoft Graph API."""
    headers = {"Authorization": f"Bearer {access_token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get("https://graph.microsoft.com/v1.0/me", headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return None


@router.get("/az/login")
async def login(request: Request):
    """Redirect the user to the Azure AD login page."""
    params = {
        "client_id": config.AZAD_CLIENT_ID,
        "redirect_uri": config.AZAD_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile User.Read",
    }
    auth_url = f"{config.AZAD_AUTHORIZE_ENDPOINT}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(auth_url)


@router.get("/auth/callback")
async def auth_callback(request: Request, code: str):
    """Handle the callback from Azure AD, exchange the code for a token, and retrieve user info."""
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.AZAD_REDIRECT_URI,
        "client_id": config.AZAD_CLIENT_ID,
        "client_secret": config.AZAD_CLIENT_SECRET,
        "scope": "openid profile User.Read",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(config.AZAD_TOKEN_ENDPOINT, data=data) as response:
            if response.status == 200:
                token_data = await response.json()
                access_token = token_data.get("access_token")
                user_info = await get_user_info(access_token)
                if user_info:
                    request.session["user"] = user_info
                    return RedirectResponse(url="/admin")
            raise HTTPException(status_code=400, detail="Authentication failed.")

@router.get("/az/logout")
async def logout(request: Request):
    """Logs out the user by clearing the session and redirecting to Azure logout."""
    # request.session.pop("user", None)
    # azure_logout_url = (
    #     f"{config.AZAD_AUTHORITY}/oauth2/v2.0/logout"
    #     f"?post_logout_redirect_uri={urllib.parse.quote(config.HOME_URL)}"
    # )
    # return RedirectResponse(url=azure_logout_url)
    request.session.clear()
    return RedirectResponse(url=config.HOME_URL)
