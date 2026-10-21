const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function generateCaptions(photo, context) {
  const formData = new FormData()
  formData.append('photo', photo)
  formData.append('context', context)

  const response = await fetch(`${API_URL}/generate-caption`, {
    method: 'POST',
    body: formData,
  })

  const body = await response.json()
  if (!response.ok) {
    throw new Error(body?.error?.message ?? 'Caption generation failed.')
  }

  return body
}
