export interface DjangoChoice {
    id: number;
    text: string;
    vote_count: number;
}

export interface DjangoQuestion {
    id: number;
    question: string;
    total_votes: number;
    choices: DjangoChoice[];
    created_date?: string
}
