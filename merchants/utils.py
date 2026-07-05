import jwt
import time
import os

from dotenv import load_dotenv

load_dotenv()

ENCODING_SECRET = os.getenv("ENCODING_SECRET")


def generate_test_api_key(payload,key_type="TEST"):
    payload["entropy"] = time.time()
    payload["key_type"] = key_type
    key = jwt.encode(payload,key=ENCODING_SECRET,algorithm="HS256")
    return key

