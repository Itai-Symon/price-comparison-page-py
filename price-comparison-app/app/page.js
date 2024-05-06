
"use client";
import React, { useState } from 'react';
import InputForm from '../app/InputForm';
import ProductTable from '../app/ProductTable';

const Home = () => {
  const [products, setProducts] = useState([]);

  const fetchProducts = async (productName) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/search?product_name=${productName}`);
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  return (
    <div>
      <h1>Product Search</h1>
      <InputForm onSubmit={fetchProducts} />
      <ProductTable products={products} />
    </div>
  );
};

export default Home;
