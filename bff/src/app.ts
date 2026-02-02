import cors from 'cors';
import express from 'express';
import pollsRouter from './routes/polls.js';
import questionsRouter from './routes/questions.js';
const app = express();

app.use(cors());
app.use(express.json());
app.use('/questions', questionsRouter);
app.use('/polls', pollsRouter);

app.get('/health', (_req, res) => {
  res.json({ status: 'ok' });
});

export default app;
