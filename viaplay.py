#!/usr/bin/env python3

# Author: Martin Borek (mborekcz@gmail.com)
# Date: Apr/2017


from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import render_template
from flask import session
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
import os
import logging
from logging.handlers import RotatingFileHandler
from helpers import create_movie, default_movie, validate_movie_data, json_false_status
from errors import InputError, ConstErrs


app = Flask(__name__)

client = MongoClient('db_viaplay', 27017) # MongoDB running at port 27017

db = client.viaplay
movie_collection = db.movie


@app.route('/frontend/')
def index():
    '''Main frontend page.'''

    app.logger.info("Page accessed: Frontend")

    # Get all movies
    movies_cursor = movie_collection.find({})
    movies_list = [entry for entry in movies_cursor]
    for entry in movies_list:
        entry['_id'] = str(entry['_id'])

    # status is used for displaying success / fail of adding, updating and deleting
    status = None
    if 'message' in session:
        status = session['message']
        session.pop('message', None)

    return render_template('index.html', movies=movies_list, status=status)


@app.route('/')
def main_page():

    app.logger.info("Page accessed: Homepage")
    return 'Viaplay homepage'


@app.route('/add_default/')
def add_default():
    '''Adds default movie entry to the database.'''

    app.logger.info("Page accessed: Add default")

    new_movie = default_movie()
    movie_collection.insert_one(new_movie)

    return jsonify({"status": True})


@app.route('/add/', methods=['POST'])
def add():
    '''Adds movie entry to the database.'''

    # If frontend is set, user will be redirected after processing the request
    # instead of sending JSON response
    frontend = request.args.get('frontend') == "yes"

    app.logger.info("Page accessed: Add")

    title = request.form.get('title')
    description = request.form.get('description')
    production_country = request.form.get('production_country')
    actors = request.form.get('actors')
    cover_image = request.form.get('cover_image')
    audio_languages = request.form.get('audio_languages')
    genre = request.form.get('genre')
    is_available = request.form.get('isAvailable')

    if is_available == "true" or is_available is True:
        is_available = True
    else:
        is_available = False

    try:
        duration = int(request.form.get('duration'))
    except ValueError:
        if frontend:
            session['message'] = ConstErrs.duration
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.duration)

    try:
        production_year = int(request.form.get('production_year'))
    except ValueError:
        if frontend:
            session['message'] = ConstErrs.production_year
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.production_year)

    try:
        imdb_rating = float(request.form.get('imdb_rating'))
    except ValueError:
        if frontend:
            session['message'] = ConstErrs.imdb
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.imdb)

    try:
        validate_movie_data(title, description, duration, production_year, production_country, actors,
                            cover_image, audio_languages, genre, imdb_rating, is_available)
    except InputError as e:
        if frontend:
            session['message'] = str(e)
            return redirect(url_for('index'))
        else:
            return json_false_status(str(e))

    if genre is not None:
        genre_list = [genre.strip() for genre in genre.split(',')]
    else:
        genre_list = []

    if audio_languages is not None:
        audio_languages_list = [language.strip() for language in audio_languages.split(',')]
    else:
        audio_languages_list = []

    if actors is not None:
        actors_list = [actor.strip() for actor in actors.split(',')]
    else:
        actors_list = []

    new_movie = create_movie(title, description, duration, production_year, production_country, actors_list,
                             cover_image, audio_languages_list, genre_list, imdb_rating, is_available)

    movie_collection.insert_one(new_movie)

    if frontend:
        session['message'] = "Movie successfully added"
        return redirect(url_for('index'))
    else:
        return jsonify({"status": True})


@app.route('/update_form/')
def update_form():
    '''Update form view for frontend.'''

    app.logger.info("Page accessed: Frontend update form")

    object_id = request.args.get('id')

    if not object_id:
        session['message'] = ConstErrs.object_id
        return redirect(url_for('index'))

    try:
        movie = movie_collection.find_one({'_id': ObjectId(object_id)})
    except InvalidId:
        session['message'] = ConstErrs.object_id
        return redirect(url_for('index'))

    if movie is None:
        session['message'] = ConstErrs.object_id
        return redirect(url_for('index'))

    movie['_id'] = str(movie['_id'])  # ObjectId needs to be converted
    movie['actors'] = ", ".join(movie['actors'])
    movie['audio_languages'] = ", ".join(movie['audio_languages'])
    movie['genre'] = ", ".join(movie['genre'])

    return render_template('update.html', movie=movie)


