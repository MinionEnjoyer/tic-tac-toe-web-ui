import { useState, useEffect } from 'react'
import { io } from 'socket.io-client'
import GameBoard from './components/GameBoard'
import GameStatus from './components/GameStatus'
import TurnIndicator from './components/TurnIndicator'
import './App.css'

function App() {
  const [socket, setSocket] = useState(null)
  const [gameState, setGameState] = useState({
    board: Array(9).fill(null),
    current_player: 'X',
    game_over: false,
    winner: null,
    winning_line: null,
    is_draw: false
  })
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    // Connect to the Flask server
    const socketUrl = window.location.hostname === 'localhost' 
      ? 'http://localhost:5000' 
      : `http://${window.location.hostname}:5000`
    
    const newSocket = io(socketUrl, {
      transports: ['websocket', 'polling']
    })

    newSocket.on('connect', () => {
      console.log('Connected to server')
      setConnected(true)
    })

    newSocket.on('disconnect', () => {
      console.log('Disconnected from server')
      setConnected(false)
    })

    newSocket.on('game_state', (state) => {
      console.log('Received game state:', state)
      setGameState(state)
    })

    newSocket.on('move_made', (result) => {
      console.log('Move made:', result)
      setGameState({
        board: result.board,
        current_player: result.next_player || result.player,
        game_over: result.game_over,
        winner: result.winner,
        winning_line: result.winning_line,
        is_draw: result.is_draw
      })
    })

    newSocket.on('game_reset', (state) => {
      console.log('Game reset:', state)
      setGameState(state)
    })

    newSocket.on('invalid_move', (data) => {
      console.log('Invalid move attempted at position:', data.position)
    })

    setSocket(newSocket)

    return () => {
      newSocket.close()
    }
  }, [])

  const handleReset = () => {
    if (socket) {
      socket.emit('reset_game')
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Tic-Tac-Toe</h1>
        <div className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
          {connected ? '● Connected' : '○ Disconnected'}
        </div>
      </header>
      
      <main className="App-main">
        <TurnIndicator 
          currentPlayer={gameState.current_player}
          gameOver={gameState.game_over}
        />
        
        <GameStatus
          gameOver={gameState.game_over}
          winner={gameState.winner}
          isDraw={gameState.is_draw}
        />
        
        <GameBoard
          board={gameState.board}
          winningLine={gameState.winning_line}
          gameOver={gameState.game_over}
        />
        
        <button 
          className="reset-button"
          onClick={handleReset}
        >
          Reset Game
        </button>
        
        <div className="instructions">
          <p>Press the physical buttons on the Raspberry Pi to make your move!</p>
          <p>Player X (Red LED) • Player O (Blue LED)</p>
        </div>
      </main>
    </div>
  )
}

export default App
