from django.conf import settings

def set_token_cookie(response, key, token):
    response.set_cookie(
        key=key,
        value=token,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite="Lax",
    )


def set_auth_cookies(response, tokens):
    set_token_cookie(response, "access_token", tokens["access"])
    if tokens.get("refresh"):
        set_token_cookie(response, "refresh_token", tokens["refresh"])


def clear_auth_cookies(response):
    response.delete_cookie("access_token", samesite="Lax")
    response.delete_cookie("refresh_token", samesite="Lax")
