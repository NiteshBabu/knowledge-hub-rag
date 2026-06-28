import { getSessionId } from "@/lib/utils";
import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NODE_ENV != "production" ? "http://localhost:8000" : "https://knowledge-hub-rag.onrender.com/",
});

api.interceptors.request.use(
  (config) => {
    config.headers[
      "X-Session-Id"
    ] = getSessionId();
    return config;
  },
);