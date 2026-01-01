import { createFileRoute, redirect, Link } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { ShieldAlert, Users, Music, Link2, Database, ArrowLeft, ExternalLink, Settings } from 'lucide-react'

export const Route = createFileRoute('/admin')({
  beforeLoad: async ({ context }) => {
    const user = await context.auth.getCurrentUser()
    if (!user || !user.is_superuser) {
      throw redirect({ to: '/' })
    }
  },
  component: AdminDashboard,
})

function AdminDashboard() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['admin-stats'],
    queryFn: async () => {
      const res = await fetch('/api/v1/admin/stats')
      if (!res.ok) throw new Error('Unauthorized')
      return res.json()
    }
  })

  return (
    <div className="max-w-6xl mx-auto space-y-12 pb-20">
      {/* Header */}
      <header className="bg-retro-dark p-10 rounded-2xl border-b-8 border-retro-teal shadow-retro relative overflow-hidden">
        <div className="flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex items-center gap-6">
            <div className="bg-retro-yellow p-4 rounded-2xl border-4 border-retro-dark shadow-retro-sm transform -rotate-3">
              <ShieldAlert className="w-12 h-12 text-retro-dark" />
            </div>
            <div>
              <h1 className="text-5xl font-display text-retro-cream uppercase italic tracking-tighter">
                Control Center
              </h1>
              <p className="font-display text-retro-teal text-xl tracking-widest uppercase mt-1">Series 2000 Administrative Interface</p>
            </div>
          </div>
          <Link
            to="/"
            className="flex items-center gap-2 px-8 py-3 bg-retro-pink text-retro-dark font-display text-xl uppercase rounded-xl border-4 border-retro-dark shadow-retro-sm hover:bg-pink-400 active:shadow-none active:translate-x-1 active:translate-y-1 transition-all"
          >
            <ArrowLeft className="w-6 h-6" />
            Exit Command
          </Link>
        </div>
      </header>

      {/* Stats Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <StatCard
          icon={<Users className="w-8 h-8 text-retro-teal" />}
          label="Citizens"
          value={stats?.users}
          loading={isLoading}
          color="teal"
        />
        <StatCard
          icon={<Music className="w-8 h-8 text-retro-pink" />}
          label="Archives"
          value={stats?.playlists}
          loading={isLoading}
          color="pink"
        />
        <StatCard
          icon={<Link2 className="w-8 h-8 text-retro-yellow" />}
          label="Relays"
          value={stats?.connections}
          loading={isLoading}
          color="yellow"
        />
        <StatCard
          icon={<Database className="w-8 h-8 text-retro-chrome" />}
          label="Nodes"
          value={stats?.oauth_accounts}
          loading={isLoading}
          color="chrome"
        />
      </section>

      {/* Operations Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <div className="lg:col-span-2 space-y-12">
          <section className="bg-white p-8 rounded-2xl border-8 border-retro-dark shadow-retro">
            <h2 className="text-3xl font-display text-retro-dark mb-8 flex items-center gap-4 uppercase border-b-4 border-retro-dark pb-4 border-dashed">
              <Settings className="h-8 w-8" />
              Operational Modules
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <ModuleLink
                title="Citizen Management"
                desc="Oversee clearances and privacy settings."
                href="/admin/user"
              />
              <ModuleLink
                title="Archive Surveillance"
                desc="Monitor public broadcasts and clones."
                href="/admin/playlist"
              />
              <ModuleLink
                title="Relay Station Control"
                desc="Manage streaming service connections."
                href="/admin/serviceconnection"
              />
              <ModuleLink
                title="Legacy System"
                desc="Access raw data management protocols."
                href="/admin/"
              />
            </div>
          </section>
        </div>

        <aside className="space-y-8">
          <div className="bg-retro-cream p-8 rounded-2xl border-8 border-retro-dark shadow-retro">
            <h3 className="text-2xl font-display text-retro-dark uppercase mb-4">System Status</h3>
            <div className="space-y-4 font-body font-bold text-sm uppercase tracking-wider text-retro-dark/70">
              <div className="flex justify-between items-center bg-white/50 p-3 rounded border-2 border-retro-dark/10">
                <span>Core Temperature</span>
                <span className="text-retro-teal">Optimal</span>
              </div>
              <div className="flex justify-between items-center bg-white/50 p-3 rounded border-2 border-retro-dark/10">
                <span>AI Synapse</span>
                <span className="text-retro-teal">Stabilized</span>
              </div>
              <div className="flex justify-between items-center bg-white/50 p-3 rounded border-2 border-retro-dark/10">
                <span>Citizen Trust</span>
                <span className="text-retro-pink">Elevated</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  )
}

interface StatCardProps {
  icon: React.ReactNode
  label: string
  value?: number
  loading: boolean
  color: 'teal' | 'pink' | 'yellow' | 'chrome'
}

function StatCard({ icon, label, value, loading, color }: StatCardProps) {
  const colorMap: Record<string, string> = {
    teal: 'bg-retro-teal/10 border-retro-teal',
    pink: 'bg-retro-pink/10 border-retro-pink',
    yellow: 'bg-retro-yellow/10 border-retro-yellow',
    chrome: 'bg-retro-chrome/10 border-retro-chrome',
  }

  return (
    <div className={`p-8 rounded-2xl border-4 border-retro-dark shadow-retro-sm flex flex-col items-center text-center space-y-4 ${colorMap[color]}`}>
      <div className="p-3 bg-white rounded-xl border-2 border-retro-dark shadow-retro-xs">
        {icon}
      </div>
      <div className="space-y-1">
        <div className="text-4xl font-display text-retro-dark tracking-tighter">
          {loading ? '---' : value}
        </div>
        <div className="text-sm font-display text-retro-dark/60 uppercase tracking-widest">
          {label}
        </div>
      </div>
    </div>
  )
}

interface ModuleLinkProps {
  title: string
  desc: string
  href: string
}

function ModuleLink({ title, desc, href }: ModuleLinkProps) {
  return (
    <a
      href={href}
      className="p-6 bg-retro-cream rounded-xl border-4 border-retro-dark shadow-retro-sm hover:shadow-retro hover:bg-white transition-all group"
    >
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-xl font-display text-retro-dark uppercase group-hover:text-retro-teal transition-colors">{title}</h3>
        <ExternalLink className="w-5 h-5 text-retro-dark/30 group-hover:text-retro-teal transition-colors" />
      </div>
      <p className="font-body text-sm text-retro-dark/60 italic leading-relaxed">{desc}</p>
    </a>
  )
}
