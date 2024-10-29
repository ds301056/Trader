import axios from 'axios'

// Log the API URL to ensure it's being read correctly
console.log('API URL:', import.meta.env.VITE_API_URL)

// Set the axios baseURL using Vite's environment variable syntax
axios.defaults.baseURL = import.meta.env.VITE_API_URL

// axios uses promises, so we can use async/await
const response = (resp) => resp.data

const requests = {
  get: (url) => {
    return axios.get(url).then(response)
  },
}

const endPoints = {
  account: () => requests.get('/account'),
  headlines: () => requests.get('/headlines'),
  options: () => requests.get('/options'),
  technicals: (p, g) => requests.get(`/technicals/${p}/${g}`),
  prices: (p, g, c) => requests.get(`/prices/${p}/${g}/${c}`),
}

export default endPoints
