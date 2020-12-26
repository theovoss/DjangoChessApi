import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from chess.chess import Chess
from .models import Game
from .helpers import get_displayable_board, get_displayable_history


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        message = json.loads(text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        game_id = message['game_id']

        game = await self.get_game(game_id)

        chess = Chess(game.data)

        if not await self.is_my_turn(game_id, self.scope["user"]):
            await self.send_update(game)
        else:
            chess = Chess(game.data)
            chess.move(self.convert_to_position(message['start']), self.convert_to_position(message['destination']))

            game = await self.save_game(game, chess)
            await self.send_update(game)

    def convert_to_position(self, position):
        return (int(position['row']), int(position['column']))

    async def send_update(self, game):
        chess = Chess(game.data)
        await self.send(text_data=json.dumps({
            'board': get_displayable_board(chess.board),
            'history': get_displayable_history(chess),
            'color': game.turn_color
        }))

    @database_sync_to_async
    def is_my_turn(self, pk, user):
        is_my_turn = Game.objects.get(pk=pk).is_my_turn(user)
        return is_my_turn

    @database_sync_to_async
    def get_game(self, pk):
        return Game.objects.get(pk=pk)

    @database_sync_to_async
    def save_game(self, game, chess):
        game.data = chess.export()
        game.save()
        return game
