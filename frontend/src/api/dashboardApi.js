const BASE_URL = "http://localhost:8000";

export async function fetchDashboardStats() {
  const response = await fetch(`${BASE_URL}/stats/dashboard`);

  if (!response.ok) {
    throw new Error("Failed to fetch dashboard stats");
  }

  return response.json();
}
