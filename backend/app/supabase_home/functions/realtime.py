import logging
from collections.abc import Callable
from typing import Any

from fastapi import HTTPException

from .._service import SupabaseService

logger = logging.getLogger(__name__)


class SupabaseRealtimeService(SupabaseService):
    """
    Service for managing Supabase Realtime subscriptions.

    This class provides methods for creating and managing Realtime subscriptions
    using server-side websocket connections.
    """

    def _configure_service(self):
        """Initialize Realtime clients"""
        self.realtime = self.raw.realtime  # Main client
        self.active_channels = {}  # Track active subscriptions

    async def subscribe_to_channel(
        self, channel: str, event: str = "*", callback: Callable | None = None
    ) -> Any:
        """
        Subscribe to a Realtime channel.

        Args:
            channel: Channel name
            event: Event to subscribe to (default: "*" for all events)
            callback: Optional callback function for events

        Returns:
            Subscription object
        """
        if not self.client.is_connected():
            await self.client.connect()

        try:
            channel_obj = self.client.channel(channel)
            if callback:
                channel_obj.on(event, callback)

            subscription = await channel_obj.subscribe()
            self.active_channels[channel] = subscription
            return subscription

        except Exception as e:
            logger.error(f"Realtime error: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Failed to subscribe to {channel}: {str(e)}"
            )

    async def unsubscribe_from_channel(self, channel: str) -> None:
        """
        Unsubscribe from a Realtime channel.

        Args:
            channel: Channel name
        """
        if channel in self.active_channels:
            try:
                await self.active_channels[channel].unsubscribe()
                del self.active_channels[channel]
            except Exception as e:
                logger.error(f"Unsubscribe error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to unsubscribe from {channel}: {str(e)}",
                )

    async def unsubscribe_all(self) -> None:
        """
        Unsubscribe from all Realtime channels.
        """
        for channel in list(self.active_channels.keys()):
            await self.unsubscribe_from_channel(channel)

    def get_channels(self) -> dict[str, Any]:
        """
        Retrieve all subscribed channels.

        Returns:
            dict containing list of subscribed channels
        """
        return {"channels": list(self.active_channels.keys())}

    async def broadcast_message(
        self, channel: str, payload: dict[str, Any], event: str = "broadcast"
    ) -> None:
        """
        Broadcast a message to a channel.

        Args:
            channel: Channel name
            payload: Message payload
            event: Event name (default: "broadcast")
        """
        if channel in self.active_channels:
            try:
                await self.active_channels[channel].send(
                    type=event, event=event, payload=payload
                )
            except Exception as e:
                logger.error(f"Broadcast error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to broadcast to {channel}: {str(e)}",
                )
        else:
            raise ValueError(f"Channel '{channel}' is not subscribed")

    async def subscribe_to_private_channel(self, channel: str, user_token: str) -> Any:
        """
        Subscribe to a private Realtime channel using RLS.

        Args:
            channel: Channel name
            user_token: User's authentication token for RLS

        Returns:
            Subscription object
        """
        if not self.client.is_connected():
            await self.client.connect()

        try:
            private_channel = self.client.channel(
                channel,
                {
                    "config": {"token": user_token}  # RLS token
                },
            )
            subscription = await private_channel.subscribe()
            self.active_channels[channel] = subscription
            return subscription
        except Exception as e:
            logger.error(f"Private channel subscription error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to subscribe to private channel {channel}: {str(e)}",
            )

    def add_callback(self, channel: str, event: str, callback: Callable) -> None:
        """
        Add a callback function to an existing channel subscription.

        Args:
            channel: Channel name
            event: Event to listen for
            callback: Callback function to execute on event
        """
        if channel in self.active_channels:
            self.active_channels[channel].on(event, callback)
        else:
            raise ValueError(f"Channel '{channel}' is not subscribed")

    async def close_all(self) -> None:
        """
        Close all websocket connections and clean up resources.
        """
        try:
            await self.unsubscribe_all()
            if self.client.is_connected():
                await self.client.disconnect()
        except Exception as e:
            logger.warning(f"Cleanup error: {str(e)}")
