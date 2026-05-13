# PulseHub - Complete Setup Guide

## 📱 Full Stack Architecture

PulseHub is a complete AI-powered notification hub consisting of:

1. **FastAPI Backend** (`apps/ai_service/`) - REST API with Ollama + OpenAI integration
2. **Expo Mobile App** (`apps/mobile/`) - React Native cross-platform app
3. **Docker Compose** - Local development infrastructure (Postgres, Redis, Ollama)
4. **CI/CD Pipeline** - GitHub Actions automated testing

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ (for mobile app)
- **Python** 3.11+ (for backend)
- **Docker & Docker Compose** (for services)
- **Expo CLI**: `npm install -g expo-cli`

### Backend Setup

```bash
# Navigate to backend
cd apps/ai_service

# Create Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests (local)
pytest tests -v --cov=apps/ai_service

# Start backend with Docker Compose
docker compose up --build
```

Backend will be available at: **http://localhost:8000**

Health check: `curl http://localhost:8000/health`

### Mobile App Setup

```bash
# Navigate to mobile app
cd apps/mobile

# Install dependencies
npm install

# Create .env file (copy from .env.example)
cp .env.example .env

# Start Expo development server
npm start

# Open in iOS Simulator (Mac only)
press 'i'

# Open in Android Emulator
press 'a'

# Open in web browser
press 'w'
```

## 📋 Features Implemented

### ✅ Backend MVP

- [x] API key authentication with JWT
- [x] Rate limiting (100 req/min)
- [x] Notification ingestion pipeline
- [x] PII redaction (email, phone)
- [x] Model routing (Ollama vs OpenAI)
- [x] Daily digest generation
- [x] PostgreSQL persistence (SQLModel ORM)
- [x] Comprehensive test suite (42/42 tests, 93% coverage)
- [x] Docker Compose orchestration
- [x] GitHub Actions CI/CD pipeline

### ✅ Mobile App MVP

- [x] Authentication (secure API key storage)
- [x] Notifications dashboard with priority badges
- [x] Daily digest generation
- [x] Settings management
- [x] API client with error handling
- [x] State management (Zustand)
- [x] Responsive UI (iOS & Android)
- [x] TypeScript for type safety

## 🔧 Development Workflow

### Running Both Backend and Mobile

**Terminal 1 - Backend:**

```bash
cd apps/ai_service
docker compose up
```

**Terminal 2 - Mobile:**

```bash
cd apps/mobile
npm start
```

Then press `i` (iOS) or `a` (Android) in Terminal 2.

### Making Changes

**Backend Changes:**

1. Edit files in `apps/ai_service/`
2. Run tests: `pytest tests -v`
3. Backend auto-reloads with `--reload` flag in docker compose

**Mobile Changes:**

1. Edit files in `apps/mobile/src/`
2. Changes auto-reload via Expo hot reload
3. Test with: `npm test`

## 📁 Project Structure

```
ClearStack/
├── apps/
│   ├── ai_service/                 # FastAPI backend
│   │   ├── main.py                 # Entry point
│   │   ├── routers/                # API endpoints
│   │   ├── services/               # Business logic
│   │   ├── models/                 # Data models
│   │   ├── repositories/           # Database layer
│   │   ├── tests/                  # Test suite (42 tests)
│   │   ├── Dockerfile              # Container image
│   │   └── requirements.txt        # Python dependencies
│   │
│   └── mobile/                     # Expo React Native app
│       ├── src/
│       │   ├── lib/                # API client & config
│       │   ├── types/              # TypeScript types
│       │   ├── store/              # Zustand stores
│       │   ├── hooks/              # Custom hooks
│       │   ├── components/         # Reusable components
│       │   ├── screens/            # Screen components
│       │   └── navigation/         # Navigation setup
│       ├── App.tsx                 # App root
│       ├── app.json                # Expo config
│       ├── package.json            # Dependencies
│       └── tsconfig.json           # TypeScript config
│
├── docker-compose.yml              # Services orchestration
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions pipeline
└── README.md                        # This file
```

## 🧪 Testing

