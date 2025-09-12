import asyncio
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_status(order_id: int, status: str):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('staff-orders', {
        'type': 'order_status_update',
        'data': {'order_id': order_id, 'status': status}
    })
