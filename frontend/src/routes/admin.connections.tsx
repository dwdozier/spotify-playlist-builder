import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { Disc } from 'lucide-react'

export const Route = createFileRoute('/admin/connections')({
  component: AdminConnections,
})

interface AdminConnection {
  id: string
  provider_name: string
  user_id: string
  expires_at: string | null
}

function AdminConnections() {
  const { data: connections, isLoading } = useQuery<AdminConnection[]>({
    queryKey: ['admin-connections'],
    queryFn: async () => {
      const res = await fetch('/api/v1/admin/connections')
      if (!res.ok) throw new Error('Unauthorized')
      return res.json()
    }
  })

  if (isLoading) return <div className="flex justify-center p-20"><Disc className="animate-spin w-12 h-12 text-retro-teal" /></div>

  return (
    <div className="space-y-8">
      <h2 className="text-4xl font-display text-retro-dark uppercase italic tracking-tight">
        Relay Station Control
      </h2>

      <div className="bg-white rounded-2xl border-8 border-retro-dark overflow-hidden shadow-retro">
        <table className="min-w-full divide-y-4 divide-retro-dark">
          <thead className="bg-retro-yellow">
            <tr>
              <th className="px-6 py-4 text-left font-display text-retro-dark uppercase tracking-widest border-r-4 border-retro-dark">Provider</th>
              <th className="px-6 py-4 text-left font-display text-retro-dark uppercase tracking-widest border-r-4 border-retro-dark">Citizen ID</th>
              <th className="px-6 py-4 text-left font-display text-retro-dark uppercase tracking-widest">Expiration</th>
            </tr>
          </thead>
          <tbody className="divide-y-4 divide-retro-dark bg-retro-cream">
            {connections?.map((conn) => (
              <tr key={conn.id} className="hover:bg-retro-yellow/10 transition-colors">
                <td className="px-6 py-4 border-r-4 border-retro-dark">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white rounded-lg border-2 border-retro-dark text-retro-yellow font-bold">
                      {conn.provider_name.charAt(0).toUpperCase()}
                    </div>
                    <div className="font-display uppercase text-retro-dark">{conn.provider_name}</div>
                  </div>
                </td>
                <td className="px-6 py-4 border-r-4 border-retro-dark font-body text-xs text-retro-dark/60">
                  {conn.user_id}
                </td>
                <td className="px-6 py-4 font-body text-sm text-retro-dark">
                  {conn.expires_at ? new Date(conn.expires_at).toLocaleString() : 'N/A'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
