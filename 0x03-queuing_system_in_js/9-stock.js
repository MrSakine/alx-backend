import express from 'express';
import redis from 'redis';
import util from 'util';

const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

const client = redis.createClient();
const getAsync = util.promisify(client.get).bind(client);
const setAsync = util.promisify(client.set).bind(client);

const getItemById = (id) => {
  return listProducts.find(item => item.id === id);
};

const reserveStockById = (itemId, stock) => {
  const key = `item.${itemId}`;
  return setAsync(key, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  const key = `item.${itemId}`;
  const reservedStock = await getAsync(key);
  return reservedStock ? parseInt(reservedStock, 10) : 0;
};

const app = express();
const port = 1245;

app.get('/list_products', (_, res) => {
  const formattedProducts = listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock
  }));
  
  res.json(formattedProducts);
});

app.get('/list_products/:id', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  const product = getItemById(id);

  if (product) {
    const reservedStock = await getCurrentReservedStockById(id);
    res.json({
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
      reservedStock
    });
  } else {
    res.status(404).send('Product not found');
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const id = parseInt(req.params.itemId, 10);
  const product = getItemById(id);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getCurrentReservedStockById(id);
  if (reservedStock >= product.stock) {
    return res.json({ status: 'Not enough stock available', itemId: id });
  }

  await reserveStockById(id, reservedStock + 1);
  res.json({ status: 'Reservation confirmed', itemId: id });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
