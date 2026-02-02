'use client';

import { apiPath } from '@/shared/api';
import { Question } from '@/types';
import { useState } from 'react';
import ChoiceItem from './ChoiceItem';

interface Props {
    initialQuestion: Question;
}

export default function PollDetail({ initialQuestion }: Props) {
    const [question, setQuestion] = useState(initialQuestion);
    const [loading, setLoading] = useState(false);

    const refetch = async () => {
        setLoading(true);
        const res = await fetch(
            `${apiPath}/polls/${question.id}/`,
            { cache: 'no-store' }
        );
        const data = await res.json();
        setQuestion(data);
        setLoading(false);
    };

    return (
        <div className="bg-white border rounded-xl p-6">
            <h1 className="text-2xl font-bold mb-2">
                {question.question}
            </h1>

            <p className="text-sm text-gray-500 mb-6">
                {question.totalVotes} total votes
            </p>

            {loading && (
                <p className="text-xs text-gray-400 mb-2">
                    Updating results…
                </p>
            )}

            <div className="space-y-3">
                {question.choices.map(choice => (
                    <ChoiceItem
                        key={choice.id}
                        choice={choice}
                        onVoted={refetch}
                    />
                ))}
            </div>
        </div>
    );
}
