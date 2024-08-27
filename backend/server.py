import asyncio
import websockets
import json
from classes import Game, Character, Pawn, Hero1, Hero2

# List of connected clients
connected_clients = []

game = Game()
turnA = True
history = ''

async def handle_move(websocket, data):
    global turnA, history
    current_player = 'A' if turnA else 'B'
    success = game.move_character(current_player, data['character'], data['direction'])
    if success:
        turnA = not turnA
        history += f'\n{current_player}-{data["character"]}:{data["direction"]}\n'
        response = {
            'type': 'board',
            'data': game.get_game_state(),
            'curr': 'A' if turnA else 'B',
            'history': history
        }
        await websocket.send(json.dumps(response))
        l = [c.name for c in game.players['A' if turnA else 'B']]
        await websocket.send(json.dumps({'type': 'characters', 'data': l}))
        if not l:
            await websocket.send(json.dumps({'type': 'over'}))
    else:
        response = {'type': 'error', 'message': 'Invalid move'}
        await websocket.send(json.dumps(response))

async def handle_init(websocket, data):
    player_a_p = data['playerA_pieces']
    player_b_p = data['playerB_pieces']
    game.add_player(player_id='A', character_names=player_a_p)
    game.add_player(player_id='B', character_names=player_b_p)
    await websocket.send(json.dumps({'mssg': 'success'}))

async def handle_get_board(websocket):
    await websocket.send(json.dumps({
        'type': 'board',
        'data': game.get_game_state(),
        'curr': 'A' if turnA else 'B'
    }))

async def handle_characters(websocket, data):
    l = [c.name for c in game.players[data['id']]]
    await websocket.send(json.dumps({'type': 'characters', 'data': l}))

async def handle_new_game():
    global game
    game = Game()

async def handler(websocket):
    global turnA, history
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'move':
                await handle_move(websocket, data)
            elif data['type'] == 'init':
                await handle_init(websocket, data)
            elif data['type'] == 'getBoard':
                await handle_get_board(websocket)
            elif data['type'] == 'characters':
                await handle_characters(websocket, data)
            elif data['type'] == 'newGame':
                await handle_new_game()
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
