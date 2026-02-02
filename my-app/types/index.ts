export interface Choice {
  id: number;
  text: string;
  votes: number;
}

export interface Question {
  id: number;
  question: string;
  created_date: string;
  totalVotes: number;
  choices: Choice[];
}
