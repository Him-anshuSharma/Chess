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

    def add_player(self, player_id, character_names):
        # Convert character names to Character objects
        temp = character_names.split(',')
        character_list = []
    
        # Convert character names to Character objects
        pc = 1;
        for c in temp:
            if(c.upper() == 'P'):
                character_list.append(f"P{pc}")
                pc = pc + 1
            else:
                character_list.append(c.upper())
        characters = []
        for c in character_list:
            if 'P' in c:
                characters.append(Pawn(player_id=player_id, name=c))
            elif c == 'H1':
                characters.append(Hero1(player_id=player_id, name=c))
            else:
                characters.append(Hero2(player_id=player_id, name=c))
        
        print(f"Player ID: {player_id}, Character Names: {character_list}")
        print(f"Number of characters: {len(characters)}")
        
        # Add the player with their characters to the players dictionary
        self.players[player_id] = characters
        
        # Place the characters on the board
        self.place_characters(player_id)



    def place_characters(self, player_id):
        row = 0 if len(self.players) == 1 else BOARD_SIZE - 1
        i = 0
        pc = 1
        print(len(self.players[player_id]))
        for character in self.players[player_id]:
            print(i)
            character.set_position(row, i)
            if(character.name == 'P' or character.name == 'p'):
                self.board[row][i] = f'{player_id}-{character.name.upper()}{pc}'
                pc = pc+1
            else:
                 self.board[row][i] = f'{player_id}-{character.name.upper()}'
            i = i+1

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
        if(player_id == 'A'):
            if(direction.upper() == 'F') :
                direction = 'B'
            elif(direction.upper() == 'B'):
                direction = 'F'
            elif(direction.upper() == 'BR'):
                direction = 'FR'
            elif(direction.upper() == 'FR'):
                direction = 'BR'
            elif(direction.upper() == 'BL'):
                direction = 'FL'
            elif(direction.upper() == 'FL'):
                direction = 'BL'

        print(direction)        

        character = next(c for c in self.players[player_id] if c.name == character_name)
        new_position = character.move(direction)
        if self.is_valid_move(player_id, character_name, new_position):
            old_x, old_y = character.position
            new_x, new_y = new_position
            cell = self.board[new_x][new_y]
            # Clear the old position
            self.board[old_x][old_y] = ''
            if(cell != ''):
                temp = cell.split('-')
                playerid = temp[0]
                piece = temp[1]
                for p in self.players[playerid]:
                    if(p.name == piece):
                        self.players[playerid].remove(p)
                        break

            # Update character's position
            character.set_position(new_x, new_y)
            # Place character in new position
            self.board[new_x][new_y] = f'{player_id}-{character.name}'
            return True
        else:
            return False

    def get_game_state(self):
        return self.board