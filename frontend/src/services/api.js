import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const enviarPergunta = async (pergunta, mesReferencia = null) => {
  const response = await axios.post(`${API_URL}/query`, {
    pergunta,
    mes_referencia: mesReferencia,
  });
  return response.data;
};
