import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";

export function useDocuments() {
  return useQuery({
    queryKey: ["documents"],
    queryFn: async () => {
      const response = await api.get("/documents/");
      return response.data;
    },

    refetchInterval: (query) => {
      const documents = query.state.data

      const hasProcessing = documents?.some(doc => doc.status === "PROCESSING" || doc.status === "UPLOADED")

      return hasProcessing ? 3000 : false
    },
  });
} 