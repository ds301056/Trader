import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import PropTypes from 'prop-types'
import {
  ComposedChart,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
  CartesianGrid,
  Line,
} from 'recharts'
import { COUNTS } from '../app/data'
import endPoints from '../app/api'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { toast } from '@/components/ui/use-toast'
import { extent } from 'd3-array'
import { scaleLinear } from 'd3-scale'
import Headlines from '@/components/Headlines'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload || !payload.length) {
    return null
  }

  const data = payload[0].payload
  return (
    <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
      <p className="text-sm font-medium mb-2">{label}</p>
      <div className="space-y-1">
        <p className="text-sm">
          <span className="text-gray-500">Open:</span>{' '}
          <span className="font-medium">{Number(data.open).toFixed(4)}</span>
        </p>
        <p className="text-sm">
          <span className="text-gray-500">High:</span>{' '}
          <span className="font-medium">{Number(data.high).toFixed(4)}</span>
        </p>
        <p className="text-sm">
          <span className="text-gray-500">Low:</span>{' '}
          <span className="font-medium">{Number(data.low).toFixed(4)}</span>
        </p>
        <p className="text-sm">
          <span className="text-gray-500">Close:</span>{' '}
          <span className="font-medium">{Number(data.close).toFixed(4)}</span>
        </p>
      </div>
    </div>
  )
}

CustomTooltip.propTypes = {
  active: PropTypes.bool,
  payload: PropTypes.arrayOf(
    PropTypes.shape({
      payload: PropTypes.shape({
        open: PropTypes.number,
        high: PropTypes.number,
        low: PropTypes.number,
        close: PropTypes.number,
      }),
    }),
  ),
  label: PropTypes.string,
}

const CandlestickSeries = ({ data, yScale }) => {
  const candleSpacing = 18 // Increase spacing between candles
  const initialOffset = 60 // Add an offset to move candles away from Y-axis

  return data.map((entry, index) => {
    const candleWidth = 10
    const x = initialOffset + index * candleSpacing // Apply spacing and initial offset

    const openPrice = parseFloat(entry.open)
    const closePrice = parseFloat(entry.close)
    const highPrice = parseFloat(entry.high)
    const lowPrice = parseFloat(entry.low)

    const color = closePrice > openPrice ? '#22c55e' : '#ef4444'

    return (
      <g key={`candle-${index}`}>
        {/* Wick line */}
        <line
          x1={x + candleWidth / 2}
          x2={x + candleWidth / 2}
          y1={yScale(highPrice)}
          y2={yScale(lowPrice)}
          stroke={color}
          strokeWidth={1}
        />
        {/* Candle body */}
        <rect
          x={x}
          y={yScale(Math.max(openPrice, closePrice))}
          width={candleWidth}
          height={Math.abs(yScale(openPrice) - yScale(closePrice))}
          fill={color}
        />
      </g>
    )
  })
}

CandlestickSeries.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      open: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
      high: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
      low: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
      close: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    }),
  ),
  x: PropTypes.func.isRequired,
  y: PropTypes.func.isRequired,
  width: PropTypes.number.isRequired,
}

