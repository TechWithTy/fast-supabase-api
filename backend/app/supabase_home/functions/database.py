from typing import Any

from app.supabase_home import get_supabase_client
from .._service import SupabaseService


class SupabaseDatabaseService(SupabaseService):
    """
    Service for interacting with Supabase Database (PostgreSQL) API.

    This class provides methods for database operations using Supabase's
    RESTful API for PostgreSQL.
    """
    def _configure_service(self):
        """Initialize auth-specific client"""
        self.auth = self.raw.table  # Gets the GoTrue client
        self.rpc = self.raw.rpc     # Assign the method, not the result of calling it
    
    def fetch_data(
        self,
        table: str,
        auth_token: str | None = None,
        select: str = "*",
        filters: dict[str, Any] | None = None,
        order: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch data from a table with optional filtering, ordering, and pagination.

        Args:
            table: Table name
            auth_token: Optional JWT token for authenticated requests
            select: Columns to select (default: "*")
            filters: Optional filters as dictionary
            order: Optional order by clause
            limit: Optional limit of rows to return
            offset: Optional offset for pagination

        Returns:
            list of rows as dictionaries
        """
        endpoint = f"/rest/v1/{table}"
        params = {"select": select}

        # Add filters if provided
        if filters:
            for key, value in filters.items():
                # Format filter with eq operator for Supabase REST API
                params[f"{key}"] = f"eq.{value}"

        # Add ordering if provided
        if order:
            params["order"] = order

        # Add pagination if provided
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        return self._make_request(
            method="GET",
            endpoint=endpoint,
            auth_token=auth_token,
            params=params,
            headers={"Prefer": "return=representation"},
        )

    def insert_data(
        self,
        table: str,
        data: dict[str, Any] | list[dict[str, Any]],
        auth_token: str | None = None,
        upsert: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Insert data into a table.

        Args:
            table: Table name
            data: Data to insert (single record or list of records)
            auth_token: Optional JWT token for authenticated requests
            upsert: Whether to upsert (update on conflict)

        Returns:
            Inserted data
        """
        endpoint = f"/rest/v1/{table}"
        headers = {"Prefer": "return=representation"}

        if upsert:
            headers["Prefer"] = "resolution=merge-duplicates,return=representation"

        return self._make_request(
            method="POST",
            endpoint=endpoint,
            auth_token=auth_token,
            data=data,
            headers=headers,
        )

    def update_data(
        self,
        table: str,
        data: dict[str, Any],
        filters: dict[str, Any],
        auth_token: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Update data in a table.

        Args:
            table: Table name
            data: Data to update
            filters: Filters to identify rows to update
            auth_token: Optional JWT token for authenticated requests

        Returns:
            Updated data
        """
        endpoint = f"/rest/v1/{table}"
        params = {}

        # Format filters with eq operator for Supabase REST API
        if filters:
            for key, value in filters.items():
                params[f"{key}"] = f"eq.{value}"

        return self._make_request(
            method="PATCH",
            endpoint=endpoint,
            auth_token=auth_token,
            data=data,
            params=params,
            headers={"Prefer": "return=representation"},
        )

    def upsert_data(
        self,
        table: str,
        data: dict[str, Any] | list[dict[str, Any]],
        auth_token: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Upsert data in a table (insert or update).

        Args:
            table: Table name
            data: Data to upsert
            auth_token: Optional JWT token for authenticated requests

        Returns:
            Upserted data
        """
        return self.insert_data(table, data, auth_token, upsert=True)

    def delete_data(
        self, table: str, filters: dict[str, Any], auth_token: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Delete data from a table.

        Args:
            table: Table name
            filters: Filters to identify rows to delete
            auth_token: Optional JWT token for authenticated requests

        Returns:
            Deleted data
        """
        endpoint = f"/rest/v1/{table}"
        params = {}

        # Format filters with eq operator for Supabase REST API
        if filters:
            for key, value in filters.items():
                params[f"{key}"] = f"eq.{value}"

        return self._make_request(
            method="DELETE",
            endpoint=endpoint,
            auth_token=auth_token,
            params=params,
            headers={"Prefer": "return=representation"},
        )

    def call_function(
        self,
        function_name: str,
        params: dict[str, Any] | None = None,
        auth_token: str | None = None,
    ) -> Any:
        """
        Call a PostgreSQL function.

        Args:
            function_name: Function name
            params: Function parameters
            auth_token: Optional JWT token for authenticated requests

        Returns:
            Function result
        """
        endpoint = f"/rest/v1/rpc/{function_name}"

        return self._make_request(
            method="POST", endpoint=endpoint, auth_token=auth_token, data=params or {}
        )

    def create_test_table(
        self, table: str, auth_token: str | None = None, is_admin: bool = True
    ) -> dict[str, Any]:
        """
        Create a simple test table for integration tests.

        Args:
            table: Table name to create
            auth_token: Optional JWT token for authenticated requests
            is_admin: Whether to use service role key (admin access)

        Returns:
            Response from the API
        """
        # SQL to create a simple test table
        sql = f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            user_id TEXT
        );
        -- Set up RLS policies
        ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;
        -- Create policy to allow all operations for authenticated users
        DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON {table};
        CREATE POLICY "Allow all operations for authenticated users"
        ON {table}
        FOR ALL
        TO authenticated
        USING (true)
        WITH CHECK (true);
        """

        # Execute the SQL using the rpc endpoint
        return self._make_request(
            method="POST",
            endpoint="/rest/v1/rpc/exec_sql",
            auth_token=auth_token,
            is_admin=is_admin,  # Must use admin privileges to create tables
            data={"query": sql},
        )

    def delete_table(
        self, table: str, auth_token: str | None = None, is_admin: bool = True
    ) -> dict[str, Any]:
        """
        Delete a table from the database.

        Args:
            table: Table name to delete
            auth_token: Optional JWT token for authenticated requests
            is_admin: Whether to use service role key (admin access)

        Returns:
            Response from the API
        """
        # SQL to drop the table
        sql = f"DROP TABLE IF EXISTS {table};"

        # Execute the SQL using the rpc endpoint
        return self._make_request(
            method="POST",
            endpoint="/rest/v1/rpc/exec_sql",
            auth_token=auth_token,
            is_admin=is_admin,  # Must use admin privileges to delete tables
            data={"query": sql},
        )
