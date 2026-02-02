import PollDashboard from '@/components/PollDashboard';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            Voice Your Opinion
          </h1>
          <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
            Participate in real-time polls, see what others are thinking, and make your vote count.
          </p>
          <div className="mt-8 flex justify-center">
            <Link
              href="/polls"
              className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10 transition-colors"
            >
              View All Polls
            </Link>
          </div>
        </div>

        <PollDashboard />
      </div>
    </div>
  );
}
