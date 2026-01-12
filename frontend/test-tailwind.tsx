// Simple test component to verify Tailwind is working
export default function TailwindTest() {
  return (
    <div className="p-6 bg-blue-200 text-red-600">
      <h1 className="text-3xl font-bold text-green-700">Tailwind Test</h1>
      <p className="text-lg text-purple-500">If you see colors, Tailwind is working!</p>
      <div className="mt-4 p-4 bg-yellow-100 border-2 border-dashed border-red-500">
        <p className="text-center text-blue-800">This box should have a dashed border</p>
      </div>
    </div>
  );
}