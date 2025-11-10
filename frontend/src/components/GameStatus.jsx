import './GameStatus.css'

function GameStatus({ gameOver, winner, isDraw }) {
  if (!gameOver) return null

  return (
    <div className={`game-status ${winner ? 'winner' : 'draw'}`}>
      {winner ? (
        <>
          <h2 className={`winner-text ${winner === 'X' ? 'player-x' : 'player-o'}`}>
            Player {winner} Wins!
          </h2>
          <p>🎉 Congratulations! 🎉</p>
        </>
      ) : isDraw ? (
        <>
          <h2>It's a Draw!</h2>
          <p>Well played! Try again.</p>
        </>
      ) : null}
    </div>
  )
}

export default GameStatus
