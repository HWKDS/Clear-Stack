/**
 * useNotifications Hook
 * Provides notifications state and fetch methods
 */
import { useCallback } from "react";
import { notificationStore } from "@/store/notifications";
import type { NotificationListFilters } from "@/types";

export function useNotifications() {
  const notifications = notificationStore((store) => store.notifications);
  const isLoading = notificationStore((store) => store.isLoading);
  const error = notificationStore((store) => store.error);
  const fetchNotifications = notificationStore(
    (store) => store.fetchNotifications,
  );
  const setError = notificationStore((store) => store.setError);

  const refresh = useCallback(
    (filters?: NotificationListFilters) => fetchNotifications(filters),
    [fetchNotifications],
  );

  return {
    // State
    notifications,
    isLoading,
    error,

    // Methods
    refresh,
    setError,
    fetchNotifications,

    // Computed
    unreadCount: notifications.length,
    highPriority: notifications.filter((n) => n.priority_score >= 80),
    mediumPriority: notifications.filter(
      (n) => n.priority_score >= 40 && n.priority_score < 80,
    ),
    lowPriority: notifications.filter((n) => n.priority_score < 40),
  };
}
