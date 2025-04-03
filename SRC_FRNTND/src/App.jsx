import React from "react";
import Header from "./components/Header";
import DarkModeToggle from "./components/DarkModeToggle";
import CryptoTable from "./components/CryptoTable";

function App() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
      <Header />
      <DarkModeToggle />
      <CryptoTable />
    </div>
  );
}

export default App;
