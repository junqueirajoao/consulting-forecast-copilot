import { useState } from 'react';

export const InputBar = ({ onEnviar, loading }) => {
  const [texto, setTexto] = useState('');
  const [focused, setFocused] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (texto.trim() && !loading) { onEnviar(texto); setTexto(''); }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(e); }
  };

  const canSend = texto.trim() && !loading;

  return (
    <div style={{
      backgroundColor: '#ffffff',
      borderTop: '1px solid #e0e0e0',
      padding: '12px 16px 14px',
      flexShrink: 0,
    }}>
      <form onSubmit={handleSubmit}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          border: '2px solid #e0e0e0',
          borderRadius: '999px',
          backgroundColor: '#f4f4f4',
          padding: '4px 4px 4px 16px',
          transition: 'border-color 0.15s ease',
        }}>
          <input
            type="text"
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            placeholder="Digite sua pergunta sobre faturamento..."
            disabled={loading}
            style={{
              flex: 1,
              backgroundColor: 'transparent',
              border: 'none',
              outline: 'none',
              padding: '7px 0',
              fontSize: '14px',
              color: '#161616',
              fontFamily: "'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif",
              letterSpacing: '0.16px',
              caretColor: '#0f62fe',
            }}
          />
          <button
            type="submit"
            disabled={!canSend}
            style={{
              backgroundColor: canSend ? '#0f62fe' : '#e0e0e0',
              border: 'none',
              outline: 'none',
              padding: '8px 18px',
              borderRadius: '999px',
              color: canSend ? '#ffffff' : '#a8a8a8',
              fontSize: '14px',
              fontWeight: '600',
              fontFamily: "'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif",
              letterSpacing: '0.16px',
              cursor: canSend ? 'pointer' : 'not-allowed',
              transition: 'background-color 0.15s ease, color 0.15s ease, transform 0.1s ease',
              display: 'flex', alignItems: 'center', gap: '7px',
              flexShrink: 0,
            }}
            onMouseDown={(e) => canSend && (e.currentTarget.style.transform = 'scale(0.96)')}
            onMouseUp={(e) => (e.currentTarget.style.transform = 'scale(1)')}
          >
            {loading ? (
              <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: '12px' }}>...</span>
            ) : (
              <>
                Enviar
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                  <path d="M2 8H14M9 3L14 8L9 13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="square"/>
                </svg>
              </>
            )}
          </button>
        </div>
        <p style={{
          fontSize: '11px',
          color: '#a8a8a8',
          marginTop: '5px',
          letterSpacing: '0.32px',
          paddingLeft: '2px',
          fontFamily: "'IBM Plex Sans', sans-serif",
        }}>
          Pressione Enter para enviar
        </p>
      </form>
    </div>
  );
};
