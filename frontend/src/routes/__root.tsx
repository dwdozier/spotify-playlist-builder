import { createRootRoute, Link, Outlet } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/router-devtools'

export const Route = createRootRoute({
  component: () => (
    <>
      <div className="p-4 flex gap-4 bg-slate-900 text-white items-center">
        <div className="font-bold mr-4 text-xl tracking-tight">Playlist Builder</div>
        <Link to="/" className="hover:text-indigo-300 [&.active]:text-indigo-400 [&.active]:font-bold transition-colors">
          Home
        </Link>
        <Link to="/playlists" className="hover:text-indigo-300 [&.active]:text-indigo-400 [&.active]:font-bold transition-colors">
          Generator
        </Link>
        <div className="flex-grow" />
        <Link to="/settings" className="hover:text-indigo-300 [&.active]:text-indigo-400 [&.active]:font-bold transition-colors">
          Settings
        </Link>
        <Link to="/login" className="px-4 py-1 rounded bg-indigo-600 hover:bg-indigo-500 transition-colors">
          Login
        </Link>
      </div>
      <hr />
      <div className="container mx-auto p-4">
        <Outlet />
      </div>
      <TanStackRouterDevtools />
    </>
  ),
})
