"""
SQLite helper for direct database assertions in API tests.
"""

import sqlite3
from pathlib import Path

from configs.settings import DATABASE_PATH


class SQLClient:
    """Run read queries against the Job Tracker SQLite database."""

    def __init__(self, database_path=DATABASE_PATH):
        """
        Initialize the client with a path to the SQLite database file.

        Args:
            database_path: Filesystem path to the Job Tracker database.
        """
        self.database_path = database_path

    def execute_query(self, sql):
        """
        Execute a SQL query and return matching rows as dictionaries.

        Args:
            sql: SQL statement to run against the database.

        Returns:
            List of row dicts keyed by column name.

        Raises:
            Exception: When no database path is configured.
            FileNotFoundError: When the database file does not exist.
        """
        # verify the database file exists
        if not self.database_path:
            raise Exception(f"The database path is not set. Please set environment variable: DATABASE_PATH")
            
        database_file = Path(self.database_path)


        if not database_file.exists():
            raise FileNotFoundError(f"The database file provided does not exist. DB File: {self.database_path}")

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [dict(row) for row in rows]
