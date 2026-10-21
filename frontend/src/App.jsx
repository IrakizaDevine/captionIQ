import { useState } from 'react'
import { generateCaptions } from './service/api.js'
import Header from './components/header.jsx'
import CaptionForm from './components/CaptionForm.jsx'
import ResultsPanel from './components/ResultsPanel.jsx'

function App() {
  const [photo, setPhoto] = useState(null)
  const [context, setContext] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    if (!photo || loading) return

    setLoading(true)
    setError('')
    setResults(null)

    try {
      const response = await generateCaptions(photo, context)
      setResults(response.captions)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-container">
      <Header />
      <form className="caption-workspace" onSubmit={handleSubmit}>
        <CaptionForm
          photo={photo}
          context={context}
          loading={loading}
          error={error}
          onPhotoChange={setPhoto}
          onContextChange={setContext}
        />
        <ResultsPanel results={results} loading={loading} />
      </form>
    </main>
  )
}

export default App
