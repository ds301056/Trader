import React from 'react'

function Test({ surname, eyes, makeClick}) {



  return(
    <>


      <div>Tested</div>
      <div>{surname}</div>
      <div>{eyes}</div>
      <button onClick={() => makeClick(14)}> Click</button>
    </>
  )
}

export default Test;
