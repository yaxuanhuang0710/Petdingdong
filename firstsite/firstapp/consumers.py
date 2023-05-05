from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django_redis import get_redis_connection
from django.core.serializers.json import DjangoJSONEncoder
from firstapp.models import Chat
import json
import time
import os, base64, uuid

def save_image(data, filename):
    # 保存图片到本地
    imgdata=base64.b64decode(data)
    with open(filename, "wb") as f:
        f.write(imgdata)

@database_sync_to_async
def save_msg(sender_id, rece_id, message, message_type="text"):
    if message_type == "image":
        image_uniq = '%s.jpg'%str(uuid.uuid4())
        image_file_name = 'firstapp/static/images/%s'%image_uniq
        save_image(message.split("base64,")[1], image_file_name)
        msg_obj = Chat.objects.create(senderNo=sender_id,
                               receiverNo=rece_id,
                               image=image_uniq)
    else:
        msg_obj = Chat.objects.create(senderNo=sender_id,
                               receiverNo=rece_id,
                               text=message)

    return msg_obj

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.f_id = self.scope['url_route']['kwargs']['f_id']
        self.u_id = self.scope['url_route']['kwargs']['u_id']

        self.con = get_redis_connection("default")
        self.con.hset("channel_list", self.u_id, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        self.con.hdel('channels_list', self.u_id, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_data = text_data_json['message']
        message_type = text_data_json['message_type']

        message_obj = await save_msg(self.u_id, self.f_id, message_data, message_type)

        message = json.dumps({
            'message_data': message_data,
            'create_time':message_obj.create_time,
            'user_id':message_obj.senderNo,
            'message_type': message_type,
        }, cls=DjangoJSONEncoder)

        await self.channel_layer.send(
            self.channel_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

        rece_channel_name = self.con.hget("channel_list", self.f_id)
        if rece_channel_name:
            rece_channel_name = rece_channel_name.decode('utf8')
            await self.channel_layer.send(
                rece_channel_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )

    # Receive message from channel
    async def chat_message(self, event):
        message = json.loads(event['message'])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }, cls=DjangoJSONEncoder))
