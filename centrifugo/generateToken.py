import secrets

def generate_api_key(length=32):
    return secrets.token_urlsafe(length)

if __name__ == "__main__":
    print(generate_api_key())
