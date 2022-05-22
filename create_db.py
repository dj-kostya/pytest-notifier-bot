import sqlite3


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        return e


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        return e


def create_database(database_name):
    database = database_name

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
    id                     INTEGER       PRIMARY KEY AUTOINCREMENT,
    user_id                VARCHAR (255) NOT NULL,
    status                 BOOLEAN       DEFAULT (TRUE)
                                         NOT NULL,
    my_path                TEXT,
    notifications_period   INTEGER       DEFAULT (300)
                                         NOT NULL,
    checks_since_last      INTEGER       DEFAULT (1)
                                         NOT NULL,
    failures_period        INTEGER       NOT NULL
                                         DEFAULT (30),
    failures_since_last    INTEGER       DEFAULT (1)
                                         NOT NULL,
    detect_failures        BOOLEAN       NOT NULL
                                         DEFAULT (TRUE),
    failure_mute           BOOLEAN       DEFAULT (FALSE)
                                         NOT NULL
);
 """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create users table
        create_table(conn, sql_create_users_table)
        conn.close()
    else:
        return 'Error! cannot create the database connection.'
