from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

def generate_tokens():
    users = User.objects.all()
    for user in users:
        token, created = Token.objects.get_or_create(user=user)
        print(f"Token generado para el usuario {user.username}: {token.key}")

if __name__ == "__main__":
    generate_tokens()