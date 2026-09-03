import psycopg2
from psycopg2 import Error
from psycopg2.extras import DictCursor
from typing import Any, Generator
from contextlib import contextmanager

from settings import DB_CONFIG

class DBConnection:
    def __init__(self):
        self._connection = None
        self._connect()

    def _connect(self):
        """Establishes a connection to the PostgreSQL database."""
        try:
            self._connection = psycopg2.connect(**DB_CONFIG)
            self._connection.autocommit = False # We'll manage transactions manually
            print("Conexión a PostgreSQL exitosa.")
        except Error as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            # In a real application, you might want to log this error
            # and potentially raise a custom exception or handle it gracefully.
            self._connection = None

    @property
    def connection(self):
        """Returns the active database connection, reconnecting if necessary."""
        if self._connection is None or self._connection.closed:
            print("Reconectando a la base de datos...")
            self._connect()
        return self._connection

    @contextmanager
    def get_cursor(self, dictionary: bool = False) -> Generator[Any, None, None]:
        """
        Provides a database cursor, optionally as a dictionary cursor.
        Ensures the cursor is closed after use.
        """
        cursor = None
        try:
            if dictionary:
                cursor = self.connection.cursor(cursor_factory=DictCursor)
            else:
                cursor = self.connection.cursor()
            yield cursor
        finally:
            if cursor:
                cursor.close()