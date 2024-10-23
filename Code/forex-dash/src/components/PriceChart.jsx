import React, { useEffect } from 'react';
import Select from './Select';
import { COUNTS } from '../app/data';
import { drawChart } from '../app/chart';




function PriceChart({ priceData, selectedPair, selectedGranularity,
                      selectedCount,handleCountChange}) { 
  

      // useEffect hook to run side effects when priceData changes
    useEffect(() => {
      if(priceData) {
        drawChart(priceData, selectedPair, selectedGranularity, 'chartDiv');
      }
    }, [priceData, selectedGranularity, selectedPair]); // Dependency array containing priceData, selectedPair, and selectedGranularity

    
  return (  
    <div className='segment' id='price-chart-holder'>
      <Select 
        name="numrows"
        title="Num. Rows."
        options={COUNTS}
        defaultValue={selectedCount}
        onSelected={handleCountChange}
      />
      <div id="chartDiv"></div>
    </div>
  )
}
export default PriceChart
