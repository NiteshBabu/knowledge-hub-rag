export function getSessionId() {
  let sessionId =
    localStorage.getItem(
      "session_id",
    );

  if (!sessionId) {
    sessionId =
      crypto.randomUUID();

    localStorage.setItem(
      "session_id",
      sessionId,
    );
  }

  return sessionId;
}


import axios from "axios";

export function getErrorMessage(
  error: unknown,
) {
  if (
    axios.isAxiosError(error)
  ) {
    return (
      error.response?.data
        ?.detail
      ?? error.response?.data
        ?.error

      ?? error.message
    );
  }

  return "Something went wrong";
}