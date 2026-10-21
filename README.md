# Photo Caption Generator (CaptionIQ)

Upload a photo, add a short line about the story behind it, and get three captions written for LinkedIn, Facebook/Instagram, and X. The context line does most of the work: the same photo produces generic captions with no context and specific, believable ones with it.

## Features

- One-screen interface: photo upload with preview, optional context field, and a single "Write my captions" button
- Three fixed platforms, each with its own voice and length:
  - **LinkedIn**: professional, warm, reflective (about 2 to 4 sentences)
  - **Facebook/Instagram**: casual and personal, with emojis and hashtags welcome
  - **X**: short and conversational, never more than 280 characters
- Character count on every caption, with a warning on X when it goes over 280
- Copy button on every caption
- Loading state, "still working" message after about 10 seconds, and clear errors with retry that keep your photo and context in place
- Captions stay grounded in the photo and the context you give. They should not invent names, dates, job titles, or events
- Responsive layout (stacks on phones) and dark mode
- Photos and captions are not stored

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite), HTML, CSS, JavaScript |
| Backend and API | Python with FastAPI |
| AI | Google Gemini vision API (free tier), called from the server only |

## How it works

1. The user picks a photo and optionally types a context line in the React page.
2. The browser sends one `multipart/form-data` request to the Python server.
3. The server checks the photo and the context text.
4. The server sends the photo and a prompt to Gemini using an API key that never leaves the server.
5. The server checks Gemini's reply, adds character counts, and returns JSON.
6. React shows three caption cards.

## Project structure

```
caption-app/
├── README.md
├── .gitignore
├── backend/
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── main.py              server setup, CORS, route registration
│   │   ├── config.py            settings read from .env
│   │   ├── routes/captions.py   POST /generate-caption
│   │   ├── validation.py        photo and context checks
│   │   ├── errors.py            error types and the shared error response
│   │   ├── schemas.py           success and error response shapes
│   │   └── services/
│   │       ├── gemini_client.py the Gemini call, with timeout
│   │       ├── prompts.py       the three platform prompts
│   │       └── caption_parser.py checks Gemini's reply, adds counts
│   └── tests/
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── api/captionApi.js    the one place that calls the backend
        ├── hooks/useCaptionGenerator.js   idle, loading, success, error state
        ├── components/          PhotoUpload, ContextField, PlatformLabels,
        │                        GenerateButton, ResultsPanel, CaptionCard,
        │                        ErrorMessage
        ├── mock/fakeResponse.js fake captions for building without the backend
        ├── constants.js
        └── styles/app.css
```

## Getting started

### Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer
- Git
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd caption-app
```

### 2. Run the backend

```bash
cd backend
python -m venv .venv

# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env        # Windows: copy .env.example .env
```

Open `.env` and add your own key (see [Configuration](#configuration)). Then start the server:

```bash
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. FastAPI also serves an interactive test page at `http://localhost:8000/docs`, where you can try the route without the frontend.

### 3. Run the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the address Vite prints, usually `http://localhost:5173`.

## Configuration

Create `backend/.env` from `backend/.env.example`:

```
GEMINI_API_KEY=your-key-here
GEMINI_MODEL=gemini-3.6-flash
MAX_UPLOAD_MB=5
MAX_CONTEXT_CHARS=300
GEMINI_TIMEOUT_SECONDS=30
ALLOWED_ORIGIN=http://localhost:5173
```

The values above for size, length, and timeout are suggestions. Use the numbers your team agrees on.

**Never commit `.env`.** It is listed in `.gitignore`. If a real key is ever committed, revoke it in Google AI Studio and create a new one.

## API

### `POST /generate-caption`

Content type: `multipart/form-data`

| Field | Required | Description |
|---|---|---|
| `photo` | yes | JPG, PNG, or WebP image, up to 5 MB |
| `context` | no | Short text about the story behind the photo |

**Success (200)**

```json
{
  "captions": {
    "linkedin":           { "text": "...", "character_count": 214 },
    "facebook_instagram": { "text": "...", "character_count": 126 },
    "x":                  { "text": "...", "character_count": 198 }
  }
}
```

Character counts use Unicode code points (`len(text)` in Python, `Array.from(text).length` in JavaScript). They are an estimate and may differ slightly from how each platform counts.

**Errors**

Every error uses the same shape:

```json
{ "error": { "code": "FILE_TOO_LARGE", "message": "Please choose a photo under 5 MB." } }
```

| Status | Meaning |
|---|---|
| 400 | Unsupported or invalid image file |
| 413 | Photo is larger than the limit |
| 422 | Context is longer than the limit |
| 429 | The AI service rate limit was reached |
| 502 | The AI replied, but its output was missing, malformed, or failed our checks |
| 503 | The AI service is unavailable or timed out |

## Development notes

- **Build the frontend against the fake response first** (`frontend/src/mock/fakeResponse.js`) so you can work on every interface state without calling the AI and using up free-tier quota.
- **Limits live in two places.** The backend enforces them and is the source of truth. `frontend/src/constants.js` repeats them so the interface can warn early. Change both together.
- **Two layers of validation.** The server validates the browser's request, and it validates Gemini's reply separately, because AI output can be malformed even when the request was fine.
- **The API key stays on the server.** The browser never sees it.

## Testing

```bash
cd backend
pytest
```

Manual checks before a demo:

- [ ] A valid photo with context returns three captions that sound different
- [ ] The same photo with no context returns more generic captions
- [ ] A non-image file shows a clear error and keeps the form filled in
- [ ] A photo over the size limit shows a clear error
- [ ] The X card warns when its caption goes over 280 characters
- [ ] Generating again clears the old captions immediately
- [ ] The Copy button works on every card
- [ ] The layout works on a phone-sized screen and in dark mode

## Troubleshooting

| Problem | Likely cause |
|---|---|
| Browser console shows a CORS error | `ALLOWED_ORIGIN` in `.env` does not match the address Vite is running on |
| Every request returns 503 or 429 | Missing or invalid API key, or the free-tier limit was reached. Wait a minute and try again |
| `ModuleNotFoundError` | The virtual environment is not activated, or `pip install -r requirements.txt` was not run |
| The page cannot reach the backend | The backend is not running, or the frontend is pointing at the wrong port |

## Team

| Role | Area |
|---|---|
| Backend | Server, route, validation, errors, configuration |
| AI | Gemini call, prompts, reply checking, caption quality |
| Frontend | React interface and all screen states |

## Roadmap

Ideas for later, not part of the first version:

- Choose which platforms to generate
- Alt-text and SEO output modes
- Code-snippet output
- Saved history and accounts
- More platforms, languages, and tone controls
- Deployment
