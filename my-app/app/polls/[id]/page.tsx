// app/polls/[id]/page.tsx
import PollDetail from '@/components/PollDetail';
import { apiPath } from '@/shared/api';

interface PageProps {
    params: Promise<{ id: string }>;
}

export default async function PollDetailPage({ params }: PageProps) {
    const { id } = await params; // ✅ unwrap the promise
    console.log("🚀 ~ PollDetailPage ~ id:", id)

    const res = await fetch(
        `${apiPath}/polls/${id}/`,
        { cache: 'no-store' }
    );

    if (!res.ok) {
        throw new Error('Poll not found');
    }

    const question = await res.json();

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-3xl mx-auto px-4 py-10">
                <PollDetail initialQuestion={question} />
            </div>
        </div>
    );
}
