import React from 'react'

function Button({text, handleClick}) {
  return (
    <div>
      <button onClick={() => handleClick()}>{text}</button>
    </div>
  )
}

export default Button