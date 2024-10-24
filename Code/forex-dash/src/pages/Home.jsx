import React, { useEffect, useState } from 'react'
import { COUNTS } from '../app/data'
import endPoints from '../app/api'

// Components
import AccountSummary from '../components/AccountSummary'
import Headlines from '../components/Headlines'
import TitleHead from '../components/TitleHead'
import Button from '../components/Button'
import Technicals from '../components/Technicals'
import PriceChart from '../components/PriceChart'
import Select from '../components/Select'

const Home = () => {
  const [selectedPair, setSelectedPair] = useState(null)
  const [selectedGran, setSelectedGran] = useState(null)
  const [technicalsData, setTechnicalsData] = useState(null)
  const [priceData, setPriceData] = useState(null)
  const [selectedCount, setSelectedCount] = useState(COUNTS[0].value)
  const [options, setOptions] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadOptions()
  }, [])

  const handleCountChange = (count) => {
    setSelectedCount(count)
    loadPrices(count)
  }

  const loadPrices = async (count) => {
    const data = await endPoints.prices(
      selectedPair,
      selectedGran,
      selectedCount,
    )
    setPriceData(data)
  }

  const loadOptions = async () => {
    const data = await endPoints.options()
    setOptions(data)
    setSelectedGran(data.granularities[0].value)
    setSelectedPair(data.pairs[0].value)
    setLoading(false)
  }

  const loadTechnicals = async () => {
    const data = await endPoints.technicals(selectedPair, selectedGran)
    setTechnicalsData(data)
    loadPrices(selectedCount)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl font-semibold">Loading...</div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-6 space-y-6">
      <AccountSummary />

      <div className="space-y-6">
        <TitleHead title="Options" />
        <div className="segment options bg-white rounded-lg shadow p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
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
            <Button text="Load" handleClick={loadTechnicals} />
          </div>
        </div>

        {technicalsData && (
          <>
            <TitleHead title="Technicals" />
            <div className="bg-white rounded-lg shadow p-4">
              <Technicals data={technicalsData} />
            </div>
          </>
        )}

        {priceData && (
          <>
            <TitleHead title="Price Chart" />
            <div className="bg-white rounded-lg shadow p-4">
              <PriceChart
                selectedCount={selectedCount}
                selectedPair={selectedPair}
                selectedGranularity={selectedGran}
                handleCountChange={handleCountChange}
                priceData={priceData}
              />
            </div>
          </>
        )}
      </div>

      <div className="mt-8">
        <div className="bg-white rounded-lg shadow">
          <Headlines />
        </div>
      </div>
    </div>
  )
}

export default Home
