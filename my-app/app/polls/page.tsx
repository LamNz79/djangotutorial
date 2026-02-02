import PollList from "@/components/PollList";
import { apiPath } from "@/shared/api";

// app/polls/page.tsx
export default async function PollsPage() {
  const res = await fetch(`${apiPath}/polls/`, {
    cache: 'no-store', // always fresh
  });

  if (!res.ok) {
    throw new Error('Failed to load polls');
  }

  const questions = await res.json();

  return (
    <div className="min-h-screen bg-gray-50">

      <div className=" max-w-4xl mx-auto px-4 py-10 ">
        <h1 className="text-3xl font-bold mb-8 text-gray-900">All Polls</h1>
        <PollList initialQuestions={questions} />
      </div>
    </div>
  );
}
