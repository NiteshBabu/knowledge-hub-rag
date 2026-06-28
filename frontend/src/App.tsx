import { BookOpenIcon, Sparkles } from "lucide-react";
import { ChatBox } from "./components/ChatBox";
import { ColdBootScreen } from "./components/ColdBootScreen";
import { DocumentList } from "./components/DocumentList";
import { UploadZone } from "./components/UploadZone";
import { useBackendHealth } from "./hooks/useBackendHealth";
import "./index.css";

export function App() {

  const { backendReady } = useBackendHealth()


  return (
    <>
      <ColdBootScreen />
      <div className="flex gap-4 items-center mb-5">
        <div className="logo relative">
          <BookOpenIcon className="w-10 h-10 md:w-14 md:h-14 stroke-lime-500" />
          <Sparkles className="absolute top-0 left-0 text-yellow-300 animate-pulse" />
        </div>
        <div className="grid">

          <h1 className="text-2xl md:text-4xl text-lime-500 font-bold">
            KnowledgeHub
          </h1>
          <small className="font-bold">RAG powered document assistant built with
            React, FastAPI, PostgreSQL/pgvector, Sentence Transformer & Groq
          </small>
        </div>
      </div>
      <main className="font-mono" inert={!backendReady} >
        <div
          className="grid md:grid-cols-[600px_400px] gap-4"
        >
          <ChatBox />
          <div >
            <UploadZone />
            <DocumentList />
          </div>
        </div>
      </main>
      <footer className="mt-2 flex justify-between items-center">
        <p>&copy;NiteshBabu {new Date().getFullYear()}</p>
        <p>Made with
          <span className="text-red-500 text-xl mx-2">
            &hearts;
          </span>
          by {'</NiteshBabu>'}</p>
      </footer>
    </>
  );
}

export default App;