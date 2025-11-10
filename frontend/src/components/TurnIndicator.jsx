import './TurnIndicator.css'

function TurnIndicator({ currentPlayer, gameOver }) {
  if (gameOver) return null

  return (
    <div className="turn-indicator">
      <div className={`indicator-light ${currentPlayer === 'X' ? 'active' : ''} player-x-light`}>
        <span className="led-icon">●</span>
        <span>Player X</span>
      </div>
      <div className={`indicator-light ${currentPlayer === 'O' ? 'active' : ''} player-o-light`}>
        <span className="led-icon">●</span>
        <span>Player O</span>
      </div>
    </div>
  )
}

export default TurnIndicator
