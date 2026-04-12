import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/axios";

// ---------------------------------------------------------------------------
// Types — mirror your API response shapes here or import from src/types/
// ---------------------------------------------------------------------------

interface HealthStatus {
  status: string;
}

// ---------------------------------------------------------------------------
// Query hook
// ---------------------------------------------------------------------------

// Naming convention: use<Resource> — one file per API resource.
// Query keys follow [resource, ...params] so invalidation stays predictable.

export function useHealth() {
  return useQuery<HealthStatus>({
    queryKey: ["health"],
    queryFn: async () => {
      const { data } = await apiClient.get<HealthStatus>("/api/v1/health");
      return data;
    },
  });
}
