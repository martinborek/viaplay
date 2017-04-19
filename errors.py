#!/usr/bin/env python3

# Author: Martin Borek (mborekcz@gmail.com)
# Date: Apr/2017


class InputError(Exception):
    '''Error conveying invalid user input'''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ConstErrs:
    '''Constants for informing users about invalid input'''

    title = "Title is mandatory"
    description = "Description is mandatory"
    duration = "Invalid duration"
    production_year = "Invalid production year"
    production_country = "Production country is mandatory"
    genre = "Genre is mandatory"
    imdb = "Invalid IMDB rating, needs to be in scale of 1 to 10"
    is_available = "isAvailable has to be a boolean"
    object_id = "id of the object needs to be provided"
    object_not_found = "Object with the given ID was not found"
