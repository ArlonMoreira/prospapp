from rest_framework_simplejwt.tokens import RefreshToken

def get_token_for_user(user):

    refresh_token = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh_token),
        'token': str(refresh_token.access_token)
    }