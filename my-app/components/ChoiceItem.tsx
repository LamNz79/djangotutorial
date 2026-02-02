'use client';

import { apiPath } from '@/shared/api';
import { useState } from 'react';

interface ChoiceProps {
    choice: {
        id: number;
        text: string;
        votes: number;
    };
    onVoted: () => void;
}


export default function ChoiceItem({ choice, onVoted }: ChoiceProps) {
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleVote = async (action: 'vote' | 'unvote') => {
        setError(null);
        setLoading(true);

        try {
            const res = await fetch(
                `${apiPath}/polls/${action}/`,
                {
                    method: 'POST',
                    headers: {
                        // Authorization: `Bearer ${localStorage.getItem('access')}`,
                        Authorization: `Bearer ${process.env.NEXT_PUBLIC_API_TOKEN ?? ''}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        "choiceId": choice.id
                    })
                }
            );

            if (!res.ok) {
                const data = await res.json();
                setError(data.error || 'Vote failed');
                return;
            }

            // 🔑 do NOT update local counters
            // ask parent to refetch authoritative data
            onVoted();
        } catch {
            setError('Failed to connect to server');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-3 border rounded-lg">
            <div className="flex justify-between items-center">
                <span className="font-medium text-gray-900">{choice.text}</span>
                <span className="text-sm text-gray-900">
                    {choice.votes} votes
                </span>
            </div>

            {error && <p className="text-xs text-red-500 mt-1">{error}</p>}

            <button
                onClick={() => handleVote('vote')}
                disabled={loading}
                className="mt-2 px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50 mr-2"
            >
                Vote
            </button>
            <button
                onClick={() => handleVote('unvote')}
                disabled={loading}
                className="ml-2 mt-2 px-3 py-1 bg-red-600 text-white rounded disabled:opacity-50"
            >
                Unvote
            </button>
        </div>
    );
}
