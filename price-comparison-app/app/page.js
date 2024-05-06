
"use client";
import { useState } from 'react';

export default function Home() {
  const [productName, setProductName] = useState('');
  const [results, setResults] = useState(null);

  const handleSearch = async () => {
    try {
      const response = await fetch(`http://localhost:8000/search?product_name=${productName}`);
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleInputChange = (event) => {
    setProductName(event.target.value);
  };

  return (
    <div>
      <input type="text" value={productName} onChange={handleInputChange} placeholder="Enter product name" />
      <button onClick={handleSearch}>Search</button>

      {results && (
        <table>
          <thead>
            <tr>
              <th>Website</th>
              <th>Item Title</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Best Buy</td>
              <td>
                {results.bestbuy_price !== 'Product not found' ? (
                  <a href={`https://www.bestbuy.com/site/searchpage.jsp?st=${productName.replace(' ', '+')}&intl=nosplash`} target="_blank" rel="noopener noreferrer">
                    {productName}
                  </a>
                ) : (
                  'Not found'
                )}
              </td>
              <td>{results.bestbuy_price}</td>
            </tr>
            <tr>
              <td>Walmart</td>
              <td>
                {results.walmart_price !== 'Product not found' ? (
                  <a href={`https://www.walmart.com/search?q=${productName.replace(' ', '+')}&intl=nosplash`} target="_blank" rel="noopener noreferrer">
                    {productName}
                  </a>
                ) : (
                  'Not found'
                )}
              </td>
              <td>{results.walmart_price}</td>
            </tr>
            <tr>
              <td>Newegg</td>
              <td>
                {results.newegg_price !== 'Product not found' ? (
                  <a href={`https://www.newegg.com/p/pl?d=${productName.replace(' ', '+')}`} target="_blank" rel="noopener noreferrer">
                    {productName}
                  </a>
                ) : (
                  'Not found'
                )}
              </td>
              <td>{results.newegg_price}</td>
            </tr>
          </tbody>
        </table>
      )}
    </div>
  );
} 