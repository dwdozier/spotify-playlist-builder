import { apiClient } from './client'

export interface Track {
  artist: string
  track: string
  album?: string
  version?: string
  duration_ms?: number
}

export interface GenerationRequest {
  prompt: string
  count?: number
  artists?: string
}

export interface VerificationRequest {
  tracks: Track[]
}

export interface VerificationResponse {
  verified: Track[]
  rejected: string[]
}

export interface Playlist {
  id: string
  name: string
  description?: string
  public: boolean
  status: 'draft' | 'transmitted'
  provider?: string
  provider_id?: string
  content_json: { tracks: Track[] }
}

export interface PlaylistCreate {
  name: string
  description?: string
  public: boolean
  tracks: Track[]
}

export interface PlaylistBuildRequest {
  playlist_id?: string
  playlist_data?: PlaylistCreate
}

export interface PlaylistGenerationResponse {
  title: string
  description?: string
  tracks: Track[]
}

export const playlistService = {
  generate: (req: GenerationRequest) =>
    apiClient<PlaylistGenerationResponse>('/playlists/generate', {
      method: 'POST',
      body: JSON.stringify(req),
    }),

  verify: (req: VerificationRequest) =>
    apiClient<VerificationResponse>('/playlists/verify', {
      method: 'POST',
      body: JSON.stringify(req),
    }),

  create: (req: PlaylistCreate) =>
    apiClient<Playlist>('/playlists/', {
      method: 'POST',
      body: JSON.stringify(req),
    }),

  getMyPlaylists: () =>
    apiClient<Playlist[]>('/playlists/me'),

  getPlaylist: (id: string) =>
    apiClient<Playlist>(`/playlists/${id}`),

  update: (id: string, req: PlaylistCreate) =>
    apiClient<Playlist>(`/playlists/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(req),
    }),

  build: (req: PlaylistBuildRequest) =>
    apiClient<BuildResponse>('/playlists/build', {
      method: 'POST',
      body: JSON.stringify(req),
    }),
}
