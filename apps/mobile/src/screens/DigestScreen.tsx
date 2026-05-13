/**
 * Digest Screen
 * Daily digest summary view
 */
import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  Pressable,
  ScrollView,
} from "react-native";
import { digestAPI } from "@/lib/api";
import { LoadingSpinner, ErrorMessage } from "@/components";

export function DigestScreen() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [digest, setDigest] = useState<string | null>(null);

  const handleGenerateDigest = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await digestAPI.generateDigest();

      if (response.error) {
        setError(response.error);
        return;
      }

      // Extract digest text from response
      const digestText =
        typeof response.data === "string"
          ? response.data
          : JSON.stringify(response.data);

      setDigest(digestText);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to generate digest";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title}>Daily Digest</Text>
          <Text style={styles.subtitle}>
            AI-powered summary of your notifications
          </Text>
        </View>

        {/* Error Message */}
        {error && (
          <ErrorMessage message={error} onRetry={handleGenerateDigest} />
        )}

        {/* Generate Button */}
        <Pressable
          style={({ pressed }) => [
            styles.generateButton,
            { opacity: pressed || isLoading ? 0.7 : 1 },
          ]}
          onPress={handleGenerateDigest}
          disabled={isLoading}
        >
          {isLoading ? (
            <LoadingSpinner size="small" color="#FFFFFF" />
          ) : (
            <Text style={styles.generateButtonText}>Generate Digest</Text>
          )}
        </Pressable>

        {/* Digest Content */}
        {digest ? (
          <View style={styles.digestCard}>
            <Text style={styles.digestTitle}>Today's Summary</Text>
            <Text style={styles.digestText}>{digest}</Text>
          </View>
        ) : !error && !isLoading ? (
          <View style={styles.placeholderCard}>
            <Text style={styles.placeholderIcon}>📋</Text>
            <Text style={styles.placeholderText}>
              Generate a digest to see a summary of your notifications
            </Text>
          </View>
        ) : null}
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
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: "#6B7280",
  },
  generateButton: {
    backgroundColor: "#3B82F6",
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: "center",
    marginBottom: 20,
  },
  generateButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
  digestCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 8,
    padding: 16,
    borderLeftWidth: 4,
    borderLeftColor: "#3B82F6",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  digestTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#1F2937",
    marginBottom: 12,
  },
  digestText: {
    fontSize: 14,
    color: "#4B5563",
    lineHeight: 22,
  },
  placeholderCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 8,
    padding: 40,
    alignItems: "center",
    borderWidth: 2,
    borderColor: "#E5E7EB",
    borderStyle: "dashed",
  },
  placeholderIcon: {
    fontSize: 48,
    marginBottom: 16,
  },
  placeholderText: {
    fontSize: 14,
    color: "#6B7280",
    textAlign: "center",
  },
});
