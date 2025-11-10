import './Square.css'

function Square({ value, isWinning, gameOver }) {
  return (
    <div className={`square ${isWinning ? 'winning' : ''} ${value ? 'filled' : ''}`}>
      {value && (
        <span className={`symbol ${value === 'X' ? 'player-x' : 'player-o'}`}>
          {value}
        </span>
      )}
    </div>
  )
}

export default Square
