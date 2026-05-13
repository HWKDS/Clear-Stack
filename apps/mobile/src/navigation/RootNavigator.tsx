/**
 * Root Navigation
 * Handles auth flow and main app navigation
 */
import React, { useEffect, useState } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { useAuth } from "@/hooks";
import { LoadingSpinner } from "@/components";
import {
  AuthScreen,
  DashboardScreen,
  DigestScreen,
  SettingsScreen,
} from "@/screens";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

/**
 * Main App Navigation (logged in)
 */
function AppTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: "#3B82F6",
        tabBarInactiveTintColor: "#9CA3AF",
        tabBarStyle: {
          backgroundColor: "#FFFFFF",
          borderTopColor: "#E5E7EB",
        },
      }}
    >
      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{
          title: "Notifications",
          tabBarIcon: ({ color }) => (
            <Text style={{ fontSize: 24, color }}>📬</Text>
          ),
        }}
      />

      <Tab.Screen
        name="Digest"
        component={DigestScreen}
        options={{
          title: "Digest",
          tabBarIcon: ({ color }) => (
            <Text style={{ fontSize: 24, color }}>📋</Text>
          ),
        }}
      />

      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          title: "Settings",
          tabBarIcon: ({ color }) => (
            <Text style={{ fontSize: 24, color }}>⚙️</Text>
          ),
        }}
      />
    </Tab.Navigator>
  );
}

/**
 * Root Navigator
 * Conditionally shows Auth or App based on authentication state
 */
export function RootNavigator() {
  const { isAuthenticated, isLoading } = useAuth();
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    // Simulate app ready state
    const timer = setTimeout(() => setIsReady(true), 0);
    return () => clearTimeout(timer);
  }, []);

  if (isLoading || !isReady) {
    return <LoadingSpinner />;
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isAuthenticated ? (
          <Stack.Screen name="App" component={AppTabs} />
        ) : (
          <Stack.Screen
            name="Auth"
            component={AuthScreen}
            options={{
              animationEnabled: false,
            }}
          />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Import Text for tab icons
import { Text } from "react-native";
