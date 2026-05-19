import { useState } from 'react';
import { useChat } from './hooks/useChat';
import { ChatWindow } from './components/ChatWindow';
import { InputBar } from './components/InputBar';
import { UploadBar } from './components/UploadBar';
import { DataTable } from './components/DataTable';
import logoCfp from './assets/logo-cfp.png';
import iconChat from './assets/icon-chat.png';
import iconDados from './assets/icon-dados.png';
import './App.css';

function App() {
  const { mensagens, loading, enviar } = useChat();
  const [abaAtiva, setAbaAtiva] = useState('chat');

  const tabStyle = (aba) => ({
    padding: '10px 20px',
    border: 'none',
    borderBottom: abaAtiva === aba ? '2px solid #0f62fe' : '2px solid transparent',
    backgroundColor: 'transparent',
    color: abaAtiva === aba ? '#0f62fe' : '#525252',
    fontSize: '14px',
    fontWeight: abaAtiva === aba ? '500' : '400',
    cursor: 'pointer',
    fontFamily: "'IBM Plex Sans', sans-serif",
    transition: 'all 0.15s',

  });

  return (
    <div style={{
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      backgroundColor: '#ffffff',
      fontFamily: "'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif",
    }}>

      {/* Header */}
      <header style={{
        backgroundColor: '#ffffff',
        borderBottom: '1px solid #e0e0e0',
        padding: '0 1rem',
        height: '48px',
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
        flexShrink: 0,
      }}>
        <img
          src={logoCfp}
          alt="CFP Logo"
          style={{ height: '36px', width: 'auto', objectFit: 'contain' }}
        />
        <div style={{ width: '1px', height: '20px', backgroundColor: '#e0e0e0' }} />
        <span style={{ color: '#161616', fontSize: '14px', fontWeight: '500', letterSpacing: '0.16px' }}>
          Consulting Forecast Copilot
        </span>
        <span style={{
          marginLeft: 'auto',
          fontSize: '11px',
          color: '#0f62fe',
          fontFamily: "'IBM Plex Mono', monospace",
          letterSpacing: '0.32px',
          fontWeight: '500',
        }}>
          AI
        </span>
      </header>

      {/* Barra de abas + upload */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        borderBottom: '2px solid #0f62fe',
        backgroundColor: '#ffffff',
        padding: '0 16px',
        flexShrink: 0,
      }}>
        <button className="tab-btn" style={tabStyle('chat')} onClick={() => setAbaAtiva('chat')}>
          <img src={iconChat} alt="" style={{ height: '16px', width: 'auto', objectFit: 'contain', verticalAlign: 'middle', marginRight: '6px' }} />
          Chat
        </button>
        <button className="tab-btn" style={tabStyle('dados')} onClick={() => setAbaAtiva('dados')}>
          <img src={iconDados} alt="" style={{ height: '16px', width: 'auto', objectFit: 'contain', verticalAlign: 'middle', marginRight: '6px' }} />
          Dados
        </button>
        <div style={{ marginLeft: 'auto' }}>
          <UploadBar />
        </div>
      </div>

      {/* Conteúdo */}
      {abaAtiva === 'chat' ? (
        <>
          <ChatWindow mensagens={mensagens} loading={loading} />
          <InputBar onEnviar={enviar} loading={loading} />
        </>
      ) : (
        <DataTable />
      )}

    </div>
  );
}

export default App;