// ------------------------------
const Dashboard = () => {
  // State management
  const [selectedPair, setSelectedPair] = useState(null)
  const [selectedGran, setSelectedGran] = useState(null)
  const [technicalsData, setTechnicalsData] = useState(null)
  const [priceData, setPriceData] = useState(null)
  const [selectedCount, setSelectedCount] = useState(COUNTS[0].value)
  const [options, setOptions] = useState({ pairs: [], granularities: [] })
  const [loading, setLoading] = useState(true)

  // Modified loadPrices function with error handling
  const loadPrices = async (
    count,
    pair = selectedPair,
    gran = selectedGran,
  ) => {
    if (!pair || !gran) return // Guard clause to prevent loading without required params

    try {
      setLoading(true)
      const response = await endPoints.prices(pair, gran, count)

      if (response && response.time && response.mid_c) {
        const formattedData = response.time
          .map((time, index) => ({
            time: new Date(time).toLocaleString(),
            close: parseFloat(response.mid_c[index]),
            high: parseFloat(response.mid_h[index]),
            low: parseFloat(response.mid_l[index]),
            open: parseFloat(response.mid_o[index]),
          }))
          .reverse()

        setPriceData(formattedData)
      }
    } catch (error) {
      console.error('Error loading prices:', error)
      toast({
        variant: 'destructive',
        title: 'Error loading prices',
        description: error.message,
      })
    } finally {
      setLoading(false)
    }
  }
  // Modified loadTechnicals function with error handling
  const loadTechnicals = async (pair = selectedPair, gran = selectedGran) => {
    if (!pair || !gran) return // Guard clause to prevent loading without required params

    try {
      setLoading(true)
      const data = await endPoints.technicals(pair, gran)
      setTechnicalsData(data)
      await loadPrices(selectedCount, pair, gran)
    } catch (error) {
      console.error('Error loading technicals:', error)
      toast({
        variant: 'destructive',
        title: 'Error loading technicals',
        description: error.message,
      })
    } finally {
      setLoading(false)
    }
  }
  // Modified loadOptions function
  const loadOptions = async () => {
    try {
      const data = await endPoints.options()

      const formattedData = {
        pairs: data.pairs.map((pair) => ({
          label: pair.text,
          value: pair.value,
        })),
        granularities: data.granularities.map((gran) => ({
          label: gran.text,
          value: gran.value,
        })),
      }

      setOptions(formattedData)

      // Find and set USD_CAD and M5 as defaults
      const usdCadPair = formattedData.pairs.find(
        (pair) => pair.value === 'USD_CAD',
      )
      const m5Gran = formattedData.granularities.find(
        (gran) => gran.value === 'M5',
      )

      const defaultPair = usdCadPair?.value || formattedData.pairs[0]?.value
      const defaultGran = m5Gran?.value || formattedData.granularities[0]?.value

      // Set the state values
      setSelectedGran(defaultGran)
      setSelectedPair(defaultPair)

      return { selectedPair: defaultPair, selectedGran: defaultGran }
    } catch (error) {
      console.error('Error loading options:', error)
      toast({
        variant: 'destructive',
        title: 'Error loading options',
        description: error.message,
      })
      return null
    }
  }
  // Modified initialization useEffect
  useEffect(() => {
    const initializeData = async () => {
      try {
        const defaults = await loadOptions()
        if (defaults) {
          // Wait for state updates to propagate
          setTimeout(() => {
            loadTechnicals(defaults.selectedPair, defaults.selectedGran)
          }, 0)
        }
      } finally {
        setLoading(false)
      }
    }

    initializeData()
  }, [])

  // Handle load button click separately from initialization
  const handleLoadClick = () => {
    loadTechnicals(selectedPair, selectedGran)
  }
  // Modified count change handler
  const handleCountChange = (count) => {
    setSelectedCount(count)
    loadPrices(count, selectedPair, selectedGran)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <h1 className="text-2xl font-semibold">Loading...</h1>
      </div>
    )
  }
  // ------------------------------

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div className="flex items-center space-x-4">
            <div className="h-10 w-10 rounded-full bg-purple-100 flex items-center justify-center">
              <span className="text-purple-600 text-xl">👤</span>
            </div>
            <div>
              <h1 className="text-2xl font-semibold">Trading Dashboard</h1>
              <p className="text-gray-500">Market Analysis Tool</p>
            </div>
          </div>
        </div>

        {/* Trading Options */}
        <Card>
          <CardHeader className="pb-4">
            <CardTitle className="text-xl font-semibold">
              Trading Options
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
              <div className="md:col-span-5 space-y-2">
                <Label className="text-sm font-medium text-gray-700">
                  Currency Pair
                </Label>
                <Select value={selectedPair} onValueChange={setSelectedPair}>
                  <SelectTrigger className="h-10 bg-white border-gray-200">
                    <SelectValue placeholder="Select Currency Pair" />
                  </SelectTrigger>
                  <SelectContent
                    style={{ maxHeight: '200px', overflowY: 'auto' }}
                  >
                    {options.pairs.map((pair) => (
                      <SelectItem
                        key={pair.value}
                        value={pair.value}
                        className="hover:bg-gray-50"
                      >
                        {pair.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="md:col-span-5 space-y-2">
                <Label className="text-sm font-medium text-gray-700">
                  Granularity
                </Label>
                <Select value={selectedGran} onValueChange={setSelectedGran}>
                  <SelectTrigger className="h-10 bg-white border-gray-200">
                    <SelectValue placeholder="Select Granularity" />
                  </SelectTrigger>
                  <SelectContent>
                    {options.granularities.map((gran) => (
                      <SelectItem
                        key={gran.value}
                        value={gran.value}
                        className="hover:bg-gray-50"
                      >
                        {gran.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="md:col-span-2 flex items-end">
                <Button
                  onClick={handleLoadClick}
                  className="w-full h-10 bg-slate-900 text-white hover:bg-slate-800"
                >
                  Load Data
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column - Technical Information */}
          <div className="lg:col-span-5 space-y-6">
            {/* Selected Pair Info */}
            <Card className="bg-slate-900 text-white">
              <CardContent className="pt-6">
                <div className="space-y-4">
                  <div>
                    <p className="text-sm text-gray-300">Selected Pair</p>
                    <h2 className="text-3xl font-bold tracking-tight">
                      {selectedPair}
                    </h2>
                  </div>
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="text-sm text-gray-300">Granularity</p>
                      <p className="font-medium">{selectedGran}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-300">Data Points</p>
                      <p className="font-medium">{selectedCount}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Technical Indicators */}
            {technicalsData && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-xl font-semibold flex items-center justify-between">
                    Technical Indicators
                    <span className="text-sm text-gray-500">
                      Updated:{' '}
                      {new Date(technicalsData.updated).toLocaleString()}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {/* Market Sentiment */}
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-green-50 p-4 rounded-lg border border-green-100">
                        <h3 className="text-sm text-gray-600 mb-1">
                          Bullish Signals
                        </h3>
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="text-2xl font-bold text-green-600">
                              {technicalsData.percent_bullish}
                            </p>
                            <p className="text-sm text-gray-500">
                              MA Buy: {technicalsData.ma_buy}
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="text-xl font-semibold text-green-600">
                              {technicalsData.ti_buy}
                            </p>
                            <p className="text-sm text-gray-500">Buy Signals</p>
                          </div>
                        </div>
                      </div>
                      <div className="bg-red-50 p-4 rounded-lg border border-red-100">
                        <h3 className="text-sm text-gray-600 mb-1">
                          Bearish Signals
                        </h3>
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="text-2xl font-bold text-red-600">
                              {technicalsData.percent_bearish}
                            </p>
                            <p className="text-sm text-gray-500">
                              MA Sell: {technicalsData.ma_sell}
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="text-xl font-semibold text-red-600">
                              {technicalsData.ti_sell}
                            </p>
                            <p className="text-sm text-gray-500">
                              Sell Signals
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Pivot Point */}
                    <div className="bg-slate-900 text-white p-4 rounded-lg">
                      <div className="flex justify-between items-center">
                        <div>
                          <h3 className="text-sm font-medium text-gray-300 mb-1">
                            Pivot Point
                          </h3>
                          <p className="text-2xl font-bold">
                            {technicalsData.pivot}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-gray-300">
                            Signal Strength
                          </p>
                          <p className="text-lg font-medium text-green-400">
                            {parseInt(technicalsData.ti_buy)} Buy /{' '}
                            {parseInt(technicalsData.ti_sell)} Sell
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Support & Resistance Levels */}
                    <div className="grid grid-cols-3 gap-4">
                      {['R3', 'R2', 'R1', 'S1', 'S2', 'S3'].map((level) => (
                        <div key={level} className="space-y-2">
                          <h3 className="text-sm font-medium text-gray-600">
                            {level.startsWith('R') ? 'Resistance' : 'Support'}{' '}
                            {level.charAt(1)}
                          </h3>
                          <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <p className="text-lg font-semibold">
                              {technicalsData[level]}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Time Frame Info */}
                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
                      <div className="flex justify-between items-center">
                        <div>
                          <h3 className="text-sm text-gray-600">Time Frame</h3>
                          <p className="text-lg font-semibold">
                            {technicalsData.time_frame / 60} Minutes
                          </p>
                        </div>
                        <div className="text-right">
                          <h3 className="text-sm text-gray-600">Pair</h3>
                          <p className="text-lg font-semibold">
                            {technicalsData.pair_name}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column - Price Chart */}
          <div className="lg:col-span-7">
            {priceData && priceData.length > 0 && (
              <Card className="h-full">
                <CardHeader className="pb-4">
                  <div className="flex justify-between items-center">
                    <CardTitle className="text-xl font-semibold">
                      Price Chart - {selectedPair}
                    </CardTitle>
                    <Tabs
                      defaultValue={selectedCount.toString()}
                      onValueChange={(value) =>
                        handleCountChange(parseInt(value))
                      }
                    >
                      <div className="flex flex-col items-start space-y-2">
                        {/* Label */}
                        <p className="text-sm font-medium text-gray-700">
                          Data Points
                        </p>

                        {/* Tabs for selecting data points */}
                        <TabsList className="bg-slate-100 p-1 rounded-md border border-gray-300">
                          {COUNTS.map((count) => (
                            <TabsTrigger
                              key={count.value}
                              value={count.value.toString()}
                              className="px-4 py-2 bg-white text-gray-700 rounded-md hover:bg-gray-200 data-[state=active]:bg-slate-900 data-[state=active]:text-white"
                            >
                              {count.label || count.value}{' '}
                              {/* Use label or fallback to the count value */}
                            </TabsTrigger>
                          ))}
                        </TabsList>
                      </div>
                    </Tabs>
                  </div>
                </CardHeader>
                <CardContent>
                  {/* Replace the existing chart section with this */}
                  <div className="h-[800px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <ComposedChart
                        data={priceData}
                        margin={{ top: 20, right: 30, left: 0, bottom: 50 }}
                      >
                        <defs>
                          <linearGradient
                            id="colorValue"
                            x1="0"
                            y1="0"
                            x2="0"
                            y2="1"
                          >
                            <stop
                              offset="5%"
                              stopColor="#8884d8"
                              stopOpacity={0.5}
                            />
                            <stop
                              offset="95%"
                              stopColor="#8884d8"
                              stopOpacity={0}
                            />
                          </linearGradient>

                          {/* Clip Path Definition */}
                          <clipPath id="clip-candle">
                            <rect
                              x="0"
                              y="0"
                              width="100%"
                              height="100%"
                              transform="translate(20,20)" // Adjust based on margin
                            />
                          </clipPath>
                        </defs>
                        <XAxis
                          dataKey="time"
                          tick={{ fontSize: 12 }}
                          height={60}
                          angle={-45}
                          textAnchor="end"
                        />
                        <YAxis
                          type="number"
                          domain={['dataMin', 'dataMax']}
                          tickFormatter={(value) => value.toFixed(4)}
                        />
                        <CartesianGrid strokeDasharray="3 3" />
                        <Tooltip content={<CustomTooltip />} />
                        {/* Use regular Line component for continuous price line */}
                        <Line
                          type="monotone"
                          dataKey="close"
                          stroke="#8884d8"
                          dot={false}
                          isAnimationActive={false}
                        />
                        {/* Add custom candles with clipPath and x-offset */}

                        {priceData && (
                          <svg clipPath="url(#clip-candle)">
                            <CandlestickSeries
                              data={priceData}
                              yScale={(value) => {
                                const [min, max] = extent(
                                  priceData,
                                  (d) => d.close,
                                )
                                const scale = scaleLinear()
                                  .domain([min, max])
                                  .range([550, 50]) // Adjust as needed
                                return scale(value)
                              }}
                              x={(index) => 60 + index * 18} // Example spacing logic for x
                              y={(price) => {
                                const [min, max] = extent(
                                  priceData,
                                  (d) => d.close,
                                )
                                const scale = scaleLinear()
                                  .domain([min, max])
                                  .range([550, 50]) // Same scale as yScale
                                return scale(price)
                              }}
                              width={10} // Fixed candle width
                            />
                          </svg>
                        )}
                      </ComposedChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
        <Headlines className="items-center overflow-scroll" />
      </div>
    </div>
  )
}

export default Dashboard
