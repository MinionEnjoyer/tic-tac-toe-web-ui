import Square from './Square'
import './GameBoard.css'

function GameBoard({ board, winningLine, gameOver }) {
  return (
    <div className="game-board">
      {board.map((value, index) => (
        <Square
          key={index}
          value={value}
          isWinning={winningLine && winningLine.includes(index)}
          gameOver={gameOver}
        />
      ))}
    </div>
  )
}

export default GameBoard
