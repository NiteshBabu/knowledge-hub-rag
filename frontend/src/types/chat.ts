export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}

export interface Source {
  chunk_id: number;
  content: string;
}