import React , { useEffect, useState } from 'react'
import { COUNTS } from '../app/data';
import TitleHead from '../components/TitleHead';
import Button from '../components/Button';
import endPoints from '../app/api';
import Technicals from '../components/Technicals';
import PriceChart from '../components/PriceChart'; // Add missing import
import Select from '../components/Select';

function Dashboard() {

  const [ selectedPair, setSelectedPair ] = useState(null)
  const [ selectedGran, setSelectedGran ] = useState(null);
  const [ technicalsData, setTechnicalsData ] = useState(null);
  const [ PriceData, setPriceData ] = useState(null);
  const [ selectedCount, setSelectedCount ] = useState(COUNTS[0].value); // Declare selectedCount variable
  const [ options, setOptions ] = useState(null); // Declare options variable
  const [ loading, setLoading] = useState(true); // Declare loading variable 


  useEffect(() => {
    loadOptions();
  }, []);



  const handleCountChange = (count) => {
    setSelectedCount(count);
    loadPrices(count);
  }

  const loadPrices = async (count) => {
    const data = await endPoints.prices(selectedPair, selectedGran, selectedCount);
    setPriceData(data);
  } 

  const loadOptions = async () => {
    const data = await endPoints.options();
    setOptions(data);
    setSelectedGran(data.granularities[0].value);
    setSelectedPair(data.pairs[0].value);
    setLoading(false);
  }

  const loadTechnicals = async () => { 
    const data = await endPoints.technicals(selectedPair, selectedGran);
    console.log({...data}); 
    setTechnicalsData(data);
    loadPrices(selectedCount);
  }

  if(loading === true) return <h1>Loading....</h1>

  return (
    <div>
      <TitleHead title="Options" />
      <div className="segment options">
       <Select 
        name="Currency"
        title="Select currency"
        options={options.pairs}
        defaultValue={selectedPair}
        onSelected={setSelectedPair}
        />
        <Select 
        name="Granularity"
        title="Select Granularity"
        options={options.granularities}
        defaultValue={selectedGran}
        onSelected={setSelectedGran}
        />
        <Button text="Load" handleClick={() => loadTechnicals()} />
      </div>
      <TitleHead title="Technicals" />
      { technicalsData && <Technicals data={technicalsData} /> }
      <TitleHead title="Price Chart" /> 
      { PriceData && <PriceChart 
      selectedCount={selectedCount}
      selectedPair={selectedPair}
      selectedGranularity={selectedGran}
      handleCountChange={handleCountChange}
      priceData={PriceData}
      />} 
    </div>
  )
}

export default Dashboard