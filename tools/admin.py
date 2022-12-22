import os

def admin(user):
    return str(user) == os.getenv("ADMIN_ID")