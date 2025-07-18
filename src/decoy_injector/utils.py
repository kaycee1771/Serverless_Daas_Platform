import random
import string

def generate_fake_decoys():
    def rand_str(n=16):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

    return {
        "FAKE_API_KEY": "AKIA" + rand_str(16),
        "FAKE_SECRET_KEY": rand_str(32),
        "FAKE_INTERNAL_URL": f"http://{rand_str(8)}.internal.local",
        "FAKE_DB_CONN": f"postgres://{rand_str(6)}:{rand_str(10)}@{rand_str(8)}.rds.amazonaws.com:5432/fake_db"
    }
