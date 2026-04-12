<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Client — Build Guide

## Stack
- **Framework**: Next.js (App Router), React
- **Styling / UI**: Tailwind CSS v4 + [shadcn/ui](https://ui.shadcn.com/)
- **State management**: Zustand
- **Server state / data fetching**: TanStack Query (React Query) + Axios

## Running the dev server
```bash
npm run dev
```

## Source layout

```
src/
  app/           # Next.js App Router — pages, layouts, loading & error boundaries
  components/
    ui/          # shadcn auto-generated components (never edit by hand)
  hooks/         # TanStack Query hooks, one file per API resource
  lib/
    axios.ts     # Axios instance — base URL, auth interceptor, error normalisation
    query-client.ts  # TanStack QueryClient singleton
    utils.ts     # shadcn cn() helper
  providers/
    query-provider.tsx  # QueryClientProvider + ReactQueryDevtools (client component)
  store/         # Zustand stores, one file per domain slice
  types/         # Shared TypeScript types
```

## Adding a shadcn component

```bash
npx shadcn@latest add <component>
```

This generates a file under `src/components/ui/`. Do not edit those files directly — override at the usage site via `className`.

## API layer — Axios

`src/lib/axios.ts` exports a pre-configured `apiClient` instance:
- `baseURL` reads from `NEXT_PUBLIC_API_URL` (falls back to `http://localhost:8000`)
- Attaches a `Bearer` token from `localStorage` on every request
- Normalises error messages so you only need to catch `Error`, not `AxiosError`

```ts
import { apiClient } from "@/lib/axios";

const { data } = await apiClient.get<MyType>("/api/v1/resource");
```

## Server state — TanStack Query

Wrap all API calls in a custom hook inside `src/hooks/`. Naming convention: `use<Resource>`.

```ts
// src/hooks/use-widgets.ts
export function useWidgets() {
  return useQuery<Widget[]>({
    queryKey: ["widgets"],
    queryFn: async () => {
      const { data } = await apiClient.get<Widget[]>("/api/v1/widgets");
      return data;
    },
  });
}
```

Query keys follow `[resource, ...params]` so cache invalidation stays predictable.

## Client state — Zustand

Add a store in `src/store/<feature>.store.ts`. Naming convention: `use<Feature>Store`.

```ts
// src/store/auth.store.ts
interface AuthState {
  token: string | null;
  setToken: (token: string) => void;
  clearToken: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  setToken: (token) => set({ token }),
  clearToken: () => set({ token: null }),
}));
```

Keep stores small and single-purpose. Derive computed values with selectors rather than storing derived state.

## Environment variables

Copy `.env.local.example` to `.env.local` and fill in values. Only variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

## Dependency management

```bash
npm install <package>          # add a runtime dependency
npm install -D <package>       # add a dev dependency
npm uninstall <package>        # remove a dependency
```
