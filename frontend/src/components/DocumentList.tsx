import { FileText, LoaderCircleIcon } from "lucide-react";
import { useDocuments } from "../hooks/useDocuments";
export function DocumentList() {
  const { data, isLoading } = useDocuments();

  if (isLoading) {
    return;
  }


  return (
    <div className="border-2 rounded-2xl border-dashed border-lime-3  00 min-h-[200px] my-5 p-2">
      <h2 className="text-xl text-center">My Documents</h2>
      {
        isLoading ? <LoaderCircleIcon className="animate-spin m-auto mt-10" />
          : data?.length > 0 ?
            <ul className="grid gap-2 mt-10">
              {data?.map((doc: any) => (
                <li key={doc.id} className="flex justify-between">
                  <div className="flex gap-2">

                    <FileText />
                    <strong className="truncate md:w-[30ch]">
                      {doc.name}
                    </strong>
                  </div>
                  <DocumentStatusPill status={doc.status} />
                </li>
              ))}
            </ul>
            :
            <small className="text-center mt-[25%] rounded-full bg-lime-100 text-zinc-500 w-fit mx-auto px-4 block">Nothing to show here</small>
      }
    </div>
  );
}

const DocumentStatusPill = ({ status }) => {
  switch (status) {
    case "FAILED":
      return <small className="bg-red-500 text-white rounded-full px-2 py-1 text-xs">{status}</small>
    case "PROCESSING":
      return <small className="bg-orange-500 text-white rounded-full px-2 py-1 text-xs">{status}</small>
    case "UPLOADED":
      return <small className="bg-yellow-500 text-white rounded-full px-2 py-1 text-xs">{status}</small>
    case "INDEXED":
      return <small className="bg-green-500 text-white rounded-full px-2 py-1 text-xs">{status}</small>
  }
}