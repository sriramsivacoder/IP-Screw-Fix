const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export async function classifyFormulation(answers) {
  const response = await fetch(`${BASE_URL}/api/classify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answers }),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(
      error.detail || `Classification failed: ${response.statusText}`
    )
  }
  return response.json()
}

export async function sendChatMessage(question, jurisdiction, classification, iprRoutes) {
  const response = await fetch(`${BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      jurisdiction,
      classification,
      ipr_routes: iprRoutes,
    }),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(
      error.detail || `Chat request failed: ${response.statusText}`
    )
  }
  return response.json()
}