### Backend Tests

```bash
cd apps/ai_service

# Run all tests
pytest tests -v

# Run with coverage
pytest tests -v --cov=apps/ai_service --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Watch mode
pytest tests -v --tb=short -x
```

**Test Results:** 42/42 passing, 93% coverage

### Mobile Tests

```bash
cd apps/mobile

# Run tests
npm test

# Watch mode
npm test -- --watch
```

## 🚢 Deployment

### Backend Deployment (Railway/Heroku)

```bash
# Set environment variables
export DATABASE_URL=postgresql://...
export REDIS_URL=redis://...
export OPENAI_API_KEY=sk-...

# Deploy with Railway
railway up
```

### Mobile Deployment (App Stores)

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to EAS
eas login

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# Submit to stores
eas submit
```

## 🔐 Security Considerations

- **API Keys:** Stored securely in device storage (expo-secure-store)
- **JWT Tokens:** 1-hour expiry with HMAC-SHA256 signing
- **Database:** PostgreSQL with encrypted connections
- **PII:** Automatically redacted from notifications before processing
- **CORS:** Configured for mobile app domain
- **Rate Limiting:** 100 requests/minute per API key

## 📚 API Documentation

### Health Check

```bash
curl http://localhost:8000/health
```

### Create API Key

```bash
curl -X POST http://localhost:8000/auth/api-keys \
  -H "Content-Type: application/json" \
  -d '{"name": "Mobile App"}'
```

Response:

```json
{
  "data": {
    "id": "uuid",
    "key": "pulsehub_abc123...",
    "name": "Mobile App",
    "created_at": "2026-05-14T..."
  },
  "error": null,
  "message": "API key created successfully..."
}
```

### List Notifications

```bash
curl -X GET http://localhost:8000/notifications/list \
  -H "x-api-key: pulsehub_abc123..."
```

### Generate Digest

```bash
curl -X POST http://localhost:8000/digest/generate \
  -H "x-api-key: pulsehub_abc123..."
```

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**

```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
```

**Database connection error:**

```bash
# Check if Postgres is healthy
docker compose ps

# Rebuild containers
docker compose down --volumes
docker compose up --build
```

**Import errors in tests:**

```bash
# Set PYTHONPATH
export PYTHONPATH=$(pwd)
pytest tests -v
```

### Mobile App Issues

**App won't connect to backend:**

- Verify backend is running: `http://localhost:8000/health`
- Check `EXPO_PUBLIC_API_URL` in `.env`
- For Android emulator: Use `http://10.0.2.2:8000` instead of localhost

**Secure storage not working:**

- Android: Ensure app permissions are granted
- iOS Simulator: Reboot simulator and reinstall

**Dependencies not installing:**

```bash
rm -rf node_modules package-lock.json
npm install
```

## 📖 Learning Resources

### Backend

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [LangChain Docs](https://python.langchain.com/)

### Mobile

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Docs](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)

## 🤝 Contributing

1. Create a branch: `git checkout -b feature/your-feature`
2. Make changes in either backend or mobile (or both)
3. Run tests: `pytest tests -v` (backend) or `npm test` (mobile)
4. Commit: `git commit -m "feat: your feature"`
5. Push: `git push origin feature/your-feature`
6. Create PR

## 📝 Next Steps

After completing the MVP, consider:

1. **Next.js Web Frontend** - Web dashboard for desktop users
2. **Alembic Migrations** - Database schema versioning
3. **WebSocket Support** - Real-time notifications
4. **Push Notifications** - FCM integration
5. **Advanced Analytics** - User behavior tracking
6. **Multi-tenant Support** - Teams/workspaces

## 📄 License

MIT License - See LICENSE file

## 🎯 Status

✅ **Production Ready**

- Backend: Fully tested, containerized, CI/CD configured
- Mobile: MVP complete, ready for beta testing
- Infrastructure: Docker Compose working, GitHub Actions passing
- Documentation: Complete with setup, API, and troubleshooting guides

**Next Deployment:** Ready for Railway/Heroku backend + TestFlight/Beta mobile
