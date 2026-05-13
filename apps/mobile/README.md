# PulseHub Mobile App

Expo React Native mobile application for PulseHub - AI-powered unified notification hub.

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Expo CLI: `npm install -g expo-cli`
- iOS Simulator (Mac) or Android Emulator

### Installation

```bash
# Navigate to mobile app directory
cd apps/mobile

# Install dependencies
npm install

# Start the development server
npm start
```

Then press:

- `i` - Open in iOS Simulator (Mac only)
- `a` - Open in Android Emulator
- `w` - Open in web browser
- `j` - Open debugger

### Environment Setup

Create a `.env` file in the root of this directory:

```env
EXPO_PUBLIC_API_URL=http://localhost:8000
```

If building for production, update to your backend URL.

## Project Structure

```
src/
├── lib/
│   ├── api.ts           # API client with axios
│   └── config.ts        # Configuration and endpoints
├── types/
│   └── index.ts         # TypeScript type definitions
├── store/
│   ├── auth.ts          # Auth state (Zustand)
│   └── notifications.ts # Notification state
├── hooks/
│   ├── useAuth.ts       # Auth hook
│   ├── useNotifications.ts
│   └── useLogin.ts      # Login flow hook
├── components/
│   ├── NotificationCard.tsx
│   ├── LoadingSpinner.tsx
│   └── ErrorMessage.tsx
├── screens/
│   ├── AuthScreen.tsx       # Login/signup
│   ├── DashboardScreen.tsx  # Notifications list
│   ├── DigestScreen.tsx     # Daily digest
│   └── SettingsScreen.tsx   # Settings
├── navigation/
│   └── RootNavigator.tsx    # Navigation setup
└── App.tsx                  # App root
```

## Features

✅ **Authentication** - Secure API key management with device storage
✅ **Notifications Dashboard** - View notifications with priority badges
✅ **Daily Digest** - Generate AI-powered summaries
✅ **Settings** - Account management and preferences
✅ **Real-time Sync** - Integrates with FastAPI backend

## Connecting to Backend

The app automatically connects to the FastAPI backend via the API URL configured in your environment.

### First Login

1. Launch the app
2. Enter a name for your API key (e.g., "My Mobile App")
3. Tap "Get Started"
4. The app will create a secure API key and save it locally

### Using the App

- **Dashboard**: View all your notifications, filtered by priority
- **Digest**: Generate a daily AI-powered summary
- **Settings**: Manage your account and preferences

## Technologies Used

- **Expo** - React Native framework for iOS/Android
- **TypeScript** - Type-safe development
- **React Navigation** - Navigation and routing
- **Zustand** - State management
- **Axios** - HTTP client
- **expo-secure-store** - Secure credential storage

## Available Scripts

```bash
npm start       # Start development server
npm run android # Run on Android emulator
npm run ios     # Run on iOS simulator
npm run web     # Run in web browser
npm run test    # Run tests
npm run type-check # Check TypeScript
```

## Deployment

To build for production:

```bash
# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android
```

Requires EAS account. See [Expo documentation](https://docs.expo.dev/eas/) for details.

## Troubleshooting

### API Connection Issues

- Verify the backend is running: `http://localhost:8000/health`
- Check `EXPO_PUBLIC_API_URL` in your environment
- For Android emulator, use `http://10.0.2.2:8000` instead of localhost

### Secure Storage Not Working

- On iOS simulator, reboot simulator and reinstall app
- On Android, ensure the app has appropriate permissions

### Dependencies Not Installing

```bash
npm install
npx expo prebuild --clean
npm start
```

## Learning Resources

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Docs](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)
- [Zustand Documentation](https://github.com/pmndrs/zustand)

## Support

For issues with the backend API, see [../../apps/ai_service/README.md](../../apps/ai_service/README.md)
