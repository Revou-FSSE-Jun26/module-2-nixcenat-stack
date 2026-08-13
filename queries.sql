-- Query kombinasi WHERE, ORDER BY, dan LIMIT
-- Mencari 2 produk termahal yang harganya di bawah $100
SELECT 
    product_id, 
    product_name, 
    price, 
    stock_quantity
FROM 
    products
WHERE 
    price < 100.00
ORDER BY 
    price DESC
LIMIT 2;