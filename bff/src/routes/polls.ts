import { Request, Response, Router } from 'express';
import { DjangoChoice, DjangoQuestion } from '../../types/django.js';
import { djangoFetch } from '../clients/djangoClient.js';

const router = Router();

router.get('/', async (_req, res) => {
  try {
    const questions = await djangoFetch<DjangoQuestion[]>('/questions/');
    res.json({
      data: {
        questions: questions.map((q) => ({
          id: q.id,
          text: q.question,
          publishedAt: q.created_date,
          totalVotes: q.total_votes,
        })),
      }
    })
  }
  catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to load polls' });
  }
});

router.get("/:id", async (req: Request, res: Response) => {
  const questionId = Number(req.params.id);

  if (Number.isNaN(questionId)) {
    return res.status(400).json({ error: "Invalid question id" });
  }

  try {
    const question = await djangoFetch<DjangoQuestion>(
      `/questions/${questionId}/`
    );

    let userVote: { choiceId: number } | null = null;
    if (req.headers.authorization) {
      try {
        const vote = await djangoFetch<{ choice_id: number }>(
          `/questions/${questionId}/my-vote/`,
          {
            headers: {
              Authorization: req.headers.authorization,
            },
          }
        );
        userVote = { choiceId: vote.choice_id };
      }
      catch (err: any) {
        userVote = null;
      }
    }

    res.json({
      data: {
        question: {
          id: question.id,
          text: question.question,
          publishedAt: question.created_date,
        },
        choices: question.choices.map((c: DjangoChoice) => ({
          id: c.id,
          text: c.text,
          voteCount: c.vote_count,
        })),
        userVote, // Phase 1: aggregation not implemented yet
      },
    });
  } catch (err: any) {
    if (err.status === 404) {
      return res.status(404).json({ error: "Question not found" });
    }

    console.error("Failed to fetch question", err);
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