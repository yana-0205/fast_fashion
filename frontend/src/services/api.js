const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";
export const MEDIA_BASE = API_BASE.replace(/\/api\/?$/, "");

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.error?.message || `Request failed with status ${response.status}`);
  }
  return payload;
}

export const api = {
  options: () => request("/options/"),
  dashboard: () => request("/dashboard/"),
  marketTrends: () => request("/market-trends/"),
  listDesigns: () => request("/designs/"),
  getDesign: (id) => request(`/designs/${id}/`),
  deleteDesign: (id) => request(`/designs/${id}/`, { method: "DELETE" }),
  generateDesign: (values) => request("/designs/generate/", { method: "POST", body: JSON.stringify(values) }),
  forecastDesign: (id) => request(`/designs/${id}/forecast/`, { method: "POST", body: "{}" }),
  insightDesign: (id) => request(`/designs/${id}/insights/`, { method: "POST", body: "{}" }),
  compareDesigns: (ids) => request("/designs/compare/", { method: "POST", body: JSON.stringify({ design_ids: ids }) }),
};

export function imageUrl(path) {
  if (!path) return "";
  return path.startsWith("http") ? path : `${MEDIA_BASE}${path}`;
}
