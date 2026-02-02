import { Request, Response, Router } from 'express';
import { DjangoChoice, DjangoQuestion } from '../../types/django.js';
import { djangoFetch } from '../clients/djangoClient.js';

const router = Router();

router.get('/', async (_req, res) => {
  try {
    const data = await djangoFetch<DjangoQuestion[]>('/questions/');
    const polls = data.map((q: DjangoQuestion) => ({
      id: q.id,
      question: q.question,
      totalVotes: q.total_votes,
      choices: q.choices.map((c: DjangoChoice) => ({
        id: c.id,
        text: c.text,
        votes: c.vote_count,
      })),
    }));
    res.json(polls);
  }
  catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to load polls' });
  }
});

router.get("/:id", async (req: Request, res: Response) => {
  const pollId = Number(req.params.id);

  if (Number.isNaN(pollId)) {
    return res.status(400).json({ error: "Invalid poll id" });
  }

  try {
    const poll = await djangoFetch<DjangoQuestion>(`/questions/${pollId}/`);

    res.json({
      id: poll.id,
      question: poll.question,
      totalVotes: poll.total_votes,
      choices: poll.choices.map((c: any) => ({
        id: c.id,
        text: c.text,
        votes: c.vote_count,
      })),
    });
  } catch (err: any) {
    if (err.status === 404) {
      return res.status(404).json({ error: "Poll not found" });
    }

    console.error("Failed to fetch poll", err);
    res.status(500).json({ error: "Internal server error" });
  }
});


/**
 * POST /polls/vote
 * body: { choiceId }
 */
router.post("/vote", async (req: Request, res: Response) => {
  const { choiceId } = req.body;

  if (!choiceId || typeof choiceId !== "number") {
    return res.status(400).json({ error: "choiceId is required" });
  }

  try {
    const result = await djangoFetch<any>(
      "/choices/vote/",
      {
        method: "POST",
        headers: {
          Authorization: req.headers.authorization ?? "",
        },
        body: JSON.stringify({ choice_id: choiceId }),
      }
    );

    res.json({
      id: result.id,
      text: result.text,
      votes: result.vote_count,
    });
  } catch (err: any) {
    if (err.status === 403) {
      return res.status(403).json({ error: "Not allowed to vote" });
    }

    if (err.status === 404) {
      return res.status(404).json({ error: "Choice not found" });
    }

    console.error(err);
    res.status(500).json({ error: "Vote failed" });
  }
});

/**
 * POST /polls/unvote
 * body: { choiceId }
 */
router.post("/unvote", async (req: Request, res: Response) => {
  const { choiceId } = req.body;

  if (!choiceId || typeof choiceId !== "number") {
    return res.status(400).json({ error: "choiceId is required" });
  }

  try {
    const result = await djangoFetch<any>(
      "/choices/un_vote/",
      {
        method: "POST",
        headers: {
          Authorization: req.headers.authorization ?? "",
        },
        body: JSON.stringify({ choice_id: choiceId }),
      }
    );

    res.json({
      id: result.id,
      text: result.text,
      votes: result.vote_count,
    });
  } catch (err: any) {
    if (err.status === 409) {
      return res.status(409).json({ error: "Invalid vote state" });
    }

    if (err.status === 404) {
      return res.status(404).json({ error: "Choice not found" });
    }

    console.error(err);
    res.status(500).json({ error: "Unvote failed" });
  }
});

export default router;