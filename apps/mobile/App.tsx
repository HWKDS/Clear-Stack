/**
 * Main App Entry Point
 * Initializes the application with navigation and state management
 */
import React from "react";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { RootNavigator } from "@/navigation/RootNavigator";

/**
 * App Component
 * Root component wrapped with gesture handler for navigation
 */
export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <RootNavigator />
    </GestureHandlerRootView>
  );
}
