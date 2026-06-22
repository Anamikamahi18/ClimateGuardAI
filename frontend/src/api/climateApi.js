import axios from "axios";

const API_URL =
  import.meta.env.VITE_API_URL;

export const getCompleteAnalysis =
  async (city) => {

    const response =
      await axios.post(
        `${API_URL}/analysis/complete`,
        {
          city,
        }
      );

    return response.data;
  };
