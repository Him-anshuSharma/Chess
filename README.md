# Turn-Based Game Documentation

## Instructions

1. **Start the Server**
   - Run the server using the following command:
     ```bash
     python3 server.py
     ```

2. **Open the Game**
   - After starting the server, open `intro.html` in your web browser to set up the game.
   - Follow the instructions in `intro.html` to input pieces and start the game.

## `board.html`

### Overview
The `board.html` file is the client-side interface for the turn-based game. It allows players to view the game board, select characters, and make moves. It also includes a history section and a modal for game-over scenarios.

### Key Sections

#### Styles
- **Body:** Centered content with a responsive design.
- **Turn Info:** Displays current turn with large, bold text.
- **Game Container:** Grid layout for the game board, with responsive sizing.
- **Controls:** Includes dropdowns for selecting characters and directions, and a button for making moves.
- **History:** A text area to display the move history.
- **Modal:** Used to show a game-over popup with a button to start a new game.

#### JavaScript
- **WebSocket Connection:** Connects to the server, handles incoming messages, and sends updates.
- **Functions:**
  - `updateBoard(gameState)`: Updates the game board with new state.
  - `updateTurnInfo(turn)`: Updates the current turn display.
  - `makeMove()`: Sends a move command to the server.
  - `updateCharacterOptions(characters)`: Updates the character selection dropdown.
  - `updateHistory(history)`: Updates the history text area.
  - `showGameOverPopup(message)`: Displays a popup when the game is over.
  - `startNewGame()`: Handles the start of a new game and redirects to `intro.html`.

## `intro.html`

### Overview
The `intro.html` file is the setup page for the game. It allows players to input their pieces for Player A and Player B and start the game.

### Key Sections

#### Styles
- **Body:** Centered content with a column layout.
- **Setup Container:** Box for entering player pieces and starting the game, with padding and shadow.

#### JavaScript
- **WebSocket Connection:** Connects to the server and handles responses.
- **Function:**
  - `startGame()`: Sends player piece data to the server and starts the game.

## `server.py`

### Overview
The `server.py` file contains the server-side logic for the game. It handles WebSocket connections, game state management, and communication with clients.

### Key Sections

#### WebSocket Handler
- **Move Handling:** Processes move commands and updates the game state.
- **Initialization:** Sets up the game with pieces for both players.
- **Board Retrieval:** Sends the current game board state.
- **Character List:** Sends the list of available characters for the current player.
- **New Game:** Resets the game state for a new game.

#### Broadcast
- **Function:** Sends a message to all connected clients.

## `classes.py`

### Overview
The `classes.py` file defines the game classes, including characters and game management.

### Key Classes

#### Character
- **Attributes:** Player ID, name, and position.
- **Methods:** `set_position()`, `move()` (abstract).

#### Pawn
- **Method:** `move()` - Moves one step in the specified direction.

#### Hero1
- **Method:** `move()` - Moves two steps in the specified direction.

#### Hero2
- **Method:** `move()` - Moves two steps in a diagonal direction.

#### Game
- **Attributes:** Board state, players, and current turn.
- **Methods:**
  - `add_player()`: Adds a player with specified characters.
  - `place_characters()`: Places characters on the board.
  - `is_valid_move()`: Checks if a move is valid.
  - `move_character()`: Moves a character and updates the board.
  - `get_game_state()`: Retrieves the current state of the board.
