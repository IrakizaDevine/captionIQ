import { useState } from 'react'
import { platforms } from '../utils/platforms'

export default function ResultsPanel({ results, loading }) {
  const [copiedKey, setCopiedKey] = useState(null)

  async function handleCopy(key, text) {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedKey(key)
    } catch {
      setCopiedKey(null)
    }
  }

  return (
    <section className="panel results-panel" aria-live="polite">
      <p className="results-heading">Your captions</p>
      <div className="results-scroll-area">
        {!results && !loading && (
          <div className="results-empty-state">
            <strong>Nothing yet</strong>
            <span>Add a photo to get started.</span>
            <div className="platform-badges" aria-label="Caption platforms">
              {platforms.map(([, label]) => <span key={label}>{label}</span>)}
            </div>
          </div>
        )}
        {loading && (
          <div className="caption-loading-list">
            {platforms.map(([, label]) => (
              <div className="caption-loading-card" key={label}><strong>{label}</strong><span /></div>
            ))}
          </div>
        )}
        {results && (
          <div className="caption-result-list">
            {platforms.map(([key, label]) => (
              <article className="caption-result-card" key={key}>
                <div className="caption-card-header">
                  <strong>{label}</strong>
                  <button
                    className="copy-caption-button"
                    type="button"
                    aria-label={copiedKey === key ? `${label} caption copied` : `Copy ${label} caption`}
                    title={copiedKey === key ? 'Copied' : `Copy ${label} caption`}
                    onClick={() => handleCopy(key, results[key].text)}
                  >
                    {copiedKey === key ? (
                      <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path d="m5 12 4 4L19 6" />
                      </svg>
                    ) : (
                      <svg viewBox="0 0 24 24" aria-hidden="true">
                        <rect x="8" y="8" width="12" height="12" rx="2" />
                        <path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2" />
                      </svg>
                    )}
                  </button>
                </div>
                <p>{results[key].text}</p>
                <small>{results[key].character_count} characters</small>
              </article>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}
