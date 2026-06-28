import { useBackendHealth } from "@/hooks/useBackendHealth";
import { useEffect, useState } from "react";

const MESSAGES = [
  "Waking up the backend...",
  "Convincing the container to leave bed...",
  "Feeding the API some coffee...",
  "Stretching the database...",
  "Polishing the vectors...",
  "Teaching the PDFs new tricks...",
  "Untangling a few network cables...",
  "Checking if the server remembered its password...",
  "Loading an unreasonable amount of intelligence...",
  "Negotiating with the rate limiter...",
  "Indexing things we'll pretend were organized all along...",
  "Giving the cache a gentle nudge...",
  "Bribing the load balancer with compliments...",
  "Synchronizing the digital hamsters...",
  "Waiting for the cloud to find itself...",
  "Making sure the logs are sufficiently dramatic...",
  "Calibrating the AI's confidence levels...",
  "Running a quick reality check...",
  "Scanning for gremlins...",
  "Sharpening the embeddings...",
  "Converting caffeine into compute...",
  "Performing highly scientific button pressing...",
  "Double-checking the important bits...",
  "Preparing dashboards and shiny graphs...",
  "Summoning application state...",
  "Almost there...",
  "Ready to roll 🚀"
];

export function ColdBootScreen() {

  const { backendReady } = useBackendHealth()
  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    if (messageIndex >= MESSAGES.length - 1 || backendReady) return;

    const interval = setInterval(() => {
      setMessageIndex(i => i + 1);
    }, 3500);

    return () => clearInterval(interval);
  }, [messageIndex]);


  if (backendReady) return

  return (
    <div className="flex h-screen flex-col items-center justify-center gap-6 px-6 text-center absolute inset-0 bg-black/30 z-10 font-mono">
      <div className="flex h-1/2 flex-col items-center justify-center gap-6 px-6 text-center backdrop-blur-xl z-10 md:w-1/2 mx-auto rounded-2xl">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-lime-300 border-t-black" />

        <h1 className="text-2xl font-semibold text-lime-500">
          Starting Backend
        </h1>

        <p className="max-w-md text-lime-500">
          {MESSAGES[messageIndex]}
        </p>

        <div className="w-full max-w-xs overflow-hidden rounded-full bg-lime-100">
          <div
            className="h-2 bg-lime-500"
            style={{
              animation:
                "coldBootProgress 90s linear forwards",
            }}
          />
        </div>

        <p className="text-sm text-lime-400">
          ❄️ Cold boot in progress.
          <br />
          This FastAPI backend is hosted on a free-tier service and may take up to a minute to spin up.
        </p>
      </div>
    </div>
  );
}