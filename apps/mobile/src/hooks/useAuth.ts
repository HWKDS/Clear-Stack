/**
 * useAuth Hook
 * Provides authentication state and methods for easy access in components
 */
import { useEffect, useState } from "react";
import { authStore } from "@/store/auth";
import type { AuthState } from "@/types";

export function useAuth() {
  const [state, setState] = useState<{
    isAuthenticated: boolean;
    isLoading: boolean;
  }>({
    isAuthenticated: false,
    isLoading: true,
  });

  const apiKey = authStore((store) => store.apiKey);
  const isAuthenticated = authStore((store) => store.isAuthenticated);
  const setApiKey = authStore((store) => store.setApiKey);
  const getApiKey = authStore((store) => store.getApiKey);
  const clearApiKey = authStore((store) => store.clearApiKey);

  // Initialize auth state on mount
  useEffect(() => {
    const initAuth = async () => {
      const key = await getApiKey();
      setState({
        isAuthenticated: !!key,
        isLoading: false,
      });
    };

    initAuth();
  }, [getApiKey]);

  return {
    // State
    isAuthenticated: state.isAuthenticated || isAuthenticated,
    isLoading: state.isLoading,
    apiKey,

    // Methods
    setApiKey,
    clearApiKey,
    getApiKey,

    // Convenience
    login: setApiKey,
    logout: clearApiKey,
  };
}
