import { useState } from 'react';
import { enviarPergunta } from '../services/api';

export const useChat = () => {
  const [mensagens, setMensagens] = useState([]);
  const [loading, setLoading] = useState(false);

  const enviar = async (texto) => {
    if (!texto.trim()) return;

    // Adiciona mensagem do usuário
    const novaMsgUsuario = {
      id: Date.now(),
      tipo: 'usuario',
      texto,
      timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
    };
    setMensagens((prev) => [...prev, novaMsgUsuario]);

    setLoading(true);
    try {
      const resposta = await enviarPergunta(texto);
      
      // Adiciona resposta do bot
      const novaMsgBot = {
        id: Date.now() + 1,
        tipo: 'bot',
        texto: resposta.resposta_texto,
        dados: {
          intent: resposta.intent,
          premissas: resposta.premissas,
          resultado: resposta.resultado,
        },
        timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
      };
      setMensagens((prev) => [...prev, novaMsgBot]);
    } catch (error) {
      const erroMsg = {
        id: Date.now() + 1,
        tipo: 'bot',
        texto: '⚠️ Erro ao processar a pergunta. Verifique se o backend está rodando.',
        timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
      };
      setMensagens((prev) => [...prev, erroMsg]);
    }
    setLoading(false);
  };

  return { mensagens, loading, enviar };
};
