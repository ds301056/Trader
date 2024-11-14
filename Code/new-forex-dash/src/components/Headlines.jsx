import { useState, useEffect } from 'react'
import Headline from './Headline'
import endPoints from '../app/api'

function Headlines() {
  const [headlines, setHeadlines] = useState(null)

  useEffect(() => {
    loadHeadlines()
  }, [])

  const loadHeadlines = async () => {
    const data = await endPoints.headlines()
    setHeadlines(data)
  }

  return (
    <div className="bg-white rounded-lg shadow pt-8">
      {/* Title Section */}
      <div className="flex justify-center mb-4">
        <h2 className="text-2xl font-semibold text-gray-800">
          Recent Headlines that may affect trade value
        </h2>
      </div>
      <div className="divide-y max-h-[500px] overflow-y-auto p-4 space-y-2">
        {headlines &&
          headlines.map((item, index) => (
            <div key={index} className="py-3 first:pt-0 last:pb-0">
              <Headline data={item} key={index} />
            </div>
          ))}
      </div>
    </div>
  )
}

export default Headlines
