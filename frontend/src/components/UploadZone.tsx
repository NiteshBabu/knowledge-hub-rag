import { UploadCloud } from "lucide-react";
import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { useUploadDocument } from "../hooks/useUploadDocument";

export function UploadZone() {
  const uploadMutation = useUploadDocument();

  const onDrop = useCallback(
    async (files: File[]) => {

      if (!files.length) return

      try {
        await uploadMutation.mutateAsync(
          files[0]!,
        );
      }
      catch (e) {
        // console.log(e)
      }
    },
    [uploadMutation],
  );

  const {
    getRootProps,
    getInputProps,
  } = useDropzone({
    onDrop,
    accept: {
      // "application/pdf": [".pdf"],
    },
  });

  return (

    <div
      {...getRootProps()}
      className="group cursor-pointer rounded-2xl border-2 border-dashed  border-lime-300  p-10 text-center transition-all duration-200  hover:border-transparent  hover:bg-lime-500/50
  "
    >
      <input {...getInputProps()} />

      <div className="flex flex-col items-center gap-4">
        <div
          className="rounded-full  bg-lime-100 p-4 text-lime-600 transition-transform duration-200 group-hover:scale-110
      "
        >
          <UploadCloud size={32} />
        </div>

        <div>
          <h3 className="text-lg font-semibold text-white">
            Upload PDF
          </h3>

          <p className="mt-1 text-sm text-white/70">
            Drag & drop your PDF here or click to browse
          </p>
        </div>

        <div
          className="
        rounded-full
        bg-lime-100
        px-3
        py-1
        text-xs
        text-zinc-600
      "
        >
          PDF files only
        </div>
      </div>
    </div>
  );
}