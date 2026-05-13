/**
 * Notifications Store (Zustand)
 * Manages notification state and fetching
 */
import { create } from "zustand";
import { notificationAPI } from "@/lib/api";
import type {
  Notification,
  NotificationListFilters,
  NotificationState,
} from "@/types";

export const notificationStore = create<NotificationState>((set) => ({
  notifications: [],
  isLoading: false,
  error: null,

  /**
   * Fetch notifications from API
   */
  fetchNotifications: async (filters?: NotificationListFilters) => {
    set({ isLoading: true, error: null });

    try {
      const response = await notificationAPI.listNotifications(filters);

      if (response.error) {
        set({ error: response.error, notifications: [] });
        return;
      }

      const notifications = Array.isArray(response.data) ? response.data : [];
      set({ notifications, error: null });
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Failed to fetch notifications";
      set({ error: errorMessage, notifications: [] });
    } finally {
      set({ isLoading: false });
    }
  },

  /**
   * Set error state
   */
  setError: (error: string | null) => {
    set({ error });
  },
}));
