import sqlite3
from sqlite3 import Error


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


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("""SELECT title
                FROM external_metadata_items
                WHERE title NOT LIKE ""
                AND id NOT IN (SELECT id FROM metadata_items)""")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    database = r"/var/snap/plexmediaserver/common/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_tasks(conn)


if __name__ == '__main__':
    main()
