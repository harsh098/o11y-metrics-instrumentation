import express from 'express';
import { promMiddleware } from 'express-red-middleware';

const app = express();
const PORT = 8000;

app.use(express.json());
app.use(promMiddleware());

app.get('/', (req, res) => {
    res.json({ message: "Welcome to the API" });
});

app.get('/items/:item_id', (req, res) => {
    const itemId = req.params.item_id;
    if (itemId == 0) {
        return res.status(404).json({ error: "Item not found" });
    }
    res.json({ item_id: itemId, name: `Item ${itemId}` });
});

app.post('/items', (req, res) => {
    const item = req.body;
    if (!item.price || item.price <= 0) {
        return res.status(400).json({ error: "Price must be positive" });
    }
    res.json({ message: "Item created", item });
});

app.put('/items/:item_id', (req, res) => {
    const itemId = req.params.item_id;
    const item = req.body;
    if (itemId == 0) {
        return res.status(404).json({ error: "Item not found" });
    }
    if (!item.price || item.price <= 0) {
        return res.status(400).json({ error: "Price must be positive" });
    }
    res.json({ message: "Item updated", item_id: itemId, item });
});

app.patch('/items/:item_id', (req, res) => {
    const itemId = req.params.item_id;
    const item = req.body;
    if (itemId == 0) {
        return res.status(404).json({ error: "Item not found" });
    }
    res.json({ message: "Item partially updated", item_id: itemId, item });
});

app.delete('/items/:item_id', (req, res) => {
    const itemId = req.params.item_id;
    if (itemId == 0) {
        return res.status(404).json({ error: "Item not found" });
    }
    res.json({ message: `Item ${itemId} deleted` });
});

app.get('/server-error', (req, res) => {
    res.status(500).json({ error: "Internal Server Error" });
});

app.get('/redirect', (req, res) => {
    res.redirect(301, '/');
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
