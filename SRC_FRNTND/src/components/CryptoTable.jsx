import React from "react";

const CryptoTable = () => {
  const sampleData = [
    {
      id: 1,
      name: "Bitcoin",
      image: "https://cryptologos.cc/logos/bitcoin-btc-logo.png",
      price: "$82,184",
      marketCap: "$1,629,265,791,015",
    },
    {
      id: 2,
      name: "Ethereum",
      image: "https://cryptologos.cc/logos/ethereum-eth-logo.png",
      price: "$1,787.75",
      marketCap: "$215,609,961,547",
    },
  ];

  return (
    <div className="p-4">
      <table className="min-w-full border-collapse border border-gray-400">
        <thead>
          <tr className="bg-gray-200 dark:bg-gray-700">
            <th className="border border-gray-400 px-4 py-2">#</th>
            <th className="border border-gray-400 px-4 py-2">Name</th>
            <th className="border border-gray-400 px-4 py-2">Price</th>
            <th className="border border-gray-400 px-4 py-2">Market Cap</th>
          </tr>
        </thead>
        <tbody>
          {sampleData.map((crypto) => (
            <tr key={crypto.id} className="text-center">
              <td className="border border-gray-400 px-4 py-2">{crypto.id}</td>
              <td className="border border-gray-400 px-4 py-2 flex items-center justify-center gap-2">
                <img src={crypto.image} alt={crypto.name} className="h-10 w-10" />
                {crypto.name}
              </td>
              <td className="border border-gray-400 px-4 py-2">{crypto.price}</td>
              <td className="border border-gray-400 px-4 py-2">{crypto.marketCap}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CryptoTable;
