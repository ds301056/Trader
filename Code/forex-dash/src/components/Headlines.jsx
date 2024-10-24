import React, { useEffect, useState } from 'react'
import Headline from './Headline'
import endPoints from '../app/api'
import TitleHead from './TitleHead'

function Headlines() {
  const [headlines, setHeadlines] = useState(null)

  useEffect(() => {
    loadHeadlines()
  }, []) // if passing in dependencies, will not rerender unless dependancies have changed

  // Define a function to handle the increment of 'count'
  const loadHeadlines = async () => {
    const data = await endPoints.headlines()
    setHeadlines(data)
  }

  return (
    <div>
      <TitleHead title="Headlines" />
      <div className="segment">
        {headlines &&
          headlines.map((item, index) => {
            return <Headline data={item} key={index} />
          })}
      </div>
    </div>
  )
}

export default Headlines
