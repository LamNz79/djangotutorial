'use client';

import { apiPath } from '@/shared/api';
import { Question } from '@/types';
import { useState } from 'react';
import ChoiceItem from './ChoiceItem';

interface Props {
    initialQuestions: Question[];
}

export default function PollList({ initialQuestions }: Props) {
    const [questions, setQuestions] = useState(initialQuestions);
    const [loading, setLoading] = useState(false);

    const refetch = async () => {
        setLoading(true);
        const res = await fetch(`${apiPath}/polls/`, {
            cache: 'no-store',
        });
        const data = await res.json();
        setQuestions(data);
        setLoading(false);
    };

    return (
        <div className="space-y-8">
            {loading && (
                <p className="text-sm text-gray-900">Refreshing results…</p>
            )}

            {questions.map(question => (
                <div
                    key={question.id}
                    className="bg-white border rounded-xl p-6"
                >
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-lg font-semibold text-gray-900">
                            {question.question}
                        </h2>
                        <span className="text-sm text-gray-900">
                            {question.totalVotes} total votes
                        </span>
                    </div>

                    <div className="space-y-2   ">
                        {question.choices.map(choice => (
                            <ChoiceItem
                                key={choice.id}
                                choice={choice}
                                onVoted={refetch}
                            />
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}
