import { useRef, useState } from 'react';

export const UploadBar = ({ onUploadSuccess }) => {
  const inputRef = useRef(null);
  const [status, setStatus] = useState(null);
  const [fileName, setFileName] = useState(null);
  const [dragging, setDragging] = useState(false);

  const handleFile = async (file) => {
    if (!file) return;
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
      setStatus('error');
      setFileName('Formato inválido — use .xlsx');
      return;
    }
    setFileName(file.name);
    setStatus('loading');
    const form = new FormData();
    form.append('file', file);
    try {
      const res = await fetch('http://127.0.0.1:8000/upload', { method: 'POST', body: form });
      if (!res.ok) { const err = await res.json(); throw new Error(err.detail || 'Erro no upload'); }
      const data = await res.json();
      setStatus('ok');
      onUploadSuccess?.(data);
    } catch (e) {
      setStatus('error');
      setFileName(e.message);
    }
  };

  const onDrop = (e) => { e.preventDefault(); setDragging(false); handleFile(e.dataTransfer.files?.[0]); };

  const statusColor = { loading: '#0f62fe', ok: '#198038', error: '#da1e28' }[status] ?? '#525252';

  return (
    <div style={{
      backgroundColor: 'transparent',
      padding: '4px 0',
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      flexShrink: 0,
    }}>
      <style>{`
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .upload-btn:hover { background: #e8f0fe !important; border-color: #0f62fe !important; }
        .upload-btn:hover svg path { stroke: #0f62fe; }
        .upload-btn:hover .upload-label { color: #0f62fe !important; }
      `}</style>

      <div
        className="upload-btn"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        style={{
          border: `1px solid ${dragging ? '#0f62fe' : '#a8a8a8'}`,
          backgroundColor: dragging ? '#e8f0fe' : '#ffffff',
          padding: '5px 16px',
          borderRadius: '999px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '7px',
          transition: 'all 0.15s ease',
          flexShrink: 0,
        }}
      >
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
          <path d="M8 10V2M5 5L8 2L11 5" stroke="#525252" strokeWidth="1.3" strokeLinecap="square"/>
          <path d="M2 11V14H14V11" stroke="#525252" strokeWidth="1.3" strokeLinecap="square"/>
        </svg>
        <span className="upload-label" style={{
          fontSize: '12px',
          color: '#525252',
          letterSpacing: '0.32px',
          fontFamily: "'IBM Plex Sans', sans-serif",
          userSelect: 'none',
          transition: 'color 0.15s ease',
        }}>
          Importar Excel
        </span>
      </div>

      <input ref={inputRef} type="file" accept=".xlsx,.xls" onChange={(e) => handleFile(e.target.files?.[0])} style={{ display: 'none' }} />

      {status && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', minWidth: 0 }}>
          {status === 'loading' && (
            <svg width="13" height="13" viewBox="0 0 14 14" fill="none" style={{ animation: 'spin 1s linear infinite', flexShrink: 0 }}>
              <circle cx="7" cy="7" r="5.5" stroke="#e0e0e0" strokeWidth="1.5"/>
              <path d="M7 1.5A5.5 5.5 0 0 1 12.5 7" stroke="#0f62fe" strokeWidth="1.5" strokeLinecap="square"/>
            </svg>
          )}
          {status === 'ok' && (
            <svg width="13" height="13" viewBox="0 0 14 14" fill="none" style={{ flexShrink: 0 }}>
              <path d="M2.5 7L5.5 10L11.5 4" stroke="#198038" strokeWidth="1.5" strokeLinecap="square"/>
            </svg>
          )}
          {status === 'error' && (
            <svg width="13" height="13" viewBox="0 0 14 14" fill="none" style={{ flexShrink: 0 }}>
              <path d="M3 3L11 11M11 3L3 11" stroke="#da1e28" strokeWidth="1.5" strokeLinecap="square"/>
            </svg>
          )}
          <span style={{
            fontSize: '12px',
            color: statusColor,
            letterSpacing: '0.32px',
            fontFamily: "'IBM Plex Mono', monospace",
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            maxWidth: '340px',
          }}>
            {status === 'loading' && `Enviando ${fileName}...`}
            {status === 'ok' && `${fileName} carregado`}
            {status === 'error' && fileName}
          </span>
          {(status === 'ok' || status === 'error') && (
            <button
              onClick={() => { setStatus(null); setFileName(null); }}
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#a8a8a8', padding: '2px', display: 'flex', alignItems: 'center' }}
            >
              <svg width="11" height="11" viewBox="0 0 12 12" fill="none">
                <path d="M2 2L10 10M10 2L2 10" stroke="currentColor" strokeWidth="1.3" strokeLinecap="square"/>
              </svg>
            </button>
          )}
        </div>
      )}
    </div>
  );
};
