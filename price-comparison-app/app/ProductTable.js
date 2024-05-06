import React from 'react';

const ProductTable = ({ products }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Link</th>
        </tr>
      </thead>
      <tbody>
        {products.map((product, index) => (
          <tr key={index}>
            <td>{product.name}</td>
            <td>
              <a href={product.link} target="_blank" rel="noreferrer">
                {product.name} Page
              </a>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ProductTable;
