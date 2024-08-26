import asyncio
import websockets
import json
from classes import Game,Character,Pawn,Hero1,Hero2


# List of connected clients
connected_clients = []


game = Game()

async def handler(websocket):
    global game
    turnA = True
    history = ''
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'move':
                current_player = 'A' if turnA else 'B'
                # Perform the move in the game
                success = game.move_character(current_player, data['character'], data['direction'])
                if success:
                    # Switch turns
                    turnA = not turnA
                    history = history + '\n' +current_player + '-' + data['character'] + ':' + data['direction'] + '\n'
                        
                    # Send the updated game state and current turn to the client
                    response = {
                        'type': 'board',
                        'data': game.get_game_state(),
                        'curr': 'A' if turnA else 'B',
                        'history' : history
                    }
                    await websocket.send(json.dumps(response))
                    l = []
                    for c in game.players['A' if turnA else 'B']:
                        l.append(c.name)
                    data = json.dumps({'type' : 'characters','data':l})
                    if(len(l) == 0):
                        await websocket.send(json.dumps({'type':'over'}))
                        
                    await websocket.send(data)
                else:
                    # Handle move failure if needed
                    response = {
                        'type': 'error',
                        'message': 'Invalid move'
                    }
                    await websocket.send(json.dumps(response))
            elif data['type'] == 'init':
                # Check which pieces to use based on player_id
                player_a_p = data['playerA_pieces']
                player_b_p = data['playerB_pieces']
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
                await websocket.send(data)
            elif data['type'] == 'newGame':
                game = Game()

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
