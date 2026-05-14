Mobile frontend guide (Expo)

This repository already has an `apps/mobile` React Native app. If you prefer a fresh Expo-based app for testing, use the steps below.

1. Install Expo CLI (if needed):

```bash
npm install -g expo-cli
```

2. Create a new Expo app in `apps/mobile_new`:

```bash
cd apps
expo init mobile_new
# choose a blank template
```

3. Use environment variable `OLLAMA_API_URL` or `VITE_OLLAMA_URL` in your native code to point to the local Ollama server (`http://localhost:11434`).

Notes

- On mobile devices, `localhost` refers to the device. When testing on a physical device, point the app to your machine IP (e.g. `http://192.168.1.5:11434`) or use Expo tunnel.
