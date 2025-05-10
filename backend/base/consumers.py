
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

class AgentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.hostname = self.scope['url_route']['kwargs']['hostname']
        self.group_name = f'agent_{self.hostname}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        systems_data = await self.get_all_systems_data()
        await self.send(text_data=json.dumps({"type": "initial_data", "systems": systems_data}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_process_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
        
        
    @sync_to_async
    def get_all_systems_data(self):
        from .models import SystemDetail
        from django.forms.models import model_to_dict
        systems = SystemDetail.objects.prefetch_related('processes').all()
        data = []       
        for system in systems:

            system_dict = {
                'system_detail': model_to_dict(system),
                # 'process_detail': [
                #     model_to_dict(proc) for proc in system.processes.all()
                # ]
            }
            data.append(system_dict)
        
        return data


    