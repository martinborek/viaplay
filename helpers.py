#!/usr/bin/env python3

# Author: Martin Borek (mborekcz@gmail.com)
# Date: Apr/2017


import datetime
from flask import jsonify
from errors import InputError, ConstErrs

OLDEST_MOVIE_YEAR = 1888  # Used for validating input data


def json_false_status(message=None):
    '''Creates JSON content for unsuccessful HTTP response'''

    return jsonify({"status": False, "message": message})


def create_movie(title, description, duration, production_year, production_country, actors_list, cover_image,
                 audio_languages_list, genre_list, imdb_rating, is_available):
    '''Creates JSON for a movie entry'''

    movie = {
        "title": title,
        "description": description,
        "duration": duration,
        "production_year": production_year,
        "production_country": production_country,
        "actors": actors_list,
        "cover_image": cover_image,
        "audio_languages": audio_languages_list,
        "genre": genre_list,
        "imdb_rating": imdb_rating,
        "isAvailable": is_available
    }
    return movie


def validate_movie_data(title, description, duration, production_year, production_country, actors, cover_image,
                        audio_languages, genre, imdb_rating, is_available):
    '''Validates input data for adding a movie'''

    # Following items do not use any validation for now
    _ = audio_languages
    _ = actors
    _ = cover_image

    if not title:
        raise InputError(ConstErrs.title)

    if not description:
        raise InputError(ConstErrs.description)

    if duration < 0:
        raise InputError(ConstErrs.duration)

    current_year = int(datetime.datetime.today().year)
    if production_year < OLDEST_MOVIE_YEAR or production_year > current_year:
        raise InputError(ConstErrs.production_year)

    if not production_country:
        raise InputError(ConstErrs.production_country)

    if imdb_rating < 1.0 or imdb_rating > 10.0:
        raise InputError(ConstErrs.imdb)

    if not genre:
        raise InputError(ConstErrs.genre)

    if not isinstance(is_available, bool):
        raise InputError(ConstErrs.is_available)

    return True


def default_movie():
    '''Creates a default movie object'''

    movie = {
        "title": "The Huntsman: Winter's War",
        "description": "Den elaka drottningen Ravenna förvandlar sin syster Freyas hjärta till is. Detta svek väcker en"
                       " isande kraft inom Freya och hindrar henne från att älska. Ett krig bryter ut mellan systrarna."
                       " Jägaren Eric och hans följeslagare Sara måste hjälpa Freya att besegra sin syster så att inte"
                       " den ondskefulla Ravenna härskar för all framtid.",
        "duration": 6540000,
        "production_year": 2016,
        "production_country": "USA",
        "actors": [
            "Charlize Theron",
            "Emily Blunt",
            "Nick Frost",
            "Jessica Chastain",
            "Chris Hemsworth"
        ],
        "cover_image": "https://i-viaplay-com.akamaized.net/scandi/Viaplay_Prod_-_Scandi/1001/108/1470751577-a216d10d96055ba93e8ec4a3b2e745a3019614dc.jpg?width=199&height=298&token=4559b1eb",
        "audio_languages": [
            "sv",
            "en",
            "no",
            "da",
            "fi"
        ],
        "genre": [
            "Drama",
            "Action"
        ],
        "imdb_rating": 6.1,
        "isAvailable": True
    }
    return movie
