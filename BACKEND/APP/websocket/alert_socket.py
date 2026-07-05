import asyncio
import json

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from APP.redis_client import get_redis

router = APIRouter()

# Redis pub/sub channel used to fan alerts out across every API replica.
# Every replica subscribes to this channel (see redis_listener below) and
# delivers incoming messages only to the WebSocket clients connected to
# itself — that's what makes this safe to run behind a load balancer with
# N replicas, unlike keeping active_connections in memory alone.
ALERTS_CHANNEL = "fraud_alerts_channel"


class ConnectionManager:

    def __init__(self):

        self.active_connections = []

    async def connect(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections.append(
            websocket
        )

        print(
            f"Client Connected | Total: {len(self.active_connections)}"
        )

    def disconnect(
        self,
        websocket: WebSocket
    ):

        if websocket in self.active_connections:

            self.active_connections.remove(
                websocket
            )

        print(
            f"Client Disconnected | Total: {len(self.active_connections)}"
        )

    async def send_personal_message(
        self,
        message: dict,
        websocket: WebSocket
    ):

        await websocket.send_json(
            message
        )

    async def broadcast(self, message: dict):
        """
        Publishes to Redis rather than writing to sockets directly. Every
        replica (including this one) picks the message back up via its
        own redis_listener task and delivers it to its own local clients.
        This is what makes broadcast() correct regardless of which
        process called it — an API request handler, a background scan,
        or a separate Kafka consumer process that has no WebSocket
        connections of its own at all.
        """
        try:
            redis = get_redis()
            await redis.publish(ALERTS_CHANNEL, json.dumps(message, default=str))
        except Exception as exc:
            # Never let a Redis hiccup break the caller (e.g. a money
            # transfer that's trying to raise a fraud alert).
            print(f"[alert_socket] failed to publish to Redis: {exc}")

    async def _deliver_local(self, message: dict):
        """
        Sends message to the WebSocket clients connected to THIS process
        only. Called exclusively by redis_listener, never directly by
        application code — application code should call broadcast().
        """
        disconnected = []

        for connection in self.active_connections:

            try:

                await connection.send_json(
                    message
                )

            except Exception:

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            self.disconnect(
                connection
            )


manager = ConnectionManager()


async def redis_listener():
    """
    Runs for the lifetime of the app (started from main.py's lifespan).
    Subscribes to ALERTS_CHANNEL and hands every message to this
    process's local WebSocket clients. Retries the subscription with a
    backoff if Redis is briefly unavailable, instead of dying and leaving
    this replica's clients permanently silent.
    """
    redis = get_redis()

    while True:
        try:
            pubsub = redis.pubsub()
            await pubsub.subscribe(ALERTS_CHANNEL)
            print(f"[alert_socket] subscribed to Redis channel '{ALERTS_CHANNEL}'")

            async for message in pubsub.listen():
                if message["type"] != "message":
                    continue
                try:
                    data = json.loads(message["data"])
                except (TypeError, ValueError):
                    continue
                await manager._deliver_local(data)

        except asyncio.CancelledError:
            raise
        except Exception as exc:
            print(f"[alert_socket] redis_listener error, retrying in 5s: {exc}")
            await asyncio.sleep(5)


@router.websocket("/ws/alerts")
async def websocket_endpoint(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )
