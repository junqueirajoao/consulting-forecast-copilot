import { useEffect, useState } from 'react';

const PAGE_SIZE = 15;

export const DataTable = () => {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);
  const [busca, setBusca] = useState('');
  const [abaSelecionada, setAbaSelecionada] = useState('');
  const [pagina, setPagina] = useState(1);

  const fetchDados = async (aba = '') => {
    setLoading(true);
    setErro(null);
    try {
      const url = aba
        ? `http://127.0.0.1:8000/dados?aba=${encodeURIComponent(aba)}`
        : 'http://127.0.0.1:8000/dados';
      const res = await fetch(url);
      if (!res.ok) throw new Error('Erro ao carregar dados');
      const data = await res.json();
      setDados(data);
      setPagina(1);
    } catch (e) {
      setErro(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchDados(); }, []);

  const handleAba = (aba) => {
    setAbaSelecionada(aba);
    setBusca('');
    fetchDados(aba);
  };

  const registrosFiltrados = dados?.registros?.filter((r) =>
    Object.values(r).some((v) =>
      String(v ?? '').toLowerCase().includes(busca.toLowerCase())
    )
  ) ?? [];

  const totalPaginas = Math.max(1, Math.ceil(registrosFiltrados.length / PAGE_SIZE));
  const paginaAtual = Math.min(pagina, totalPaginas);
  const registrosPagina = registrosFiltrados.slice((paginaAtual - 1) * PAGE_SIZE, paginaAtual * PAGE_SIZE);

  const MESES = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];

  const formatarAba = (v) => {
    // '2026-03' ou '2026-3' → 'Mar/26'
    const m = String(v).match(/^(\d{4})[-\/](\d{1,2})$/);
    if (m) return `${MESES[parseInt(m[2], 10) - 1]}/${m[1].slice(2)}`;
    return v;
  };

  const formatarData = (v) => {
    if (!v) return '—';
    const s = String(v).trim();
    // Já está em dd/mm/YYYY
    if (/^\d{2}\/\d{2}\/\d{4}$/.test(s)) return s;
    // ISO YYYY-MM-DD
    const iso = s.match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (iso) return `${iso[3]}/${iso[2]}/${iso[1]}`;
    // Timestamp JS (ms)
    if (/^\d{10,}$/.test(s)) {
      const d = new Date(parseInt(s));
      return d.toLocaleDateString('pt-BR');
    }
    return s;
  };

  const formatarValor = (v, col) => {
    if (v === null || v === undefined || v === '') return '—';
    if (col === 'Referência') return formatarAba(v);
    if (col === 'Data de Entrada' || col === 'Data de Saída') return formatarData(v);
    if (typeof v === 'number') return v.toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
    return String(v);
  };

  const isMoeda = (col) => col.toLowerCase().includes('receita');
  const isRef = (col) => col === 'Referência';

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', backgroundColor: '#ffffff' }}>

      {/* Toolbar */}
      <div style={{
        padding: '10px 16px',
        borderBottom: '1px solid #e0e0e0',
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        flexShrink: 0,
        flexWrap: 'wrap',
      }}>
        {/* Filtro por aba */}
        {dados?.abas?.length > 0 && (
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
            <button
              onClick={() => handleAba('')}
              style={{
                padding: '4px 12px',
                borderRadius: '999px',
                border: '1px solid',
                borderColor: abaSelecionada === '' ? '#0f62fe' : '#e0e0e0',
                backgroundColor: abaSelecionada === '' ? '#0f62fe' : '#ffffff',
                color: abaSelecionada === '' ? '#ffffff' : '#525252',
                fontSize: '12px',
                cursor: 'pointer',
                fontFamily: "'IBM Plex Sans', sans-serif",
                transition: 'all 0.15s',
              }}
            >
              Todas
            </button>
            {dados.abas.map((aba) => (
              <button
                key={aba}
                onClick={() => handleAba(aba)}
                style={{
                  padding: '4px 12px',
                  borderRadius: '999px',
                  border: '1px solid',
                  borderColor: abaSelecionada === aba ? '#0f62fe' : '#e0e0e0',
                  backgroundColor: abaSelecionada === aba ? '#0f62fe' : '#ffffff',
                  color: abaSelecionada === aba ? '#ffffff' : '#525252',
                  fontSize: '12px',
                  cursor: 'pointer',
                  fontFamily: "'IBM Plex Sans', sans-serif",
                  transition: 'all 0.15s',
                }}
              >
                {formatarAba(aba)}
              </button>
            ))}
          </div>
        )}

        {/* Busca */}
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '8px',
          border: '1px solid #e0e0e0', borderRadius: '999px', padding: '4px 12px',
          backgroundColor: '#f4f4f4', minWidth: '220px' }}>
          <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
            <circle cx="6.5" cy="6.5" r="5" stroke="#a8a8a8" strokeWidth="1.3"/>
            <path d="M10.5 10.5L14 14" stroke="#a8a8a8" strokeWidth="1.3" strokeLinecap="square"/>
          </svg>
          <input
            type="text"
            placeholder="Buscar..."
            value={busca}
            onChange={(e) => { setBusca(e.target.value); setPagina(1); }}
            style={{
              border: 'none', outline: 'none', background: 'transparent',
              fontSize: '13px', color: '#161616', width: '100%',
              fontFamily: "'IBM Plex Sans', sans-serif",
            }}
          />
          {busca && (
            <button onClick={() => setBusca('')} style={{ border: 'none', background: 'none', cursor: 'pointer', color: '#a8a8a8', padding: 0, display: 'flex' }}>
              <svg width="11" height="11" viewBox="0 0 12 12" fill="none">
                <path d="M2 2L10 10M10 2L2 10" stroke="currentColor" strokeWidth="1.3" strokeLinecap="square"/>
              </svg>
            </button>
          )}
        </div>

        {/* Contador */}
        <span style={{ fontSize: '12px', color: '#a8a8a8', fontFamily: "'IBM Plex Mono', monospace", flexShrink: 0 }}>
          {registrosFiltrados.length} registros
        </span>
      </div>

      {/* Tabela */}
      <div style={{ flex: 1, overflowY: 'auto', overflowX: 'auto' }}>
        {loading && (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '200px', color: '#a8a8a8', fontSize: '14px', gap: '10px' }}>
            <svg width="16" height="16" viewBox="0 0 14 14" fill="none" style={{ animation: 'spin 1s linear infinite' }}>
              <circle cx="7" cy="7" r="5.5" stroke="#e0e0e0" strokeWidth="1.5"/>
              <path d="M7 1.5A5.5 5.5 0 0 1 12.5 7" stroke="#0f62fe" strokeWidth="1.5" strokeLinecap="square"/>
            </svg>
            Carregando dados...
          </div>
        )}

        {erro && (
          <div style={{ padding: '24px', textAlign: 'center', color: '#da1e28', fontSize: '14px' }}>
            {erro} — faça o upload de um Excel primeiro.
          </div>
        )}

        {!loading && !erro && dados && (
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', fontFamily: "'IBM Plex Sans', sans-serif" }}>
            <thead>
              <tr style={{ backgroundColor: '#f4f4f4', borderBottom: '2px solid #0f62fe' }}>
                {dados.colunas.map((col) => (
                  <th key={col} style={{
                    padding: '10px 16px',
                    textAlign: isMoeda(col) ? 'right' : 'left',
                    fontSize: '11px',
                    fontWeight: '600',
                    color: '#525252',
                    letterSpacing: '0.32px',
                    textTransform: 'uppercase',
                    whiteSpace: 'nowrap',
                    position: 'sticky',
                    top: 0,
                    backgroundColor: '#f4f4f4',
                    zIndex: 1,
                  }}>
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {registrosPagina.length === 0 ? (
                <tr>
                  <td colSpan={dados.colunas.length} style={{ padding: '40px', textAlign: 'center', color: '#a8a8a8' }}>
                    Nenhum resultado encontrado
                  </td>
                </tr>
              ) : (
                registrosPagina.map((row, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid #f4f4f4', backgroundColor: i % 2 === 0 ? '#ffffff' : '#fafafa' }}>
                    {dados.colunas.map((col) => (
                      <td key={col} style={{
                        padding: '10px 16px',
                        color: isRef(col) ? '#0f62fe' : '#161616',
                        fontWeight: isRef(col) ? '500' : '400',
                        textAlign: isMoeda(col) ? 'right' : 'left',
                        whiteSpace: 'nowrap',
                        fontFamily: isMoeda(col) || isRef(col) ? "'IBM Plex Mono', monospace" : 'inherit',
                        fontSize: isMoeda(col) || isRef(col) ? '12px' : '13px',
                      }}>
                        {isMoeda(col) && row[col] !== null && row[col] !== undefined && row[col] !== ''
                          ? `R$ ${formatarValor(row[col], col)}`
                          : formatarValor(row[col], col)}
                      </td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        )}
      </div>

      {/* Paginação */}
      {!loading && !erro && totalPaginas > 1 && (
        <div style={{
          borderTop: '1px solid #e0e0e0',
          padding: '8px 16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-end',
          gap: '8px',
          flexShrink: 0,
        }}>
          <button onClick={() => setPagina(1)} disabled={paginaAtual === 1}
            style={{ border: 'none', background: 'none', cursor: paginaAtual === 1 ? 'not-allowed' : 'pointer', color: paginaAtual === 1 ? '#e0e0e0' : '#525252', fontSize: '12px' }}>«</button>
          <button onClick={() => setPagina(p => Math.max(1, p - 1))} disabled={paginaAtual === 1}
            style={{ border: 'none', background: 'none', cursor: paginaAtual === 1 ? 'not-allowed' : 'pointer', color: paginaAtual === 1 ? '#e0e0e0' : '#525252', fontSize: '12px' }}>‹</button>
          <span style={{ fontSize: '12px', color: '#525252', fontFamily: "'IBM Plex Mono', monospace" }}>
            {paginaAtual} / {totalPaginas}
          </span>
          <button onClick={() => setPagina(p => Math.min(totalPaginas, p + 1))} disabled={paginaAtual === totalPaginas}
            style={{ border: 'none', background: 'none', cursor: paginaAtual === totalPaginas ? 'not-allowed' : 'pointer', color: paginaAtual === totalPaginas ? '#e0e0e0' : '#525252', fontSize: '12px' }}>›</button>
          <button onClick={() => setPagina(totalPaginas)} disabled={paginaAtual === totalPaginas}
            style={{ border: 'none', background: 'none', cursor: paginaAtual === totalPaginas ? 'not-allowed' : 'pointer', color: paginaAtual === totalPaginas ? '#e0e0e0' : '#525252', fontSize: '12px' }}>»</button>
        </div>
      )}

      <style>{`
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
};
