import React from 'react'
import Progress from './Progress';


const HEADERS = [
  "R1", "R2", "R3", 
  "S1", "S2", "S3", 
  "Pivot" ];



function Technicals({ data }) {
  return (
    <div className='segment'>
      <Progress
        title="Bullish"
        color="#21ba45"
        percentage={data.percent_bullish} />
      <Progress
      title="Bearish"
      color="#db2828"
      percentage={data.percent_bearish} />
      <table>
        <thead>
            <tr>{
              HEADERS.map(item => {
                return <th key={item}>{item}</th>
              })
            }
            </tr>
            <tr>{
              HEADERS.map(item => {
                return <td key={item}>{data[item]}</td>
              })
            }
            </tr>
        </thead>
      </table>
    </div>
  )
}

export default Technicals
