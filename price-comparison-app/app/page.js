"use client";
import { useState } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(to bottom right, #00bfff, #ff69b4);
  color: #fff;
`;

const SearchInput = styled.input`
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  margin-right: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
`;

const SearchButton = styled.button`
  padding: 10px 20px;
  font-size: 16px;
  background-color: #fff;
  color: #333;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;

  &:hover {
    background-color: #333;
    color: #fff;
  }
`;

const Table = styled.table`
  margin-top: 30px;
  border-collapse: collapse;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
`;

const Th = styled.th`
  padding: 10px;
  background-color: #333;
  color: #fff;
  text-align: left;
`;

const Td = styled.td`
  padding: 10px;
  background-color: #fff;
  color: #333;
  text-align: left;
`;

const ProductLink = styled.a`
  color: #0077b6;
  text-decoration: none;
  transition: all 0.3s ease;

  &:hover {
    color: #023e8a;
    text-decoration: underline;
  }
`;

export default function Home() {
  const [productName, setProductName] = useState('');
  const [results, setResults] = useState(null);

  const handleSearch = async () => {
    try {
      const response = await fetch(`http://localhost:8000/search?product_name=${productName}`);
      const data = await response.json();
      console.log('Data:', data);
      setResults(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleInputChange = (event) => {
    setProductName(event.target.value);
  };

  return (
    <Container>
      <SearchInput
        type="text"
        value={productName}
        onChange={handleInputChange}
        placeholder="Enter product name"
      />
      <SearchButton onClick={handleSearch}>Search</SearchButton>
      {results && (
        <Table>
          <thead>
            <tr>
              <Th>Website</Th>
              <Th>Item Title</Th>
              <Th>Price</Th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <Td>Best Buy</Td>
              <Td>
                {results.bestbuy_price !== 'Product not found' ? (
                  <ProductLink
                    href={results.bestbuy_chosen_product_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {productName}
                  </ProductLink>
                ) : (
                  'Not found'
                )}
              </Td>
              <Td>{results.bestbuy_price}</Td>
            </tr>
            <tr>
              <Td>Walmart</Td>
              <Td>
                {results.walmart_price !== 'Product not found' ? (
                  <ProductLink
                    href={results.walmart_chosen_product_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {productName}
                  </ProductLink>
                ) : (
                  'Not found'
                )}
              </Td>
              <Td>{results.walmart_price}</Td>
            </tr>
            <tr>
              <Td>Newegg</Td>
              <Td>
                {results.newegg_price !== 'Product not found' ? (
                  <ProductLink
                    href={results.newegg_chosen_product_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {productName}
                  </ProductLink>
                ) : (
                  'Not found'
                )}
              </Td>
              <Td>{results.newegg_price}</Td>
            </tr>
          </tbody>
        </Table>
      )}
    </Container>
  );
}