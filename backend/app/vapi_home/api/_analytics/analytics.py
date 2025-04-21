from typing import List, Dict, Any
from vapi import AnalyticsQuery
from ..client import get_client

def get_analytics_data(queries: List[AnalyticsQuery]) -> Dict[str, Any]:
    """
    Fetches analytics data from the Vapi API using the SDK.

    Args:
        queries (List[AnalyticsQuery]): List of analytics queries to execute.

    Returns:
        Dict[str, Any]: The analytics data from the API.

    Raises:
        Exception: If there's an error fetching the analytics data.
    """
    try:
        client = get_client()
        return client.analytics.get(queries=queries)
    except Exception as e:
        raise Exception(f"Failed to fetch analytics data: {str(e)}")