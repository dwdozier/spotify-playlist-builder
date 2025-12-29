import { createFileRoute } from '@tanstack/react-router'
import { Settings as SettingsIcon, Link2, ExternalLink } from 'lucide-react'

export const Route = createFileRoute('/settings')({
  component: Settings,
})

function Settings() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <SettingsIcon className="h-6 w-6" />
          User Settings
        </h2>
        <p className="text-slate-600 mt-1">Manage your account and connected services.</p>
      </div>

      <section className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-6 border-b border-slate-200 bg-slate-50/50">
          <h3 className="font-semibold text-lg flex items-center gap-2">
            <Link2 className="h-5 w-5 text-indigo-600" />
            Connected Services
          </h3>
        </div>
        <div className="p-6 space-y-6">
          <div className="flex items-center justify-between p-4 rounded-lg border border-slate-100 bg-white shadow-sm">
            <div className="flex items-center gap-4">
              <div className="h-10 w-10 bg-[#1DB954]/10 rounded-full flex items-center justify-center">
                <img src="https://www.spotify.com/favicon.ico" className="h-5 w-5" alt="Spotify" />
              </div>
              <div>
                <h4 className="font-medium text-slate-900">Spotify</h4>
                <p className="text-sm text-slate-500">Enable playlist building and syncing.</p>
              </div>
            </div>
            <button className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 transition-colors">
              Connect
              <ExternalLink className="h-4 w-4" />
            </button>
          </div>

          <div className="flex items-center justify-between p-4 rounded-lg border border-slate-100 bg-white shadow-sm opacity-60">
            <div className="flex items-center gap-4">
              <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">
                A
              </div>
              <div>
                <h4 className="font-medium text-slate-900">Apple Music</h4>
                <p className="text-sm text-slate-500 italic">Coming soon...</p>
              </div>
            </div>
            <button disabled className="px-4 py-2 rounded-md bg-slate-100 text-slate-400 text-sm font-medium cursor-not-allowed">
              Locked
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}
