import asyncio
import websockets
import json
from classes import Game,Character,Pawn,Hero1,Hero2


# List of connected clients
connected_clients = []

myset = set()
game = Game()

async def handler(websocket, path):
    player_id = None
    connected_clients.append(websocket)

    try:
        async for message in websocket:
            data = json.loads(message)
            print("message :",data)
            player_id = data['player_id']
            if data['type'] == 'init':
                if data['player_id'] not in myset:
                    characters = []
                    for char_data in data['characters']:
                        if char_data == 'P':
                            characters.append(Pawn(player_id, f'P{len(characters)+1}'))
                        elif char_data == 'H1':
                            characters.append(Hero1(player_id, f'H1'))
                        elif char_data == 'H2':
                            characters.append(Hero2(player_id, f'H2'))
                    game.add_player(player_id, characters)
                    myset.add(player_id)
                    print("game players " , game.players)
                    if len(game.players) == 2:
                        game.turn = 'A'
                    await broadcast(game.get_game_state())

            elif data['type'] == 'move':
                player_id = data['player_id']
                print(player_id , " " , game.turn)
                if game.turn == player_id:
                    success = game.move_character(player_id, data['character'], data['direction'])
                    print('success ', success)
                    if success:
                        game.turn = 'B' if game.turn == 'A' else 'A'
                        await broadcast(game.get_game_state())
                    else:
                        await websocket.send(json.dumps({'error': 'Invalid move'}))
                else:
                    await websocket.send(json.dumps({'error': 'Not your turn'}))
    except:
        print("invalid handler")

async def broadcast(message):
    for client in connected_clients:
        try:
            await client.send(message)
        except:
            connected_clients.remove(client)

async def main():
    host = "localhost"
    port = 8765
    print(f"Starting server on ws://{host}:{port}")
    async with websockets.serve(handler, host, port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
