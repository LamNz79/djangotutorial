import cors from 'cors';
import express from 'express';
import pollsRouter from './routes/polls.js';

const app = express();

app.use(cors());
app.use(express.json());

app.use('/polls', pollsRouter);

app.get('/health', (_req, res) => {
  res.json({ status: 'ok' });
});

export default app;
