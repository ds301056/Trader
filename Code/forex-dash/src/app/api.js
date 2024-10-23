import axios from "axios";

console.log("API URL:", process.env.REACT_APP_API_URL); // Log the API URL to ensure it's being read correctly
axios.defaults.baseURL = process.env.REACT_APP_API_URL;
// axios uses promises so we can use async/await

const response = (resp) => resp.data;

const requests = {
  get: (url) => {
    return axios.get(url).then(response);
  }
}

const endPoints = {
  account: () => requests.get("/account"),
  headlines: () => requests.get("/headlines"),
  options: (p, g) => requests.get("/options"),
  technicals: (p, g) => requests.get(`/technicals/${p}/${g}`),
  prices: (p, g, c) => requests.get(`/prices/${p}/${g}/${c}`)
  
}

export default endPoints;
