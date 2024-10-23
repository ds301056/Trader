import React, { useState, useEffect } from 'react'; // Import React to use JSX and create components

import TitleHead from './TitleHead'; // Import a custom component named TitleHead
import endPoints from '../app/api';

const DATA_KEYS = [
  { name: "Account Num.", key: "id", fixed: -1 },
  { name: "Balance", key: "balance", fixed: -1 },
  { name: "NAV", key: "NAV", fixed: -1 },
  { name: "Open Trades", key: "openTradeCount", fixed: -1 },
  { name: "Unrealized PL", key: "unrealizedPL", fixed: -1 },
  { name: "Closeout %", key: "marginCloseoutPercent", fixed: -1 },
  { name: "Last Trans. ID", key: "lastTransactionID", fixed: -1 }

]


// Define the AccountSummary component
function AccountSummary() {
  // Use the useState hook to create a state variable 'count' and a function 'setCount' to update it.
  // The initial value of 'count' is set to 0.
 

  const [account, setAccount] = useState(null);

  useEffect(() => { 
    loadAccount();
  }, []) // if passing in dependencies, will not rerender unless dependancies have changed

  // Define a function to handle the increment of 'count'
  const loadAccount = async () => {
    const data = await endPoints.account();
    setAccount(data);
  }

  // The component's render output
  return (
    <div>
      {/* Render the TitleHead component and pass a prop 'title' with the value 'Account Summary' */}
      <TitleHead title='Account Summary' />
      {
        account && <div className='segment'>
            {
              DATA_KEYS.map(item  => {
                return <div key={item.key} className="account-row">
                  <div className = 'bold header' >{item.name}</div>
                  <div>{account[item.key]}</div>
                </div>
  
              })
            
            }
          </div>
      }
     
    </div>
  )
}

// Export the AccountSummary component to be used in other parts of the application
export default AccountSummary;
