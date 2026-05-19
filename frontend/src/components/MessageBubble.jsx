import logoCfp from '../assets/logo-cfp.png';

export const MessageBubble = ({ mensagem }) => {
  const isUsuario = mensagem.tipo === 'usuario';

  return (
    <div style={{
      display: 'flex',
      alignItems: 'flex-start',
      gap: '8px',
      marginBottom: '16px',
      flexDirection: isUsuario ? 'row-reverse' : 'row',
    }}>
      {/* Avatar */}
      <div style={{
        width: '36px', height: '36px',
        backgroundColor: isUsuario ? '#0f62fe' : '#ffffff',
        border: isUsuario ? '1.5px solid #0f62fe' : '1.5px solid #0f62fe',
        borderRadius: '8px',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
        marginTop: '2px',
      }}>
        {isUsuario ? (
          <svg width="14" height="14" viewBox="0 0 12 12" fill="none">
            <circle cx="6" cy="4" r="2.5" stroke="white" strokeWidth="1.2"/>
            <path d="M1.5 11c0-2.485 2.015-4.5 4.5-4.5s4.5 2.015 4.5 4.5" stroke="white" strokeWidth="1.2" strokeLinecap="square"/>
          </svg>
        ) : (
          <img src={logoCfp} alt="CFP" style={{ width: '22px', height: '22px', objectFit: 'contain' }} />
        )}
      </div>

      {/* Bubble */}
      <div style={{ maxWidth: '72%' }}>
        <div style={{
          backgroundColor: isUsuario ? '#f4f4f4' : '#ffffff',
          border: `1px solid ${isUsuario ? '#e0e0e0' : '#e0e0e0'}`,
          borderLeft: isUsuario ? '1px solid #e0e0e0' : '2px solid #0f62fe',
          borderRadius: '2px',
          padding: '10px 14px',
        }}>
          <p style={{
            fontSize: '14px',
            color: '#161616',
            lineHeight: '1.6',
            letterSpacing: '0.16px',
            whiteSpace: 'pre-wrap',
            margin: 0,
            fontFamily: "'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif",
          }}>
            {mensagem.texto}
          </p>
        </div>
        {mensagem.timestamp && (
          <p style={{
            fontSize: '11px',
            color: '#a8a8a8',
            marginTop: '4px',
            letterSpacing: '0.32px',
            textAlign: isUsuario ? 'right' : 'left',
            fontFamily: "'IBM Plex Mono', monospace",
          }}>
            {mensagem.timestamp}
          </p>
        )}
      </div>
    </div>
  );
};
