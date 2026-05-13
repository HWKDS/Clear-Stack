/**
 * Auth Screen
 * Initial login screen - generates API key on first launch
 */
import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  SafeAreaView,
  TextInput,
  Alert,
} from "react-native";
import { useAuth, useLogin } from "@/hooks";
import { LoadingSpinner, ErrorMessage } from "@/components";

export function AuthScreen() {
  const { isLoading: authLoading } = useAuth();
  const { login, isLoading: loginLoading, error, setError } = useLogin();
  const [keyName, setKeyName] = useState("Mobile App");

  const handleLogin = async () => {
    try {
      setError(null);
      const response = await login(keyName);
      Alert.alert(
        "Success",
        "API key created and saved. You can now access PulseHub!",
      );
    } catch (err) {
      // Error is already set in useLogin
      console.error("Login error:", err);
    }
  };

  if (authLoading) {
    return <LoadingSpinner />;
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.logo}>PulseHub</Text>
          <Text style={styles.subtitle}>
            AI-Powered Unified Notification Hub
          </Text>
        </View>

        {/* Features List */}
        <View style={styles.features}>
          <FeatureItem icon="✓" text="Unified notification dashboard" />
          <FeatureItem icon="✓" text="AI-powered prioritization" />
          <FeatureItem icon="✓" text="Daily intelligent digests" />
          <FeatureItem icon="✓" text="Privacy-first design" />
        </View>

        {/* Error Message */}
        {error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>{error}</Text>
          </View>
        )}

        {/* Key Name Input */}
        <View style={styles.form}>
          <Text style={styles.label}>API Key Name</Text>
          <TextInput
            style={styles.input}
            placeholder="e.g., My Mobile App"
            value={keyName}
            onChangeText={setKeyName}
            editable={!loginLoading}
            placeholderTextColor="#9CA3AF"
          />
        </View>

        {/* Login Button */}
        <Pressable
          style={({ pressed }) => [
            styles.loginButton,
            {
              opacity: pressed || loginLoading ? 0.7 : 1,
            },
          ]}
          onPress={handleLogin}
          disabled={loginLoading || !keyName.trim()}
        >
          {loginLoading ? (
            <LoadingSpinner size="small" color="#FFFFFF" />
          ) : (
            <Text style={styles.loginButtonText}>Get Started</Text>
          )}
        </Pressable>

        {/* Info Text */}
        <Text style={styles.infoText}>
          First login? This will create an API key securely stored on your
          device.
        </Text>
      </View>
    </SafeAreaView>
  );
}

/**
 * Feature Item Component
 */
function FeatureItem({ icon, text }: { icon: string; text: string }) {
  return (
    <View style={styles.featureItem}>
      <Text style={styles.featureIcon}>{icon}</Text>
      <Text style={styles.featureText}>{text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F9FAFB",
  },
  content: {
    flex: 1,
    padding: 20,
    justifyContent: "space-between",
  },
  header: {
    alignItems: "center",
    marginTop: 40,
    marginBottom: 40,
  },
  logo: {
    fontSize: 40,
    fontWeight: "700",
    color: "#3B82F6",
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: "#6B7280",
    textAlign: "center",
  },
  features: {
    marginVertical: 30,
    gap: 12,
  },
  featureItem: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },
  featureIcon: {
    fontSize: 20,
    color: "#10B981",
  },
  featureText: {
    fontSize: 14,
    color: "#374151",
    flex: 1,
  },
  errorContainer: {
    backgroundColor: "#FEE2E2",
    borderLeftWidth: 4,
    borderLeftColor: "#DC2626",
    padding: 12,
    borderRadius: 4,
    marginBottom: 16,
  },
  errorText: {
    color: "#DC2626",
    fontSize: 14,
  },
  form: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: "600",
    color: "#374151",
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: "#D1D5DB",
    borderRadius: 6,
    padding: 12,
    fontSize: 14,
    backgroundColor: "#FFFFFF",
  },
  loginButton: {
    backgroundColor: "#3B82F6",
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: "center",
    marginBottom: 16,
  },
  loginButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
  infoText: {
    fontSize: 12,
    color: "#6B7280",
    textAlign: "center",
  },
});
