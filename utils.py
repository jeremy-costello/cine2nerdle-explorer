import requests


URL_BASE = "https://api.themoviedb.org/3"


def get_url(endpoint):
    url = f"{URL_BASE}/{endpoint}"
    return url


def get_payload():
    with open("key.txt", "r") as f:
        api_key = f.readline()

    headers = {"accept": "application/json"}
    params = {"api_key": api_key}

    return {
        "headers": headers,
        "params": params
    }


def get_response(endpoint):
    url = get_url(endpoint)
    payload_dict = get_payload()

    response = requests.get(
        url,
        headers=payload_dict["headers"],
        params=payload_dict["params"]
    )

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    