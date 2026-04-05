# Personal Agent Web Dashboard

A full-stack AI-powered text transformation platform with a FastAPI backend and React frontend.

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Setup

#### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run backend
python main.py
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The dashboard will be available at `http://localhost:5173`

### Architecture

```
┌────────────────────────────────┐
│   React Dashboard              │
│   (http://localhost:5173)      │
├────────────────────────────────┤
│   Vite Dev Server              │
│   Proxy: /api → localhost:8000 │
└────────────┬───────────────────┘
             │ HTTP/REST
             │
┌────────────▼───────────────────┐
│   FastAPI Backend              │
│   (http://localhost:8000)      │
├────────────────────────────────┤
│  • Humanize Routes             │
│  • Profile Routes              │
│  • History/Stats Routes        │
│  • Batch Processing            │
├────────────────────────────────┤
│   PersonalAgentService         │
│   (Singleton)                  │
├────────────────────────────────┤
│  • Gemini API Wrapper          │
│  • Config Loader               │
│  • File Handler                │
└────────────────────────────────┘
```

## API Endpoints

### Humanize
- `POST /api/humanize` - Humanize text with tone profile
- Request: `{ text, tone, doc_type?, instruction? }`
- Response: `{ original, humanized, tone, input_length, output_length, timestamp }`

### Profiles
- `GET /api/profiles` - List all tone profiles
- `GET /api/types` - List document types
- `GET /api/profile/{name}` - Get specific profile

### Operations
- `POST /api/summarize` - Summarize text
- `POST /api/takeaways` - Extract key takeaways
- `POST /api/batch` - Batch process files (multipart/form-data)

### History & Analytics
- `GET /api/history?limit=50` - Get operation history
- `GET /api/stats` - Get usage statistics
- `GET /api/history/count` - Get total operation count

### Health
- `GET /health` - Health check
- `GET /` - API info
- `GET /api/ping` - Ping endpoint

## Frontend Features

### Components

1. **ToneSelector** - Grid of tone profiles with auto-detection by document type
2. **TextEditor** - Input textarea with character count
3. **PreviewPanel** - Side-by-side preview with copy button and statistics
4. **BatchUpload** - Drag-and-drop file upload with progress tracking
5. **HistoryLog** - Scrollable operation history
6. **StatsPanel** - Usage statistics and metrics

### Pages/Tabs

1. **Humanize Tab** - Main humanization interface
   - Choose tone profile
   - Select document type
   - Add custom instructions
   - Live preview of results
   - Copy to clipboard

2. **Summarize Tab** - Text summarization
   - Quick summarization interface
   - Results display

3. **Batch Tab** - Batch file processing
   - Drag-and-drop upload
   - Multi-file processing
   - Success/failure tracking

4. **History Tab** - Operation history & statistics
   - Recent operations log
   - Usage statistics
   - Compression metrics

## Environment Variables

### Backend (.env)
```
GEMINI_API_KEY=your_key_here
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173
LOG_LEVEL=INFO
OUTPUT_DIR=./output
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=52428800
```

### Frontend (Vite)
Frontend uses proxy configuration in `vite.config.js` to forward API calls to backend

## Development Workflow

### Running Both in Development

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 (Optional) - CLI:**
```bash
cd personal_agent
python cli.py humanize "Your text" --tone osha_formal
```

### Building for Production

**Backend:**
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with gunicorn (production WSGI server)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app.main:app"
```

**Frontend:**
```bash
npm run build
# Output in: frontend/dist/
```

## Testing

### Manual Testing
1. Start backend and frontend (see Development Workflow)
2. Navigate to `http://localhost:5173`
3. Test humanize with different tones
4. Test batch upload
5. Check history and stats

### API Testing with curl

```bash
# Get profiles
curl http://localhost:8000/api/profiles

# Humanize text
curl -X POST http://localhost:8000/api/humanize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here",
    "tone": "osha_formal"
  }'

# Get history
curl http://localhost:8000/api/history

# Health check
curl http://localhost:8000/health
```

## Debugging

### Backend Logs
- Check `backend/logs/` directory
- FastAPI automatic docs: `http://localhost:8000/docs`

### Frontend Console
- Browser DevTools (F12)
- Check Network tab for API calls
- Check Console for JavaScript errors

### Common Issues

**CORS Error**
- Ensure `CORS_ORIGINS` in `.env` includes frontend URL
- Clear browser cache

**API Connection Failed**
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS configuration

**Missing Profiles**
- Verify `personal_agent/config/tone_profiles.json` exists
- Backend service initializes profiles on startup

## Extending the Dashboard

### Adding a New Route
1. Create route function in `backend/app/routes/`
2. Use `@router.post()` or `@router.get()` decorator
3. Include router in `app/main.py`
4. Add corresponding API call in `frontend/src/api.js`

### Adding a New Component
1. Create `.jsx` file in `frontend/src/components/`
2. Export default function
3. Import in `App.jsx`
4. Add to appropriate tab/section

### Adding a New Tone Profile
1. Edit `personal_agent/config/tone_profiles.json`
2. Add new entry to `profiles` object
3. Optionally add to `document_types` defaults
4. No restart needed - profiles reload dynamically

## Performance Considerations

- **Caching**: Add Redis caching for frequent operations
- **Queuing**: Add Celery for long-running batch jobs
- **Database**: Move from JSONL to PostgreSQL for scalability
- **Monitoring**: Integrate OpenTelemetry for performance metrics

## Security Considerations

- API key stored in `.env` (not committed)
- CORS whitelist for allowed origins
- Input validation on all endpoints
- File upload size limits enforced
- HTTPS recommended for production

## Future Enhancements

- [ ] WebSocket for real-time streaming results
- [ ] Multi-user support with authentication
- [ ] Database backend for operation history
- [ ] Advanced metrics and analytics dashboard
- [ ] Tone profile training from user edits
- [ ] Export to PDF/DOCX
- [ ] Diff viewer for before/after
- [ ] Scheduled batch jobs
- [ ] Integration with external services

## Troubleshooting

### Can't connect to API
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check logs
tail backend/logs/*.log
```

### Missing dependencies
```bash
# Backend
pip install -r backend/requirements.txt

# Frontend
npm install
```

### Port already in use
```bash
# Change ports in .env (backend) and vite.config.js (frontend)
# Or kill existing process: lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill
```

## Support

For issues with:
- **Backend/API**: Check `backend/logs/` and review `app/main.py`
- **Frontend**: Check browser console and network tab
- **Personal Agent CLI**: See `personal_agent/README.md`

## Architecture Summary

This is a **three-tier architecture**:

1. **Presentation Layer**: React dashboard (TailwindCSS styled)
2. **API Layer**: FastAPI with modular routes
3. **Service Layer**: PersonalAgentService wrapping CLI modules
4. **Data Layer**: Gemini API, local file operations

**Key Design Decisions**:
- Singleton pattern for PersonalAgentService (one instance per backend)
- Shared logging between CLI and API (JSONL format)
- Modular route structure (each operation type in separate file)
- Reusable components in React (ToneSelector, TextEditor, etc)
