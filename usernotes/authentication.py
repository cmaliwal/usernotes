from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    """Custom authentication class to add the keyword in the authorization header. e.g. Authorization: Bearer <token_key>"""

    keyword = "Bearer"
