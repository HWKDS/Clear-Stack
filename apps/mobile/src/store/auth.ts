/**
 * Authentication Store (Zustand)
 * Manages API key storage and retrieval with secure storage
 */
import { create } from "zustand";
import * as SecureStore from "expo-secure-store";
import type { AuthState } from "@/types";
import { STORAGE_KEYS } from "@/lib/config";

/**
 * Create auth store with secure storage backing
 * This uses expo-secure-store to encrypt sensitive data on device
 */
export const authStore = create<AuthState>((set) => ({
  apiKey: null,
  isAuthenticated: false,

  /**
   * Set API key - saves to secure storage
   */
  setApiKey: async (key: string) => {
    try {
      // Validate key format before storing
      if (!key || key.length < 10) {
        throw new Error("Invalid API key format");
      }

      // Store securely
      await SecureStore.setItemAsync(STORAGE_KEYS.apiKey, key);

      // Update state
      set({
        apiKey: key,
        isAuthenticated: true,
      });
    } catch (error) {
      console.error("Failed to set API key:", error);
      throw error;
    }
  },

  /**
   * Get API key from secure storage
   */
  getApiKey: async () => {
    try {
      const key = await SecureStore.getItemAsync(STORAGE_KEYS.apiKey);
      if (key) {
        set({ apiKey: key, isAuthenticated: true });
      }
      return key || null;
    } catch (error) {
      console.error("Failed to get API key:", error);
      return null;
    }
  },

  /**
   * Clear API key and logout
   */
  clearApiKey: async () => {
    try {
      await SecureStore.deleteItemAsync(STORAGE_KEYS.apiKey);
      await SecureStore.deleteItemAsync(STORAGE_KEYS.userId);
      set({
        apiKey: null,
        isAuthenticated: false,
      });
    } catch (error) {
      console.error("Failed to clear API key:", error);
      throw error;
    }
  },
}));
