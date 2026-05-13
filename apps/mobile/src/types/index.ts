/**
 * Core type definitions for PulseHub Mobile
 * Matches the FastAPI backend response models
 */

// Authentication & API Keys
export interface APIKey {
  id: string;
  name: string;
  is_active: boolean;
  created_at: string;
  last_used_at: string | null;
  expires_at: string | null;
}

export interface APIKeyCreateResponse {
  id: string;
  key: string; // Only shown once
  name: string;
  created_at: string;
}

// Notifications
export interface Notification {
  id: string;
  source: string; // "gmail", "calendar", "whatsapp", "linkedin"
  title: string;
  body: string;
  summary?: string;
  priority_score: number; // 0-100
  meta: Record<string, any>;
  created_at: string;
}

export interface NotificationListFilters {
  source?: string;
  priority_min?: number;
  priority_max?: number;
  limit?: number;
  offset?: number;
}

// Digest
export interface Digest {
  id: string;
  summary: string;
  notifications: Notification[];
  generated_at: string;
}

// API Responses
export interface APIResponse<T> {
  data: T | null;
  error: string | null;
  message: string;
}

// Auth Store
export interface AuthState {
  apiKey: string | null;
  isAuthenticated: boolean;
  setApiKey: (key: string) => Promise<void>;
  getApiKey: () => Promise<string | null>;
  clearApiKey: () => Promise<void>;
}

// Notification Store
export interface NotificationState {
  notifications: Notification[];
  isLoading: boolean;
  error: string | null;
  fetchNotifications: (filters?: NotificationListFilters) => Promise<void>;
  setError: (error: string | null) => void;
}
