/**
 * Settings Screen
 * User preferences and account management
 */
import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  Pressable,
  ScrollView,
  Alert,
} from "react-native";
import { useAuth } from "@/hooks";

export function SettingsScreen() {
  const { logout, apiKey } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const handleLogout = () => {
    Alert.alert(
      "Log Out",
      "Are you sure you want to log out? You will need to create a new API key to log back in.",
      [
        { text: "Cancel", onPress: () => {}, style: "cancel" },
        {
          text: "Log Out",
          onPress: async () => {
            setIsLoading(true);
            try {
              await logout();
              // Navigation to auth screen will happen automatically
            } finally {
              setIsLoading(false);
            }
          },
          style: "destructive",
        },
      ],
    );
  };

  const handleCopyKey = () => {
    if (apiKey) {
      // Note: In a real app, use react-native-clipboard
      Alert.alert("API Key", "API key copied to clipboard");
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title}>Settings</Text>
        </View>

        {/* Account Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Account</Text>

          <View style={styles.settingItem}>
            <Text style={styles.settingLabel}>API Key</Text>
            <Text style={styles.settingValue}>
              {apiKey ? `${apiKey.substring(0, 8)}...` : "Not configured"}
            </Text>
          </View>

          {apiKey && (
            <Pressable
              style={({ pressed }) => [
                styles.button,
                styles.secondaryButton,
                { opacity: pressed ? 0.7 : 1 },
              ]}
              onPress={handleCopyKey}
            >
              <Text style={styles.secondaryButtonText}>Copy Key</Text>
            </Pressable>
          )}
        </View>

        {/* About Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>

          <View style={styles.settingItem}>
            <Text style={styles.settingLabel}>App Name</Text>
            <Text style={styles.settingValue}>PulseHub</Text>
          </View>

          <View style={styles.settingItem}>
            <Text style={styles.settingLabel}>Version</Text>
            <Text style={styles.settingValue}>1.0.0</Text>
          </View>

          <View style={styles.settingItem}>
            <Text style={styles.settingLabel}>Description</Text>
            <Text style={styles.settingValue}>
              AI-powered unified notification hub
            </Text>
          </View>
        </View>

        {/* Danger Zone */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Danger Zone</Text>

          <Pressable
            style={({ pressed }) => [
              styles.button,
              styles.dangerButton,
              { opacity: pressed || isLoading ? 0.7 : 1 },
            ]}
            onPress={handleLogout}
            disabled={isLoading}
          >
            <Text style={styles.dangerButtonText}>Log Out</Text>
          </Pressable>
        </View>

        {/* Footer */}
        <Text style={styles.footer}>Made with ❤️ for notification sanity</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F9FAFB",
  },
  content: {
    padding: 16,
  },
  header: {
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    color: "#1F2937",
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: "700",
    color: "#6B7280",
    textTransform: "uppercase",
    marginBottom: 12,
  },
  settingItem: {
    backgroundColor: "#FFFFFF",
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 6,
    marginBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#E5E7EB",
  },
  settingLabel: {
    fontSize: 12,
    color: "#6B7280",
    fontWeight: "500",
    marginBottom: 4,
  },
  settingValue: {
    fontSize: 14,
    color: "#1F2937",
    fontWeight: "500",
  },
  button: {
    paddingVertical: 12,
    borderRadius: 6,
    alignItems: "center",
    marginTop: 8,
  },
  secondaryButton: {
    backgroundColor: "#E5E7EB",
  },
  secondaryButtonText: {
    color: "#374151",
    fontWeight: "600",
    fontSize: 14,
  },
  dangerButton: {
    backgroundColor: "#DC2626",
  },
  dangerButtonText: {
    color: "#FFFFFF",
    fontWeight: "600",
    fontSize: 14,
  },
  footer: {
    textAlign: "center",
    color: "#9CA3AF",
    fontSize: 12,
    marginVertical: 40,
  },
});
