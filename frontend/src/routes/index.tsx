import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/')({
  component: Index,
})

function Index() {
  return (
    <div className="p-2">
      <h1 className="text-3xl font-bold underline">
        Welcome to Playlist Builder
      </h1>
      <p className="mt-4 text-slate-600">
        Generate and manage your playlists with AI and type-safe verification.
      </p>
    </div>
  )
}
