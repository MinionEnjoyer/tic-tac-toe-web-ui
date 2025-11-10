"""
Game Controller for Tic-Tac-Toe
Implements game logic, win detection, and state management
"""


class GameController:
    """Manages the Tic-Tac-Toe game logic and state."""
    
    # Winning line combinations (panel indices)
    WINNING_LINES = [
        # Rows
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        # Columns
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        # Diagonals
        [0, 4, 8],
        [2, 4, 6],
    ]
    
    def __init__(self):
        """Initialize the game controller."""
        self.board = [None] * 9  # None = empty, 'X' or 'O' for filled
        self.current_player = 'X'  # X always starts
        self.game_over = False
        self.winner = None
        self.winning_line = None
        print("Game controller initialized")
    
    def reset_game(self):
        """Reset the game to initial state."""
        print("Resetting game")
        self.board = [None] * 9
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_line = None
    
    def is_valid_move(self, position):
        """
        Check if a move is valid.
        
        Args:
            position: Board position (0-8)
            
        Returns:
            True if the move is valid, False otherwise
        """
        if position < 0 or position > 8:
            return False
        
        if self.game_over:
            return False
        
        # Square must be empty
        return self.board[position] is None
    
    def make_move(self, position):
        """
        Make a move on the board.
        
        Args:
            position: Board position (0-8)
            
        Returns:
            Dict with move result info or None if invalid
        """
        if not self.is_valid_move(position):
            print(f"Invalid move: position {position}")
            return None
        
        # Place the symbol
        self.board[position] = self.current_player
        print(f"Player {self.current_player} placed at position {position}")
        
        result = {
            'position': position,
            'player': self.current_player,
            'board': self.board.copy(),
            'game_over': False,
            'winner': None,
            'winning_line': None,
            'is_draw': False,
            'next_player': None
        }
        
        # Check for win or draw
        if self._check_win():
            self.game_over = True
            self.winner = self.current_player
            result['game_over'] = True
            result['winner'] = self.winner
            result['winning_line'] = self.winning_line
            print(f"Player {self.current_player} wins!")
        elif self._check_draw():
            self.game_over = True
            result['game_over'] = True
            result['is_draw'] = True
            print("Game is a draw!")
        else:
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            result['next_player'] = self.current_player
            print(f"Turn: Player {self.current_player}")
        
        return result
    
    def _check_win(self):
        """
        Check if the current player has won.
        
        Returns:
            True if current player won, False otherwise
        """
        for line in self.WINNING_LINES:
            if all(self.board[i] == self.current_player for i in line):
                self.winning_line = line
                return True
        return False
    
    def _check_draw(self):
        """
        Check if the game is a draw (all squares filled, no winner).
        
        Returns:
            True if game is a draw, False otherwise
        """
        return all(square is not None for square in self.board)
    
    def get_game_state(self):
        """
        Get the complete current game state.
        
        Returns:
            Dict with all game state information
        """
        return {
            'board': self.board.copy(),
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'winning_line': self.winning_line,
            'is_draw': self.game_over and self.winner is None
        }
