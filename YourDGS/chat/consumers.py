from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync
from.models import Stock




class EchoConsumer(SyncConsumer):
    def websocket_connect(self,event):
        self.room_name = 'broadcast'
        self.send({
            'type': 'websocket.accept'
        })
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
        print(f'[{self.channel_name}] - You are now connected')



    def websocket_receive(self,event):
        print(f'[{self.channel_name}] - Message received - {event["text"]}')
        mainmal=event["text"]
        self.name=mainmal.split('~')[1]
        self.message=mainmal.split('~')[0]

        stock=Stock(name=self.name,message=self.message)
        print(stock)
        stock.save()

        async_to_sync(self.channel_layer.group_send)(self.room_name,
        {
            'type': 'websocket.message',
            'text': event.get('text'),
        }
        )

    def websocket_message(self,event):
        print(f'[{self.channel_name}] - Message send - {event["text"]}')
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    def websocket_disconnect(self,event):
        print(f'[{self.channel_name}] - Disconnected')
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)


        # f"tor mal tuy le {event.get('text')}"