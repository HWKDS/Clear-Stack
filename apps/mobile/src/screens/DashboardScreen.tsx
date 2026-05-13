/**
 * Dashboard Screen
 * Main notification list view
 */
import React, { useEffect, useCallback } from "react";
import {
  View,
  StyleSheet,
  SafeAreaView,
  FlatList,
  Text,
  RefreshControl,
  Pressable,
} from "react-native";
import { useNotifications } from "@/hooks";
import { LoadingSpinner, ErrorMessage, NotificationCard } from "@/components";

export function DashboardScreen() {
  const {
    notifications,
    isLoading,
    error,
    refresh,
    unreadCount,
    highPriority,
    mediumPriority,
    lowPriority,
  } = useNotifications();

  // Fetch notifications on mount
  useEffect(() => {
    refresh();
  }, [refresh]);

  const handleRefresh = useCallback(() => {
    refresh();
  }, [refresh]);

  const renderHeader = () => (
    <View style={styles.header}>
      <Text style={styles.title}>Notifications</Text>
      <View style={styles.stats}>
        <StatBadge label="High" count={highPriority.length} color="#DC2626" />
        <StatBadge
          label="Medium"
          count={mediumPriority.length}
          color="#EA580C"
        />
        <StatBadge label="Low" count={lowPriority.length} color="#6B7280" />
      </View>
    </View>
  );

  if (isLoading && notifications.length === 0) {
    return <LoadingSpinner />;
  }

  if (error && notifications.length === 0) {
    return (
      <SafeAreaView style={styles.container}>
        {renderHeader()}
        <ErrorMessage message={error} onRetry={handleRefresh} />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={notifications}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.cardContainer}>
            <NotificationCard notification={item} />
          </View>
        )}
        ListHeaderComponent={renderHeader}
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Text style={styles.emptyStateIcon}>📭</Text>
            <Text style={styles.emptyStateTitle}>No Notifications</Text>
            <Text style={styles.emptyStateText}>
              All caught up! Check back later for new notifications.
            </Text>
          </View>
        }
        refreshControl={
          <RefreshControl
            refreshing={isLoading}
            onRefresh={handleRefresh}
            tintColor="#3B82F6"
          />
        }
        contentContainerStyle={styles.listContent}
      />
    </SafeAreaView>
  );
}

/**
 * Stat Badge Component
 */
function StatBadge({
  label,
  count,
  color,
}: {
  label: string;
  count: number;
  color: string;
}) {
  return (
    <View style={[styles.badge, { borderColor: color }]}>
      <Text style={[styles.badgeLabel, { color }]}>{label}</Text>
      <Text style={[styles.badgeCount, { color }]}>{count}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F9FAFB",
  },
  header: {
    backgroundColor: "#FFFFFF",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#E5E7EB",
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    color: "#1F2937",
    marginBottom: 16,
  },
  stats: {
    flexDirection: "row",
    gap: 8,
  },
  badge: {
    flex: 1,
    borderWidth: 2,
    borderRadius: 8,
    padding: 10,
    alignItems: "center",
  },
  badgeLabel: {
    fontSize: 12,
    fontWeight: "600",
  },
  badgeCount: {
    fontSize: 20,
    fontWeight: "700",
    marginTop: 4,
  },
  listContent: {
    padding: 16,
    paddingTop: 12,
  },
  cardContainer: {
    marginBottom: 8,
  },
  emptyState: {
    alignItems: "center",
    paddingVertical: 40,
  },
  emptyStateIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyStateTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#1F2937",
    marginBottom: 8,
  },
  emptyStateText: {
    fontSize: 14,
    color: "#6B7280",
    textAlign: "center",
  },
});
