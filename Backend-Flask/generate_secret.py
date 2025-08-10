import secrets
import base64

# Generate a 32-byte (256-bit) random key and encode it in base64
secret_key = base64.b64encode(secrets.token_bytes(32)).decode("utf-8")
print("\nGenerated JWT_SECRET_KEY:")
print(secret_key)
print("\nAdd this to your .env file as:")
print(f"JWT_SECRET_KEY={secret_key}\n")
