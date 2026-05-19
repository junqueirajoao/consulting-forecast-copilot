import { useEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';
import logoCfp from '../assets/logo-cfp.png';

export const ChatWindow = ({ mensagens, loading }) => {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [mensagens]);

  return (
    <div style={{
      flex: 1,
      overflowY: 'auto',
      backgroundColor: '#ffffff',
      padding: '24px 16px',
      display: 'flex',
      flexDirection: 'column',
    }}>
      {mensagens.length === 0 && (
        <div style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '12px',
          color: '#a8a8a8',
        }}>
          <img src={logoCfp} alt="CFP" style={{ height: '28px', width: 'auto', objectFit: 'contain', opacity: 0.85 }} />
          <p style={{ fontSize: '14px', color: '#525252', letterSpacing: '0.16px' }}>
            Faça uma pergunta para começar
          </p>
          <p style={{ fontSize: '12px', color: '#a8a8a8', letterSpacing: '0.32px' }}>
            Pergunte sobre faturamento, times e consultores
          </p>
        </div>
      )}

      {mensagens.map((msg) => (
        <MessageBubble key={msg.id} mensagem={msg} />
      ))}

      {loading && (
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', marginTop: '8px' }}>
          <div style={{
            width: '24px', height: '24px',
            backgroundColor: '#0f62fe',
            borderRadius: '2px',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexShrink: 0,
          }}>
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
              <path d="M4 9L6 3L8 9" stroke="white" strokeWidth="1.2" strokeLinecap="square"/>
              <path d="M4.5 7.5H7.5" stroke="white" strokeWidth="1.2" strokeLinecap="square"/>
            </svg>
          </div>
          <div style={{
            backgroundColor: '#f4f4f4',
            border: '1px solid #e0e0e0',
            borderRadius: '2px',
            padding: '10px 14px',
            display: 'flex', gap: '5px', alignItems: 'center',
          }}>
            {[0, 1, 2].map((i) => (
              <div key={i} style={{
                width: '6px', height: '6px',
                backgroundColor: '#0f62fe',
                borderRadius: '50%',
                animation: `pulse 1.4s ease-in-out ${i * 0.2}s infinite`,
              }} />
            ))}
          </div>
        </div>
      )}

      <style>{`
        @keyframes pulse {
          0%, 80%, 100% { opacity: 0.25; transform: scale(0.8); }
          40% { opacity: 1; transform: scale(1); }
        }
      `}</style>

      <div ref={endRef} />
    </div>
  );
};
