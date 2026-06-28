import { useMutation, useQueryClient } from "@tanstack/react-query";

import { getErrorMessage } from "@/lib/utils";
import { api } from "../api/client";

export function useUploadDocument() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (
      file: File,
    ) => {
      const formData =
        new FormData();

      formData.append(
        "file",
        file,
      );

      const response =
        await api.post(
          "/documents/upload",
          formData
        );

      return response.data;
    },

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: [
          "documents",
        ],
      });
    },

    onError: (error) => {
      alert(getErrorMessage(error))
      return
    }
  });
}