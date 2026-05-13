/**
 * API-based login hook
 * Handles API key generation and login flow
 */
import { useState } from "react";
import { authAPI } from "@/lib/api";
import { authStore } from "@/store/auth";

export function useLogin() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const setApiKey = authStore((store) => store.setApiKey);

  const login = async (name: string = "Mobile App Key") => {
    setIsLoading(true);
    setError(null);

    try {
      // Call backend to create API key
      // Note: In dev mode, this works without authentication
      const response = await authAPI.createApiKey(name);

      if (response.error) {
        throw new Error(response.error);
      }

      if (!response.data || !("key" in response.data)) {
        throw new Error("Invalid response from server");
      }

      // Store the API key securely
      await setApiKey(response.data.key);

      return response.data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Login failed";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    login,
    isLoading,
    error,
    setError,
  };
}
