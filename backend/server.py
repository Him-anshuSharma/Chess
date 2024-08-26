import asyncio
import websockets
import json
from classes import Game,Character,Pawn,Hero1,Hero2


# List of connected clients
connected_clients = []

myset = set()
game = Game()

async def handler(websocket):
    turnA = True
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'move':
                turnA = not turnA
                await websocket.send(json.dumps({'type' : 'board','data':game.get_game_state(),'curr':'A' if turnA else 'B'}))
                pass
            elif data['type'] == 'init':
                # Check which pieces to use based on player_id
                player_a_p = data['playerA_pieces']
                player_b_p = data['playerB_pieces']
                print(player_a_p,player_b_p)
                game.add_player(player_id='A', character_names=player_a_p)
                game.add_player(player_id='B', character_names=player_b_p)
                await websocket.send(json.dumps({'mssg': 'success'}))
            elif data['type'] == 'getBoard':
                await websocket.send(json.dumps({'type' : 'board','data':game.get_game_state(),'curr':'A' if turnA else 'B'}))
            elif data['type'] == 'characters':
                l = []
                for c in game.players[data['id']]:
                    l.append(c.name)
                data = json.dumps({'type' : 'characters','data':l})
                print(data)
                await websocket.send(data)

    except Exception as e:
        print(f"Exception occurred: {e}")
        await websocket.send(json.dumps({'error': 'An error occurred'}))

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
