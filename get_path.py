import os
import json
from tqdm import tqdm
from api_calls import get_movie_details, get_person_details, get_people, get_movies


MOVIE_CACHE = "./cache/movie_dict_cache.json"
PERSON_CACHE = "./cache/person_dict_cache.json"
ID_BLACKLIST = [99]
MIN_VOTE_COUNT = 40


def main():
    initial_id = 16
    initial_type = "movie"
    get_path(initial_id, initial_type)


def get_path(initial_id, initial_type, max_nest_level=1, person_blacklist=[], movie_blacklist=[]):
    valid_movies = dict()

    person_blacklist = [str(person_id) for person_id in person_blacklist]
    movie_blacklist = [str(movie_id) for movie_id in movie_blacklist]
    
    if initial_type == "movie":
        movie_id_list = [str(initial_id)]
        person_id_list = []
        movie_blacklist.append(str(initial_id))

        movie_dict = get_movie_details(initial_id)
        release_year = movie_dict["release_date"].split("-")[0]
        json_save_name = f"./movies/{initial_id} - {movie_dict["title"]} ({release_year}).json"
    elif initial_type == "person":
        movie_id_list = []
        person_id_list = [str(initial_id)]

        person_dict = get_person_details(initial_id)
        json_save_name = f"./people/{initial_id} - {person_dict["name"]}.json"
    else:
        raise ValueError("Initial ID must be 'person' or 'movie'.")
    
    if os.path.isfile(MOVIE_CACHE):
        with open(MOVIE_CACHE, "r") as f:
            movie_dict_cache = json.load(f)
    else:
        movie_dict_cache = dict()

    if os.path.isfile(PERSON_CACHE):
        with open(PERSON_CACHE, "r") as f:
            person_dict_cache = json.load(f)
    else:
        person_dict_cache = dict()

    for nest in range(max_nest_level):
        print(nest, "people")
        if movie_id_list or nest > 0:
            person_id_list = []
        for movie_id in movie_id_list:
            if movie_id not in movie_dict_cache.keys():
                person_dict = get_people(movie_id)
                movie_dict_cache[movie_id] = person_dict
            else:
                person_dict = movie_dict_cache[movie_id]
            
            pid_set = person_dict.keys()
            pbl_set = set(person_blacklist)
            new_person_ids = list(pid_set - pbl_set)
            person_id_list.extend(new_person_ids)
        
        with open(MOVIE_CACHE, "w") as f:
            json.dump(movie_dict_cache, f, indent=4)
        
        print(nest, "movies")
        if person_id_list or nest > 0:
            movie_id_list = []
        for person_id in tqdm(person_id_list):
            if person_id not in person_dict_cache.keys():
                movie_dict = get_movies(person_id)
                person_dict_cache[person_id] = movie_dict
            else:
                movie_dict = person_dict_cache[person_id]
            
            mid_set = movie_dict.keys()
            mbl_set = set(movie_blacklist)
            new_movie_ids = list(mid_set - mbl_set)
            movie_id_list.extend(new_movie_ids)
            
            for movie_id in new_movie_ids:
                if movie_id not in valid_movies.keys():
                    id_union = set(movie_dict[movie_id]["genre_ids"]) & set(ID_BLACKLIST)
                    if not id_union and movie_dict[movie_id]["vote_count"] >= MIN_VOTE_COUNT:
                        valid_movies[movie_id] = movie_dict[movie_id]
        
        with open(PERSON_CACHE, "w") as f:
            json.dump(person_dict_cache, f, indent=4)
        
        valid_movies = dict(sorted(valid_movies.items(), key=lambda x: x[1]["vote_count"]))
        with open(json_save_name, "w") as f:
            json.dump(valid_movies, f, indent=4)


if __name__ == "__main__":
    main()
