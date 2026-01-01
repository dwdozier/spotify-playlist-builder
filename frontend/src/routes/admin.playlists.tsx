import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { Disc, Music, Globe, Lock } from 'lucide-react'

export const Route = createFileRoute('/admin/playlists')({
  component: AdminPlaylists,
})

interface AdminPlaylist {
  id: string
  name: string
  description: string
  public: boolean
  user_id: string
}

function AdminPlaylists() {
  const { data: playlists, isLoading } = useQuery<AdminPlaylist[]>({
    queryKey: ['admin-playlists'],
    queryFn: async () => {
      const res = await fetch('/api/v1/admin/playlists')
      if (!res.ok) throw new Error('Unauthorized')
      return res.json()
    }
  })

  if (isLoading) return <div className="flex justify-center p-20"><Disc className="animate-spin w-12 h-12 text-retro-teal" /></div>

  return (
    <div className="space-y-8">
      <h2 className="text-4xl font-display text-retro-dark uppercase italic tracking-tight">
        Archive Surveillance
      </h2>

      <div className="bg-white rounded-2xl border-8 border-retro-dark overflow-hidden shadow-retro">
        <table className="min-w-full divide-y-4 divide-retro-dark">
          <thead className="bg-retro-pink">
            <tr>
              <th className="px-6 py-4 text-left font-display text-retro-dark uppercase tracking-widest border-r-4 border-retro-dark">Playlist</th>
              <th className="px-6 py-4 text-left font-display text-retro-dark uppercase tracking-widest border-r-4 border-retro-dark">Visibility</th>
              <th className="px-6 py-4 text-left font-display text-retro-dark uppercase tracking-widest">Citizen ID</th>
            </tr>
          </thead>
          <tbody className="divide-y-4 divide-retro-dark bg-retro-cream">
            {playlists?.map((playlist) => (
              <tr key={playlist.id} className="hover:bg-retro-pink/10 transition-colors">
                <td className="px-6 py-4 border-r-4 border-retro-dark">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white rounded-lg border-2 border-retro-dark">
                      <Music className="w-5 h-5 text-retro-dark" />
                    </div>
                    <div>
                      <div className="font-body font-bold text-retro-dark leading-tight">{playlist.name}</div>
                      <div className="text-xs text-retro-dark/60 font-body italic">{playlist.description || 'No description'}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 border-r-4 border-retro-dark">
                  {playlist.public ? (
                    <div className="flex items-center gap-2 text-retro-teal font-display text-sm">
                      <Globe className="w-4 h-4" /> BROADCAST
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-retro-dark/40 font-display text-sm">
                      <Lock className="w-4 h-4" /> PRIVATE
                    </div>
                  )}
                </td>
                <td className="px-6 py-4 font-body text-xs text-retro-dark/60">
                  {playlist.user_id}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
