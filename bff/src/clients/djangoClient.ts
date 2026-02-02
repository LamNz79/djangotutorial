const DJANGO_API = process.env.DJANGO_API!;

export async function djangoFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${DJANGO_API}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    }
  })
  if (!res.ok) {
    // Try to read response body safely
    const contentType = res.headers.get("content-type");
    const errorBody =
      contentType?.includes("application/json")
        ? await res.json()
        : await res.text();

    const error = new Error(
      `Django error ${res.status}: ${typeof errorBody === "string"
        ? errorBody
        : JSON.stringify(errorBody)
      }`
    );

    // Attach metadata (useful later)
    (error as any).status = res.status;
    (error as any).body = errorBody;

    throw error;
  }
  if (res.status === 204) {
    return undefined as T;
  }
  return res.json() as Promise<T>;
}