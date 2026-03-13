const BASE_URL = "http://localhost:8000";

export async function analyzeUnified(payload) {
  const res = await fetch(`${BASE_URL}/analyze/unified`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Unified analysis failed");
  }

  return res.json();
}

export async function analyzeBulk(payload) {
  const res = await fetch(`${BASE_URL}/analyze/bulk`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Bulk analysis failed");
  }

  return res.json();
}
