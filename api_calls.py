from utils import get_response


RELEVANT_PERSON_KEYS = ["name"]
RELEVANT_MOVIE_KEYS = ["genre_ids", "id", "popularity", "release_date", "title", "vote_count"]
VALID_JOBS = [
    "Original Music Composer",
    "Director",
    "Director of Photography",
    "Writer"
]


def get_genres():
    endpoint = f"genre/movie/list"
    data = get_response(endpoint)
    return data


def get_movie_details(movie_id):
    movie_endpoint = f"movie/{movie_id}"
    movie_data = get_response(movie_endpoint)
    movie_dict = {key: movie_data[key] for key in RELEVANT_MOVIE_KEYS if key in movie_data.keys()}
    return movie_dict


def get_person_details(person_id):
    person_endpoint = f"person/{person_id}"
    person_data = get_response(person_endpoint)
    person_dict = {key: person_data[key] for key in RELEVANT_PERSON_KEYS if key in person_data.keys()}
    return person_dict


def get_people(movie_id):
    credits_endpoint = f"movie/{movie_id}/credits"
    credits_data = get_response(credits_endpoint)

    if credits_data is None:
        return None
    else:
        person_dict = dict()

        cast = credits_data.get("cast", [])
        crew = credits_data.get("crew", [])

        for person in cast + crew:
            job = person.get("job", None)
            if job is None or job in VALID_JOBS:
                person_id = person["id"]
                person_dict[str(person_id)] = {key: person[key] for key in RELEVANT_PERSON_KEYS}

        return person_dict


def get_movies(person_id):
    credits_endpoint = f"person/{person_id}/movie_credits"
    credits_data = get_response(credits_endpoint)

    if credits_data is None:
        return None
    else:
        movie_dict = dict()

        cast = credits_data.get("cast", [])
        crew = credits_data.get("crew", [])

        for movie in cast + crew:
            movie_id = movie["id"]
            if movie_id not in movie_dict.keys():
                movie_dict[str(movie_id)] = {key: movie[key] for key in RELEVANT_MOVIE_KEYS}
    
        return movie_dict
 