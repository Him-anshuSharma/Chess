import json

# Game board dimensions
BOARD_SIZE = 5

# Character classes
class Character:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.position = None

    def set_position(self, x, y):
        self.position = (x, y)

    def move(self, direction):
        raise NotImplementedError("This method should be overridden by subclasses")

class Pawn(Character):
    def move(self, direction):
        x, y = self.position
        if direction == 'L':  # Left
            y -= 1
        elif direction == 'R':  # Right
            y += 1
        elif direction == 'F':  # Forward
            x -= 1
        elif direction == 'B':  # Backward
            x += 1
        return (x, y)

class Hero1(Character):
    def move(self, direction):
        x, y = self.position
        if direction == 'L':  # Left
            y -= 2
        elif direction == 'R':  # Right
            y += 2
        elif direction == 'F':  # Forward
            x -= 2
        elif direction == 'B':  # Backward
            x += 2
        return (x, y)

class Hero2(Character):
    def move(self, direction):
        x, y = self.position
        if direction == 'FL':  # Forward-Left
            x -= 2
            y -= 2
        elif direction == 'FR':  # Forward-Right
            x -= 2
            y += 2
        elif direction == 'BL':  # Backward-Left
            x += 2
            y -= 2
        elif direction == 'BR':  # Backward-Right
            x += 2
            y += 2
        return (x, y)

# Game class to manage the game state
class Game:
    def __init__(self):
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.players = {}
        self.turn = None

    def add_player(self, player_id, characters):
        self.players[player_id] = characters
        self.place_characters(player_id, characters)

    def place_characters(self, player_id, characters):
        row = 0 if player_id == 'A' else BOARD_SIZE - 1
        for i, character in enumerate(characters):
            character.set_position(row, i)
            self.board[row][i] = f'{player_id}-{character.name}'

    def is_valid_move(self, player_id, character_name, new_position):
        x, y = new_position
        # Check if the move is within bounds
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            return False
        # Check if the move is not onto a friendly character
        if self.board[x][y].startswith(player_id):
            return False
        return True

    def move_character(self, player_id, character_name, direction):
        character = next(c for c in self.players[player_id] if c.name == character_name)
        new_position = character.move(direction)
        if self.is_valid_move(player_id, character_name, new_position):
            old_x, old_y = character.position
            new_x, new_y = new_position
            # Clear the old position
            self.board[old_x][old_y] = ''
            if(self.board[new_x][new_y] != ''):
                temp = self.board[new_x][new_y].split('-')
                playerid = temp[0]
                piece = temp[1]
                for p in self.players.keys():
                    if(p == playerid):
                        for c in self.players[p]:
                            if(c == piece):
                                self.players[p].remove(c)



            # Update character's position
            character.set_position(new_x, new_y)
            # Place character in new position
            self.board[new_x][new_y] = f'{player_id}-{character.name}'
            return True
        else:
            return False

    def get_game_state(self):
        json_temp = json.dumps(self.board)
        return json_temp