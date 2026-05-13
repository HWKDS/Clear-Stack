/**
 * Notification Card Component
 * Displays a single notification with priority styling
 */
import React from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import type { Notification } from "@/types";

interface NotificationCardProps {
  notification: Notification;
  onPress?: () => void;
}

export function NotificationCard({
  notification,
  onPress,
}: NotificationCardProps) {
  // Determine priority level (0-100 scale)
  const getPriorityColor = (score: number) => {
    if (score >= 80) return "#DC2626"; // Red - High
    if (score >= 40) return "#EA580C"; // Orange - Medium
    return "#6B7280"; // Gray - Low
  };

  const getPriorityLabel = (score: number) => {
    if (score >= 80) return "High";
    if (score >= 40) return "Medium";
    return "Low";
  };

  const priorityColor = getPriorityColor(notification.priority_score);
  const priorityLabel = getPriorityLabel(notification.priority_score);

  return (
    <Pressable
      style={({ pressed }) => [styles.card, { opacity: pressed ? 0.7 : 1 }]}
      onPress={onPress}
    >
      <View style={styles.header}>
        <View style={styles.priorityBadge}>
          <View
            style={[styles.priorityDot, { backgroundColor: priorityColor }]}
          />
          <Text style={styles.priorityLabel}>{priorityLabel}</Text>
        </View>
        <Text style={styles.source}>{notification.source}</Text>
      </View>

      <Text style={styles.title} numberOfLines={2}>
        {notification.title}
      </Text>

      <Text style={styles.body} numberOfLines={3}>
        {notification.summary || notification.body}
      </Text>

      <Text style={styles.timestamp}>
        {new Date(notification.created_at).toLocaleString()}
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
    borderLeftColor: "#3B82F6",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  priorityBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
  },
  priorityDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  priorityLabel: {
    fontSize: 12,
    fontWeight: "600",
    color: "#374151",
  },
  source: {
    fontSize: 12,
    color: "#6B7280",
    fontWeight: "500",
    textTransform: "capitalize",
  },
  title: {
    fontSize: 16,
    fontWeight: "600",
    color: "#1F2937",
    marginBottom: 8,
  },
  body: {
    fontSize: 14,
    color: "#4B5563",
    lineHeight: 20,
    marginBottom: 8,
  },
  timestamp: {
    fontSize: 12,
    color: "#9CA3AF",
  },
});
