import { apiPath } from '@/shared/api';
import { Question } from '@/types';
import Link from 'next/link';

export default async function PollDashboard() {
    const res = await fetch(`${apiPath}/polls/`, {
        headers: {
            Authorization: `Bearer ${process.env.NEXT_PUBLIC_API_TOKEN ?? ''}`,
        },
        cache: 'no-store',
    });

    const questions: Question[] = await res.json();

    const popularPolls = questions
        .sort((a, b) => b.totalVotes - a.totalVotes)
        .slice(0, 3);

    return (
        <div className="mb-12">
            <h2 className="text-2xl font-bold mb-6 text-gray-900">Trending Polls</h2>

            <div className="grid md:grid-cols-3 gap-6">
                {popularPolls.map(poll => (
                    <Link
                        key={poll.id}
                        href={`/polls/${poll.id}`}
                        className="p-6 bg-white rounded-xl border"
                    >
                        <h3 className="font-semibold mb-2 text-gray-900">{poll.question}</h3>
                        <div className="text-3xl font-bold text-blue-600 ">
                            {poll.totalVotes}
                        </div>
                        <div className="text-sm text-gray-500">Total votes</div>
                    </Link>
                ))}
            </div>
        </div>
    );
}
