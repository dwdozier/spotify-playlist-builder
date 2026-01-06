export class UnauthorizedError extends Error {
  constructor(message: string = 'Session expired. Please login again.') {
    super(message)
    this.name = 'UnauthorizedError'
  }
}

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`/api/v1${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  })

  if (response.status === 401) {
    throw new UnauthorizedError()
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }))
    throw new Error(error.detail || response.statusText)
  }

  return response.json() as Promise<T>
}
