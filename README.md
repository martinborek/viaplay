# Viaplay movie database

Author: Martin Borek (mborekcz@gmail.com)

## How to run
The application can be simply deployed with docker-compose. To build and run containers with MongoDB and web application, run: `$ docker-compose up --build`
Web application is running at http://localhost/`
The application has a very simple frontend that is accessible at `http://localhost/frontend/`
Default movie entry can be added with ``http://localhost/add_default/`

## Backend
Backend provides an API that expects input in form of POST and GET requests, responding with JSON objects.
API consits of:
Adding a movie: `http://localhost/add/`
Updating a movie: `http://localhost/update/`
Deleting a movie: `http://localhost/delete/`
Listing movies: `http://localhost/list/`
Showing a movie entry: `http://localhost/view/`
Showing all movies: `http://localhost/view_all/`


## Technologies used
The application is written in Python3 using Flask framework and MongoDB. MongoDB. Advantage of these tools is their simplicity, allowing for easy development. All of them are yet very powerful.

## Improvements
Since the functionality and especially the frontend are very basic, there is a lot of room for improvements. The application could include sorting, filtering, content rating and so on.
