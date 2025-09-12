import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class StaffOrdersConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('staff-orders', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('staff-orders', self.channel_name)

    async def order_status_update(self, event):
        await self.send_json(event['data'])
