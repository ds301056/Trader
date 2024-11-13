import React from 'react' // Import React to use JSX and create components
import NavbarLink from './NavbarLink'

// Define the NavigationBar component
function NavigationBar() {
  return (
    // This is the main container for the navigation bar
    <div id="navbar">
      {/* This is the title section of the navigation bar */}
      <div className="navtitle">Forex Dash</div>
      
      {/* This is the section for navigation links */}
      <div id="navlinks">
        <NavbarLink path="/" text="Home"/>
        <NavbarLink path="/dashboard" text="Dashboard"/>
      </div>
    </div>
  )
}

// Export the NavigationBar component to be used in other parts of the application
export default NavigationBar
