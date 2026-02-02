import 'dotenv/config';
import app from "./app.js";

const PORT = process.env.PORT || 3002;

app.get('/', (_req, res) => {
  res.json({ ok: true });
});

app.listen(PORT, () => {
  console.log(`BFF running on http://localhost:${PORT}`);
});
