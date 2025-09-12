import { Outlet } from 'react-router-dom'

export default function App() {
  return (
    <div>
      <header className="bg-[#E30613] text-white p-4 font-bold">Staff - Click & Collect</header>
      <main className="max-w-5xl mx-auto p-4"><Outlet /></main>
    </div>
  )
}
