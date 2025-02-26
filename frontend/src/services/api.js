const API_URL = "http://127.0.0.1:8000/api";

export const fetchMessage = async () => {
  const response = await fetch(`${API_URL}/hello`);
  return response.json();
};
