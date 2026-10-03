import requests
from extract import create_session, get_json

FAILED_URL = "https://pokeapi.co/api/v2/pokemon/this-pokemon-does-not-exist"

session = create_session()

print("Starting failure scenario...")
print(f"Requesting: {FAILED_URL}")

result = get_json(session, FAILED_URL)

if result is None:
    print("Failure handled successfully.")
else:
    print("Unexpected success.")