@app.route('/update/', methods=['POST'])
def update():
    '''Updates a movie entry in the database.'''

    # If frontend is set, user will be redirected after processing the request
    # instead of sending JSON response
    frontend = request.args.get('frontend') == "yes"

    app.logger.info("Page accessed: Update")

    object_id = request.form.get('id')
    if not object_id:
        return json_false_status(ConstErrs.object_id)

    title = request.form.get('title')
    description = request.form.get('description')
    production_country = request.form.get('production_country')
    actors = request.form.get('actors')
    cover_image = request.form.get('cover_image')
    audio_languages = request.form.get('audio_languages')
    genre = request.form.get('genre')
    is_available = request.form.get('isAvailable')

    if is_available == "true" or is_available is True:
        is_available = True
    else:
        is_available = False

    try:
        duration = int(request.form.get('duration'))
    except ValueError:
        if frontend:
            session['message'] = ConstErrs.duration
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.duration)

    try:
        production_year = int(request.form.get('production_year'))
    except ValueError:
        if frontend:
            session['message'] = ConstErrs.production_year
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.production_year)

    try:
        imdb_rating = float(request.form.get('imdb_rating'))
    except ValueError:
        if frontend:
            session['message'] = ConstErrs.imdb
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.imdb)

    try:
        validate_movie_data(title, description, duration, production_year, production_country, actors,
                            cover_image, audio_languages, genre, imdb_rating, is_available)
    except InputError as e:
        if frontend:
            session['message'] = str(e)
            return redirect(url_for('index'))
        else:
            return json_false_status(str(e))

    genre_list = [genre.strip() for genre in genre.split(',')]
    audio_languages_list = [language.strip() for language in audio_languages.split(',')]
    actors_list = [actor.strip() for actor in actors.split(',')]

    new_movie = create_movie(title, description, duration, production_year, production_country, actors_list,
                             cover_image, audio_languages_list, genre_list, imdb_rating, is_available)

    try:
        update_result = movie_collection.replace_one({'_id': ObjectId(object_id)}, new_movie)
    except InvalidId:
        if frontend:
            session['message'] = ConstErrs.object_not_found
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.object_not_found)

    if update_result.modified_count < 1:
        if frontend:
            session['message'] = ConstErrs.object_not_found
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.object_not_found)

    if frontend:
        session['message'] = "Movie successfully updated"
        return redirect(url_for('index'))
    else:
        return jsonify({"status": True})


@app.route('/list/')
def list_entries():
    '''Lists all movies in the database.'''

    app.logger.info("Page accessed: List entries")

    movies_cursor = movie_collection.find({})
    movies_dict = {str(entry.get('_id')): entry.get('title') for entry in movies_cursor}

    return jsonify(movies_dict)


@app.route('/view/', methods=['GET'])
def view():
    '''Returns a movie as a JSON object. Movie specified with id argument.'''

    app.logger.info("Page accessed: View")

    object_id = request.args.get('id')

    if not object_id:
        return json_false_status(ConstErrs.object_id)

    try:
        movie = movie_collection.find_one({'_id': ObjectId(object_id)})
    except InvalidId:
        return json_false_status(ConstErrs.object_not_found)

    if movie is None:
        return json_false_status(ConstErrs.object_not_found)

    movie['_id'] = str(movie['_id'])

    return jsonify(movie)


@app.route('/view_all/')
def view_all():
    '''Returns all movies as a list of JSON objects.'''

    app.logger.info("Page accessed: View all")

    movies_cursor = movie_collection.find({})
    movies_list = [entry for entry in movies_cursor]
    for entry in movies_list:
        entry['_id'] = str(entry['_id'])

    return jsonify(movies_list)


@app.route('/delete/')
def delete():
    '''Deletes a movie specified with id argument.'''

    # If frontend is set, user will be redirected after processing the request
    # instead of sending JSON response
    frontend = request.args.get('frontend') == "yes"

    app.logger.info("Page accessed: Delete")

    object_id = request.args.get('id')
    if not object_id:
        if frontend:
            session['message'] = ConstErrs.object_id
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.object_id)

    try:
        delete_result = movie_collection.delete_one({'_id': ObjectId(object_id)})
    except InvalidId:
        if frontend:
            session['message'] = ConstErrs.object_not_found
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.object_not_found)

    if delete_result.deleted_count < 1:
        if frontend:
            session['message'] = ConstErrs.object_not_found
            return redirect(url_for('index'))
        else:
            return json_false_status(ConstErrs.object_not_found)

    if frontend:
        session['message'] = "Item successfully deleted"
        return redirect(url_for('index'))
    else:
        return jsonify({"status": True})


@app.errorhandler(404)
def not_found(error):
    '''Error 404 view.'''

    _ = error
    return "404: Page not found"


if __name__ == '__main__':
    '''Runs the web application.'''

    app.config['DEBUG'] = True
    app.config['JSON_AS_ASCII'] = False
    app.secret_key = 'my_secret_key_f6e9GeR'
    app.config['SESSION_TYPE'] = 'filesystem'

    log_handler = RotatingFileHandler("info.log", maxBytes=10000, backupCount=1)
    log_handler.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
