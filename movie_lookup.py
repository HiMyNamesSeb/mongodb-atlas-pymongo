"""Look up a movie in the MongoDB Atlas sample_mflix database with PyMongo.

Usage:
    python movie_lookup.py                 # looks up the default title
    python movie_lookup.py "Back to the Future"
"""

import os
import sys

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

DEFAULT_TITLE = "Highwaymen"


def get_client() -> MongoClient:
    """Build a MongoClient from the MONGODB_URI environment variable."""
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    if not uri:
        sys.exit("MONGODB_URI is not set. Copy .env.example to .env and add your connection string.")
    return MongoClient(uri, tlsCAFile=certifi.where())


def find_movie(client: MongoClient, title: str):
    """Return the first movie whose title matches exactly, or None."""
    movies = client.get_database("sample_mflix").get_collection("movies")
    return movies.find_one(
        {"title": title},
        {"_id": 0, "title": 1, "plot": 1, "year": 1},
    )


def print_movie(movie: dict) -> None:
    print("Movie Information")
    print("-----------------")
    print(f"Title: {movie.get('title', 'N/A')}")
    print()
    print(f"Plot: {movie.get('plot', 'N/A')}")
    print()
    print(f"Year: {movie.get('year', 'N/A')}")


def main() -> None:
    title = " ".join(sys.argv[1:]) or DEFAULT_TITLE
    client = get_client()
    try:
        movie = find_movie(client, title)
        if movie:
            print_movie(movie)
        else:
            print(f'No movie found with the title "{title}".')
    except PyMongoError as e:
        sys.exit(f"Database error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
