import sqlite3
from sqlite3 import Error
import re

output_hd_movies = open("./movie_output/hd_movies.txt", "w+")
output_movies = open("./movie_output/all_movies.txt", "w+")
output_4k_movies = open("./movie_output/4k_movies.txt", "w+")
output_anime_movies = open("./movie_output/anime_movies.txt", "w+")
output_short_movies = open("./movie_output/short_movies.txt", "w+")
unmatched_items = open("./movie_output/unmatched_items.txt", "w+")

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as except_err:
        print(except_err)
    return conn


def select_all_movies(conn):
    """
    Query all rows in the media_parts table
    And returns all of the movie paths into
    A file, excluding the extras.
    :param conn: the db connection
    """
    cur = conn.cursor()
    cur.execute("""SELECT title, file
                FROM media_parts
                INNER JOIN external_metadata_items on external_metadata_items.id = media_parts.id
                ORDER BY title""")

    rows = cur.fetchall()

    for row in rows:
        output_movies.write(str(row) + "\n")

def select_4k_movies(conn):
    """
    Query all rows in the media_parts table
    And returns all of the 4K movie paths into
    A file
    """
    cur = conn.cursor()
    cur.execute("""SELECT file
                FROM media_parts
                WHERE file NOT LIKE '%Featurettes%'
                    AND file NOT LIKE '%Deleted Scenes'
                    AND file NOT LIKE '%Interviews%'
                    AND file NOT LIKE '%Anime%'
                    AND file NOT LIKE '%Feature Film%'
                    AND file NOT LIKE '%Shorts%'
                    AND file IS NOT ''""")

    rows = cur.fetchall()

    for row in rows:
        output_4k_movies.write(str(row) + "\n")

def select_hd_movies(conn):
    """
    Query all rows in the media_parts table
    And returns all of the 4K movie paths into
    A file
    """
    cur = conn.cursor()
    cur.execute("""SELECT file
                FROM media_parts
                WHERE file NOT LIKE '%Featurettes%'
                    AND file NOT LIKE '%Deleted Scenes'
                    AND file NOT LIKE '%Interviews%'
                    AND file NOT LIKE '%Movies 4K%'
                    AND file NOT LIKE '%Shorts%'
                    AND file NOT LIKE '%Anime%'
                    AND file IS NOT ''""")

    rows = cur.fetchall()

    for row in rows:
        output_hd_movies.write(str(row) + "\n")

def select_anime_movies(conn):
    """
    Query all rows in the media_parts table
    And returns all of the 4K movie paths into
    A file
    """
    cur = conn.cursor()
    cur.execute("""SELECT file
                FROM media_parts
                WHERE file NOT LIKE '%Featurettes%'
                    AND file NOT LIKE '%Deleted Scenes'
                    AND file NOT LIKE '%Interviews%'
                    AND file NOT LIKE '%Movies 4K%'
                    AND file NOT LIKE '%Feature Film%'
                    AND file NOT LIKE '%Shorts%'
                    AND file IS NOT ''""")

    rows = cur.fetchall()

    for row in rows:
        output_anime_movies.write(str(row) + "\n")

def select_short_movies(conn):
    """
    Query all rows in the media_parts table
    And returns all of the 4K movie paths into
    A file
    """
    cur = conn.cursor()
    cur.execute("""SELECT file
                FROM media_parts
                WHERE file NOT LIKE '%Featurettes%'
                    AND file NOT LIKE '%Deleted Scenes'
                    AND file NOT LIKE '%Interviews%'
                    AND file NOT LIKE '%Movies 4K%'
                    AND file NOT LIKE '%Feature Film%'
                    AND file NOT LIKE '%Anime%'
                    AND file IS NOT ''""")

    rows = cur.fetchall()

    for row in rows:
        output_short_movies.write(str(row) + "\n")

def show_unmatched_items(conn):
    """
    A query that compares the movies IDs in 
    the tables external_metadata_items and
    metadata_items, and then reports the 
    movies that are not in metadata_items.
    """
    cur = conn.cursor()
    cur.execute("""SELECT title
                FROM external_metadata_items
                WHERE title NOT LIKE ""
                AND id NOT IN (SELECT id FROM metadata_items)
                ORDER BY title""")

    rows = cur.fetchall()

    for row in rows:
        unmatched_items.write(str(row) + "\n")


def main():
    database = r"/var/snap/plexmediaserver/common/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_movies(conn)
        select_4k_movies(conn)
        select_hd_movies(conn)
        select_anime_movies(conn)
        select_short_movies(conn)
        show_unmatched_items(conn)


if __name__ == '__main__':
    main()