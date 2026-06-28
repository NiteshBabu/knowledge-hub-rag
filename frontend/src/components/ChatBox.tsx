import {
  useEffect,
  useRef,
  useState,
} from "react";

import { api } from "../api/client";

import { useDocuments } from "@/hooks/useDocuments";
import { getErrorMessage } from "@/lib/utils";
import type {
  ChatMessage
} from "../types/chat";

export function ChatBox() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { data } = useDocuments()

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const askQuestion = async () => {
    const trimmed =
      question.trim();

    if (!trimmed || loading)
      return;

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: trimmed,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    setQuestion("");

    try {
      setLoading(true);

      const response =
        await api.post("/chat", {
          question: trimmed,
        });

      const assistantMessage: ChatMessage =
      {
        id: crypto.randomUUID(),
        role: "assistant",
        content:
          response.data.answer,
        sources:
          response.data.sources,
      };

      setMessages((prev) => [
        ...prev,
        assistantMessage,
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: getErrorMessage(error)
        },
      ]);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className={`flex flex-col gap-4 rounded-2xl border border-lime-500 h-[calc(100vh-130px)] min-w-85 ${!data?.length && "opacity-50 pointer-events-none"}`}>
      <div className="p-4 overflow-y-auto flex-1">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`mb-4 flex ${message.role === "user"
              ? "justify-end"
              : "justify-start"
              }`}
          >
            <div
              className={`max-w-[75%] rounded-xl px-4 py-2 ${message.role === "user"
                ? "bg-lime-600 text-white"
                : "bg-zinc-100 text-zinc-900"
                }`}
            >
              <div>{message.content}</div>

              {/* {message.sources?.length ? (
                <div className="mt-4 border-t border-zinc-300 pt-3">
                  <p className="mb-2 text-sm font-semibold">
                    Sources
                  </p>

                  {message.sources.map(
                    (source: Source) => (
                      <div
                        key={source.chunk_id}
                        className="mb-2 rounded-md bg-white/50 p-2 text-xs"
                      >
                        <div className="font-medium">
                          Chunk #{source.chunk_id}
                        </div>

                        <div className="mt-1">
                          {source.content}
                        </div>
                      </div>
                    ),
                  )}
                </div>
              ) : null} */}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="rounded-xl bg-zinc-100 px-4 py-3 text-zinc-500">
              Thinking...
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="border-t border-zinc-200 p-4">
        <textarea
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          // disabled={!data?.length || !data?.some(d => d.status === "INDEXED")}
          rows={3}
          placeholder={getChatPlaceholder(data)}
          className="w-full resize-none rounded-lg border border-zinc-300 p-3 outline-none focus:border-lime-500 focus:ring-2 focus:ring-lime-500 disabled:opacity-50"
          onKeyDown={(e) => {
            if (
              e.key === "Enter" &&
              !e.shiftKey
            ) {
              e.preventDefault();
              askQuestion();
            }
          }}
        />

        <button
          onClick={askQuestion}
          disabled={
            loading ||
            question.trim().length === 0 || !data?.length
          }
          className="mt-3 rounded-lg bg-lime-600 px-4 py-2 text-white transition hover:bg-lime-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div >
  );
}

function getChatPlaceholder(
  documents?: Document[],
) {
  if (!documents?.length) {
    return "Please upload a PDF file to start chatting...";
  }

  if (
    documents.some(
      (d) => d.status === "UPLOADED",
    )
  ) {
    return "Document uploaded...";
  }

  if (
    documents.some(
      (d) => d.status === "PROCESSING",
    )
  ) {
    return "Please wait while the document is processed...";
  }

  if (
    documents.some(
      (d) => d.status === "INDEXED",
    )
  ) {
    return "Let's go, shoot a question...";
  }

  return "Please upload a PDF file to start chatting...";
}