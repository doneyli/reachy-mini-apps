"""ClickHouse client wrapper for Reachy Mini applications."""

from typing import Any

import clickhouse_connect


class ClickHouseClient:
    """Wrapper around clickhouse-connect for application use."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8123,
        username: str = "default",
        password: str = "",
        database: str = "default",
    ):
        """
        Initialize ClickHouse client.

        Args:
            host: ClickHouse server host.
            port: ClickHouse HTTP port.
            username: Database username.
            password: Database password.
            database: Default database name.
        """
        self.client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
        )

    def insert(self, table: str, data: list[dict[str, Any]]) -> None:
        """
        Insert rows into a table.

        Args:
            table: Target table name.
            data: List of row dictionaries.
        """
        if not data:
            return
        columns = list(data[0].keys())
        rows = [[row[col] for col in columns] for row in data]
        self.client.insert(table, rows, column_names=columns)

    def query(self, sql: str) -> list[dict[str, Any]]:
        """
        Execute a query and return results as dictionaries.

        Args:
            sql: SQL query string.

        Returns:
            List of row dictionaries.
        """
        result = self.client.query(sql)
        columns = result.column_names
        return [dict(zip(columns, row)) for row in result.result_rows]

    def close(self) -> None:
        """Close the client connection."""
        self.client.close()
