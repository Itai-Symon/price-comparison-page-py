import React, { useState } from 'react';

const InputForm = ({ onSubmit }) => {
  const [productName, setProductName] = useState('');

  const handleChange = (e) => {
    setProductName(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(productName);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={productName} onChange={handleChange} />
      <button type="submit">Search</button>
    </form>
  );
};

export default InputForm;
