import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

export const RootProviders = ({ children }: { children: React.ReactNode }) => {
  return <QueryClientProvider client={queryClient} >
    {children}
  </QueryClientProvider>
}