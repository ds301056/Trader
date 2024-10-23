import Footer from './components/Footer';
import NavigationBar from './components/NavigationBar';
import Dashboard from './pages/Dashboard'; // Import the Dashboard component
import Home from './pages/Home'; // Import the Home component

import {
  BrowserRouter,
  Route,
  Routes
} from 'react-router-dom';

function App() {

  return (
    <>
      <BrowserRouter> 
      <div id="app-holder">
        <NavigationBar />
        <div className="container">
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </div>
        <Footer />
      </div>
      </BrowserRouter>
    </>
  );
}

export default App;
