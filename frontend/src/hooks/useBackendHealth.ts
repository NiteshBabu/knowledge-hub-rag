import { api } from "@/api/client";
import { useQuery } from "@tanstack/react-query";

export function useBackendHealth() {
  const query = useQuery({
    queryKey: ["health"],
    queryFn: () => api.get("/health"),
    retry: Infinity,
    retryDelay: 5000,
    networkMode: "always",
  });

  return {
    backendReady: query.isSuccess,
    showColdBoot:
      !query.isSuccess &&
      query.failureCount >= 2,
  };
}