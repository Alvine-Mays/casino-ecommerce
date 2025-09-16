import { Outlet, Link, useLocation } from 'react-router-dom'

// Layout staff avec navigation latérale (sections)
export default function App() {
  const { pathname } = useLocation()
  const NavLink = ({ to, children }) => (
    <Link to={to} className={`block px-3 py-2 rounded ${pathname===to? 'bg-[#E30613] text-white':'hover:bg-gray-100'}`}>{children}</Link>
  )
  return (
    <div className="min-h-screen">
      <header className="bg-[#E30613] text-white p-4 font-bold">Staff — Administration</header>
      <div className="grid grid-cols-12 gap-0">
        <aside className="col-span-12 md:col-span-3 lg:col-span-2 border-r p-3 space-y-2">
          <div className="text-xs uppercase text-gray-500 px-3">Sections</div>
          <NavLink to="/orders">Commandes</NavLink>
          <NavLink to="/products">Produits</NavLink>
          <NavLink to="/inventory">Stocks</NavLink>
          <NavLink to="/categories">Catégories</NavLink>
          <NavLink to="/users">Utilisateurs</NavLink>
          <NavLink to="/analytics">Rapports</NavLink>
        </aside>
        <main className="col-span-12 md:col-span-9 lg:col-span-10 p-4">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
