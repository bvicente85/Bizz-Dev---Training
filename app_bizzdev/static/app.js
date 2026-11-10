// ============================================================================
// SKOLAE BIZZ DEV AI — FRONTEND CONTROLLER (APPLE / LINEAR / DOTS STANDARD)
// ============================================================================

const STATE = {
  clients: [],
  filteredClients: [],
  statusFilter: 'Todos',
  activeClientId: 'Desentop_Ambiente',
  activeClientDetail: null,
  activeContextTab: 'resumo',
  dashboard: null,
  lastMarginMin65: 2094.43,
  lastPPTData: null,
  svgCache: {}
};

// ============================================================================
// 1. CARREGADOR DE ÍCONES SVG LOCAIS (assets/icons/lucide/)
// ============================================================================
async function fetchLocalLucideSvg(iconName) {
  const clean = (iconName || 'circle').trim().toLowerCase();
  if (STATE.svgCache[clean]) return STATE.svgCache[clean];
  try {
    const res = await fetch(`/icons/lucide/${encodeURIComponent(clean)}.svg`);
    if (!res.ok) return '';
    const svgText = await res.text();
    STATE.svgCache[clean] = svgText;
    return svgText;
  } catch (e) {
    return '';
  }
}

async function hydrateLucideIcons(root = document) {
  const nodes = root.querySelectorAll('[data-lucide]');
  await Promise.all(
    Array.from(nodes).map(async (node) => {
      const name = node.getAttribute('data-lucide');
      if (!name || node.dataset.loaded === name) return;
      const svg = await fetchLocalLucideSvg(name);
      if (svg) {
        node.innerHTML = svg;
        node.dataset.loaded = name;
      }
    })
  );
}

// ============================================================================
// 2. RENDERIZADOR MARKDOWN LIMPO & HUMANO
// ============================================================================
function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function renderMarkdown(md) {
  if (!md) return '';
  let text = String(md).replace(/\r\n/g, '\n');

  // Extrair blocos de código ```...```
  const codeBlocks = [];
  text = text.replace(/```(?:\w+)?\n([\s\S]*?)```/g, (_, code) => {
    const idx = codeBlocks.length;
    codeBlocks.push(code.trim());
    return `@@CODEBLOCK_${idx}@@`;
  });

  // Tabelas Markdown simples
  text = text.replace(/((?:^\|.+\|\n)+)/gm, (tableBlock) => {
    const lines = tableBlock.trim().split('\n');
    if (lines.length < 2) return tableBlock;
    let html = '<table>';
    lines.forEach((line, idx) => {
      if (/^\|[\s\-:|]+\|$/.test(line.trim())) return;
      const cells = line.split('|').slice(1, -1).map((c) => c.trim());
      const tag = idx === 0 ? 'th' : 'td';
      if (idx === 0) html += '<thead>';
      if (idx === 2) html += '<tbody>';
      html += '<tr>' + cells.map((c) => `<${tag}>${formatInlineMarkdown(c)}</${tag}>`).join('') + '</tr>';
      if (idx === 0) html += '</thead>';
    });
    html += '</tbody></table>';
    return html;
  });

  const lines = text.split('\n');
  const out = [];
  let inList = false;

  for (let rawLine of lines) {
    const line = rawLine.trim();
    if (!line) {
      if (inList) {
        out.push('</ul>');
        inList = false;
      }
      continue;
    }

    if (line.startsWith('@@CODEBLOCK_') || line.startsWith('<table>')) {
      if (inList) {
        out.push('</ul>');
        inList = false;
      }
      out.push(line);
      continue;
    }

    if (line.startsWith('### ')) {
      if (inList) { out.push('</ul>'); inList = false; }
      out.push(`<h3>${formatInlineMarkdown(line.slice(4))}</h3>`);
    } else if (line.startsWith('#### ')) {
      if (inList) { out.push('</ul>'); inList = false; }
      out.push(`<h4>${formatInlineMarkdown(line.slice(5))}</h4>`);
    } else if (line.startsWith('## ')) {
      if (inList) { out.push('</ul>'); inList = false; }
      out.push(`<h3>${formatInlineMarkdown(line.slice(3))}</h3>`);
    } else if (line.startsWith('> ')) {
      if (inList) { out.push('</ul>'); inList = false; }
      out.push(`<blockquote>${formatInlineMarkdown(line.slice(2))}</blockquote>`);
    } else if (/^([-*]|\d+\.)\s+/.test(line)) {
      if (!inList) {
        out.push('<ul>');
        inList = true;
      }
      const itemText = line.replace(/^([-*]|\d+\.)\s+/, '');
      out.push(`<li>${formatInlineMarkdown(itemText)}</li>`);
    } else {
      if (inList) { out.push('</ul>'); inList = false; }
      out.push(`<p>${formatInlineMarkdown(line)}</p>`);
    }
  }
  if (inList) out.push('</ul>');

  let finalHtml = out.join('\n');

  // Re-injetar blocos de código com botão de cópia em 1 clique
  finalHtml = finalHtml.replace(/@@CODEBLOCK_(\d+)@@/g, (_, idx) => {
    const rawCode = codeBlocks[Number(idx)] || '';
    const encoded = encodeURIComponent(rawCode);
    return `
      <div class="relative group my-2.5">
        <button onclick="copyEncodedText('${encoded}', this)"
          class="absolute right-2.5 top-2.5 px-2.5 py-1 rounded-md bg-white hover:bg-[#FFF5EC] text-[#111827] hover:text-[#FF912B] border border-[#E5E7EB] text-[11px] font-medium shadow-2xs transition cursor-pointer">
          Copiar Minuta
        </button>
        <pre class="pr-24">${escapeHtml(rawCode)}</pre>
      </div>
    `;
  });

  return finalHtml;
}

function formatInlineMarkdown(str) {
  let s = escapeHtml(str);
  s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/\*(.+?)\*/g, '<em>$1</em>');
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  return s;
}

function copyEncodedText(encoded, btnEl) {
  const txt = decodeURIComponent(encoded);
  navigator.clipboard.writeText(txt);
  if (btnEl) {
    const prev = btnEl.textContent;
    btnEl.textContent = '✓ Copiado!';
    setTimeout(() => { btnEl.textContent = prev; }, 1600);
  }
}

// ============================================================================
// 3. DASHBOARD & CONTAS DA CARTEIRA
// ============================================================================
async function loadDashboard() {
  try {
    const res = await fetch('/api/dashboard');
    const data = await res.json();
    STATE.dashboard = data;

    const t = data.metrics.tasks;
    document.getElementById('metric-tasks-value').textContent = `${t.completed} / ${t.total}`;
    document.getElementById('metric-tasks-sub').textContent = `${t.pending} pendentes · clique p/ gerir`;
    const pct = t.total > 0 ? Math.round((t.completed / t.total) * 100) : 0;
    document.getElementById('metric-tasks-bar').style.width = `${pct}%`;

    const m = data.metrics.margin;
    document.getElementById('metric-margin-value').textContent = `${m.average_pct}%`;

    const c = data.metrics.clients;
    document.getElementById('metric-clients-active').textContent = `${c.active_pipeline}`;
    document.getElementById('metric-clients-total').textContent = `de ${c.total_portfolio} contas em 032_Clientes`;
    document.getElementById('metric-clients-proposals').textContent = `${c.in_proposal} contas com propostas / dossiers ativos`;
  } catch (e) {
    console.error('Erro ao carregar dashboard:', e);
  }
}

async function loadClientsList() {
  try {
    const res = await fetch('/api/clients');
    const data = await res.json();
    STATE.clients = data.clients || [];
    filterAccountsList();
  } catch (e) {
    console.error('Erro ao carregar lista de clientes:', e);
  }
}

function setAccountStatusFilter(status) {
  STATE.statusFilter = status;
  document.querySelectorAll('.acc-filter-pill').forEach((btn) => {
    btn.className = 'acc-filter-pill text-[11px] px-2 py-0.5 rounded-md font-medium bg-white text-[#4B5563] border border-[#E5E7EB] hover:border-[#D1D5DB] transition';
  });
  const activeBtn = document.getElementById(`flt-${status}`);
  if (activeBtn) {
    activeBtn.className = 'acc-filter-pill text-[11px] px-2 py-0.5 rounded-md font-medium bg-[#111827] text-white transition';
  }
  filterAccountsList();
}

function filterAccountsList() {
  const q = (document.getElementById('account-search-input')?.value || '').trim().toLowerCase();
  const st = STATE.statusFilter;

  STATE.filteredClients = STATE.clients.filter((c) => {
    const matchesQ = !q || c.name.toLowerCase().includes(q) || (c.core_business || '').toLowerCase().includes(q);
    const matchesSt = st === 'Todos' || c.status === st;
    return matchesQ && matchesSt;
  });

  document.getElementById('sidebar-accounts-count').textContent = STATE.filteredClients.length;
  renderAccountsSidebar();
}

function getStatusDotClass(status) {
  if (status === 'Em Proposta') return 'proposta';
  if (status === 'Ativo') return 'ativo';
  if (status === 'Qualificação') return 'qualificacao';
  return 'carteira';
}

function renderAccountsSidebar() {
  const container = document.getElementById('accounts-list-container');
  if (!container) return;

  if (STATE.filteredClients.length === 0) {
    container.innerHTML = `<div class="text-[12px] text-[#9CA3AF] text-center py-6">Nenhuma conta encontrada.</div>`;
    return;
  }

  container.innerHTML = STATE.filteredClients
    .map((c) => {
      const isActive = c.id === STATE.activeClientId;
      const dotClass = getStatusDotClass(c.status);
      return `
        <div onclick="selectClient('${c.id.replace(/'/g, "\\'")}')"
          class="account-item ${isActive ? 'active' : ''}">
          <div class="flex items-center gap-2.5 min-w-0">
            <span class="status-dot ${dotClass}" title="${escapeHtml(c.status)}"></span>
            <div class="truncate">
              <div class="text-[12.5px] font-medium text-[#111827] truncate">${escapeHtml(c.name)}</div>
              <div class="text-[10.5px] text-[#6B7280] truncate">${escapeHtml(c.core_business)}</div>
            </div>
          </div>
          ${c.has_proposals ? `<span class="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-[#FFF5EC] text-[#FF912B] flex-shrink-0">PPT/PDF</span>` : ''}
        </div>
      `;
    })
    .join('');
}

// ============================================================================
// 4. PAINEL LATERAL DIREITO (CONTEXTO ATIVO DO CLIENTE)
// ============================================================================
async function selectClient(clientId) {
  STATE.activeClientId = clientId;
  renderAccountsSidebar();

  try {
    const res = await fetch(`/api/clients/${encodeURIComponent(clientId)}`);
    if (!res.ok) return;
    const detail = await res.json();
    STATE.activeClientDetail = detail;

    // Atualizar Cabeçalho Direito
    document.getElementById('ctx-client-name').textContent = detail.name;
    document.getElementById('ctx-core-business').textContent = detail.core_business || 'Formação Corporativa Intra-Empresa';
    document.getElementById('ctx-status-badge').textContent = detail.status;
    document.getElementById('ctx-last-date').textContent = detail.last_interaction || '';

    // Atualizar Pill na Caixa de Chat
    const pill = document.getElementById('active-client-pill');
    if (pill) {
      pill.textContent = detail.name;
      pill.classList.remove('hidden');
    }

    renderActiveContextTab();
  } catch (e) {
    console.error('Erro ao carregar detalhe do cliente:', e);
  }
}

function switchContextTab(tabName) {
  STATE.activeContextTab = tabName;
  ['resumo', 'acoes', 'reunioes', 'ficheiros'].forEach((t) => {
    const btn = document.getElementById(`tab-btn-${t}`);
    if (!btn) return;
    if (t === tabName) {
      btn.className = 'ctx-tab-btn text-[11px] font-semibold py-1 rounded-md bg-white text-[#111827] shadow-2xs transition';
    } else {
      btn.className = 'ctx-tab-btn text-[11px] font-medium py-1 rounded-md text-[#6B7280] hover:text-[#111827] transition';
    }
  });
  renderActiveContextTab();
}

function renderActiveContextTab() {
  const container = document.getElementById('ctx-panel-body');
  const d = STATE.activeClientDetail;
  if (!container || !d) return;

  // Banner de Guardrail Factual (se aplicável, ex: Carl Zeiss #SOMOS, Devoteam, Desentop)
  const guardrailHtml = (d.guardrails && d.guardrails.length > 0)
    ? `
      <div class="p-3 rounded-xl bg-[#FFF5EC] border border-[#FF912B]/35 text-[11.5px] text-[#111827] leading-relaxed">
        <div class="font-bold text-[#FF912B] uppercase tracking-wider text-[10px] mb-0.5">⚡ Nota de Rigor SKOLAE</div>
        ${escapeHtml(d.guardrails[0])}
      </div>
    `
    : '';

  if (STATE.activeContextTab === 'resumo') {
    const decisoresHtml = (d.decisores && d.decisores.length > 0)
      ? d.decisores.map((dec) => `<li class="text-[12px] text-[#374151] flex items-start gap-1.5"><span class="text-[#FF912B] font-bold">•</span><span>${escapeHtml(dec)}</span></li>`).join('')
      : `<li class="text-[12px] text-[#9CA3AF]">Sem decisores listados no cabeçalho.</li>`;

    const areasHtml = (d.areas_interesse && d.areas_interesse.length > 0)
      ? d.areas_interesse.map((ar) => `<span class="text-[11px] px-2 py-0.5 rounded-md bg-[#F5F5F7] border border-[#E5E7EB] text-[#374151]">${escapeHtml(ar)}</span>`).join('')
      : `<span class="text-[11px] text-[#9CA3AF]">Formação Intra-Empresa à Medida</span>`;

    const dbContactsHtml = (d.db_contacts && d.db_contacts.length > 0)
      ? `
        <div class="apple-card p-3.5">
          <div class="text-[11px] font-bold uppercase tracking-wider text-[#6B7280] mb-2">
            Contactos nas Bases Excel (031_Bases_Dados)
          </div>
          <div class="space-y-2">
            ${d.db_contacts.slice(0, 5).map((c) => `
              <div class="p-2 rounded-lg bg-[#FBFBFD] border border-[#E5E7EB] flex items-center justify-between gap-2">
                <div class="min-w-0">
                  <div class="text-[12px] font-semibold text-[#111827] truncate">${escapeHtml(c.name || c.company)}</div>
                  <div class="text-[11px] text-[#6B7280] truncate">${escapeHtml(c.role || c.status)} · ${escapeHtml(c.email)}</div>
                </div>
                ${c.email ? `
                  <button onclick="navigator.clipboard.writeText('${escapeHtml(c.email)}')" title="Copiar e-mail"
                    class="text-[10.5px] px-2 py-1 rounded bg-white border border-[#E5E7EB] hover:border-[#FF912B] text-[#374151] flex-shrink-0 cursor-pointer">
                    Copiar
                  </button>
                ` : ''}
              </div>
            `).join('')}
          </div>
        </div>
      `
      : '';

    container.innerHTML = `
      ${guardrailHtml}

      <div class="apple-card p-3.5">
        <div class="text-[11px] font-bold uppercase tracking-wider text-[#6B7280] mb-2">Decisores & Interlocutores</div>
        <ul class="space-y-1">${decisoresHtml}</ul>
      </div>

      <div class="apple-card p-3.5">
        <div class="text-[11px] font-bold uppercase tracking-wider text-[#6B7280] mb-2">Áreas de Interesse Mapeadas</div>
        <div class="flex flex-wrap gap-1.5">${areasHtml}</div>
      </div>

      ${dbContactsHtml}

      <div class="apple-card p-3.5">
        <div class="text-[11px] font-bold uppercase tracking-wider text-[#6B7280] mb-2">Contexto Integral (${escapeHtml(d.name)})</div>
        <div class="prose-skolae text-[12.5px] max-h-[340px] overflow-y-auto pr-1">
          ${renderMarkdown(d.context_md || 'Sem ficheiro de contexto registado.')}
        </div>
      </div>
    `;
  } else if (STATE.activeContextTab === 'acoes') {
    const items = d.action_items || [];
    const actionsListHtml = items.length > 0
      ? items.map((item) => `
          <div class="p-2.5 rounded-xl bg-white border border-[#E5E7EB] flex items-start gap-2.5">
            <input type="checkbox" ${item.completed ? 'checked' : ''} class="mt-1 accent-[#FF912B] cursor-pointer" />
            <span class="text-[12.5px] leading-snug ${item.completed ? 'line-through text-[#9CA3AF]' : 'text-[#111827]'}">
              ${escapeHtml(item.text)}
            </span>
          </div>
        `).join('')
      : `<div class="text-[12px] text-[#6B7280]">Sem ações pendentes isoladas. Consulta o registo de progresso abaixo.</div>`;

    container.innerHTML = `
      ${guardrailHtml}
      <div class="space-y-2">
        <div class="text-[11px] font-bold uppercase tracking-wider text-[#6B7280] px-1">Próximas Ações Agendadas</div>
        ${actionsListHtml}
      </div>

      <div class="apple-card p-3.5 mt-3">
        <div class="text-[11px] font-bold uppercase tracking-wider text-[#6B7280] mb-2">Progresso Comercial (_progress.md)</div>
        <div class="prose-skolae text-[12.5px]">
          ${renderMarkdown(d.progress_md || 'Sem histórico de progresso registado.')}
        </div>
      </div>
    `;
  } else if (STATE.activeContextTab === 'reunioes') {
    container.innerHTML = `
      ${guardrailHtml}
      <div class="apple-card p-3.5">
        <div class="flex items-center justify-between mb-2">
          <span class="text-[11px] font-bold uppercase tracking-wider text-[#6B7280]">Atas & Notas de Reunião</span>
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-[#F5F5F7] text-[#6B7280]">Append-Only</span>
        </div>
        <div class="prose-skolae text-[12.5px]">
          ${renderMarkdown(d.meeting_notes_md || 'Sem notas de reunião registadas em `_meeting_notes.md`.')}
        </div>
      </div>
    `;
  } else if (STATE.activeContextTab === 'ficheiros') {
    const filesHtml = (d.files || []).map((f) => {
      let badge = 'MD';
      let badgeCls = 'bg-gray-100 text-gray-700';
      if (f.type === 'pdf') { badge = 'PDF'; badgeCls = 'bg-red-50 text-red-700 border border-red-200'; }
      if (f.type === 'pptx') { badge = 'PPTX'; badgeCls = 'bg-[#FFF5EC] text-[#FF912B] border border-[#FF912B]/30'; }
      return `
        <div onclick="openWorkspaceFile('${f.rel_path.replace(/'/g, "\\'")}')"
          class="p-2.5 rounded-xl bg-white border border-[#E5E7EB] hover:border-[#FF912B] flex items-center justify-between gap-2 cursor-pointer transition">
          <div class="flex items-center gap-2 min-w-0">
            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded ${badgeCls} flex-shrink-0">${badge}</span>
            <span class="text-[12px] font-medium text-[#111827] truncate" title="${escapeHtml(f.name)}">${escapeHtml(f.name)}</span>
          </div>
          <span class="text-[11px] text-[#FF912B] font-medium flex-shrink-0">Abrir</span>
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div class="space-y-2">
        <div class="text-[11px] font-bold uppercase tracking-wider text-[#6B7280] px-1">
          Ficheiros na Pasta do Cliente (${(d.files || []).length})
        </div>
        ${filesHtml}
      </div>
    `;
  }
}

async function openWorkspaceFile(relPath) {
  try {
    await fetch('/api/open-file', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rel_path: relPath })
    });
  } catch (e) {
    console.error('Erro ao abrir ficheiro:', e);
  }
}

function openCurrentClientFolder() {
  if (!STATE.activeClientId) return;
  openWorkspaceFile(`03_Carteira_Clientes/032_Clientes/${STATE.activeClientId}`);
}

function openWorkspaceTemplatePPT() {
  openWorkspaceFile('Template Proposta - 1 curso.pptx');
}

// ============================================================================
// 5. ÁREA DE CONVERSA HUMANA (CHAT ESTRATÉGICO BIZZ DEV AI)
// ============================================================================
function appendChatMessage(role, markdownText, modeBadge = '') {
  const inner = document.getElementById('chat-messages-inner');
  const container = document.getElementById('chat-messages-container');
  if (!inner) return;

  const isUser = role === 'user';
  const msgEl = document.createElement('div');
  msgEl.className = `animate-msg flex items-start gap-3.5 ${isUser ? 'justify-end' : ''}`;

  if (isUser) {
    msgEl.innerHTML = `
      <div class="max-w-xl bg-[#111827] text-white px-4 py-3 rounded-2xl rounded-tr-xs text-[13.5px] leading-relaxed shadow-xs">
        ${escapeHtml(markdownText)}
      </div>
      <div class="w-8 h-8 rounded-full bg-[#E5E7EB] text-[#111827] font-semibold text-[11.5px] flex items-center justify-center flex-shrink-0">
        BV
      </div>
    `;
  } else {
    msgEl.innerHTML = `
      <div class="w-8 h-8 rounded-xl bg-[#FF912B] text-white font-bold text-[12px] flex items-center justify-center flex-shrink-0 shadow-xs mt-0.5">
        SK
      </div>
      <div class="flex-1 apple-card p-4 min-w-0">
        ${modeBadge ? `
          <div class="flex items-center justify-between mb-2 pb-1.5 border-b border-[#E5E7EB]/70">
            <span class="text-[11px] font-semibold text-[#FF912B] uppercase tracking-wider">${escapeHtml(modeBadge)}</span>
            <span class="text-[10.5px] text-[#9CA3AF]">SKOLAE Standard · PT-PT</span>
          </div>
        ` : ''}
        <div class="prose-skolae">
          ${renderMarkdown(markdownText)}
        </div>
      </div>
    `;
  }

  inner.appendChild(msgEl);
  container.scrollTop = container.scrollHeight;
}

async function sendChatMessage(customText = null) {
  const input = document.getElementById('chat-input');
  const text = (customText !== null ? customText : input.value).trim();
  if (!text) return;

  if (customText === null) input.value = '';
  appendChatMessage('user', text);

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        client_id: STATE.activeClientId
      })
    });
    const data = await res.json();
    appendChatMessage('assistant', data.reply, data.mode || 'Parceiro Estratégico BIZZ DEV AI');
  } catch (e) {
    appendChatMessage('assistant', 'Ocorreu um erro ao comunicar com o motor local.', 'Erro Local');
  }
}

function handleChatKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendChatMessage();
  }
}

function triggerQuickPrompt(promptText) {
  sendChatMessage(promptText);
}

// ============================================================================
// 6. MODAIS DE AÇÃO RÁPIDA (FAST-TRACK, MARGEM, PPT, ÍCONES, CONTACTOS)
// ============================================================================
function closeModal(id) {
  document.getElementById(id)?.classList.add('hidden');
}

// --- MODAL 1: FOLLOW-UP FAST-TRACK ---
async function openFastTrackModal() {
  const d = STATE.activeClientDetail;
  if (d) {
    const firstDec = (d.decisores && d.decisores[0]) ? d.decisores[0].split('(')[0].split('—')[0].trim() : '';
    const firstArea = (d.areas_interesse && d.areas_interesse[0]) ? d.areas_interesse[0].replace(/\s*\([^)]*\)/g, '') : '';
    document.getElementById('ft-recipient').value = firstDec;
    document.getElementById('ft-topic').value = firstArea;
  }
  document.getElementById('modal-fast-track').classList.remove('hidden');
  await refreshFastTrackDraft();
}

async function refreshFastTrackDraft() {
  const ttype = document.getElementById('ft-template-type').value;
  const recipient = document.getElementById('ft-recipient').value;
  const topic = document.getElementById('ft-topic').value;

  const res = await fetch('/api/actions/fast-track', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: STATE.activeClientId,
      template_type: ttype,
      recipient_name: recipient,
      topic: topic
    })
  });
  const data = await res.json();
  document.getElementById('ft-subject').value = data.subject || '';
  document.getElementById('ft-body').value = data.body || '';
  updateLiveWordCount();
}

function updateLiveWordCount() {
  const txt = document.getElementById('ft-body').value || '';
  const lines = txt.split('\n').map((l) => l.trim()).filter(Boolean);
  const bodyLines = lines.filter((l) => {
    const low = l.toLowerCase();
    return !low.startsWith('olá ') && !low.startsWith('bom dia') && !low.startsWith('boa tarde') &&
           !low.startsWith('com os melhores cumprimentos') && !low.startsWith('cumprimentos') &&
           !low.startsWith('obrigado e até breve') && !low.startsWith('bruno vicente');
  });
  const words = (bodyLines.join(' ').match(/\b\w+\b/g) || []).length;
  const badge = document.getElementById('ft-word-badge');
  badge.textContent = `${words} palavras no corpo`;
  if (words >= 35 && words <= 58) {
    badge.className = 'text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200';
  } else {
    badge.className = 'text-[11px] font-semibold px-2 py-0.5 rounded-full bg-[#FFF5EC] text-[#FF912B] border border-[#FF912B]/30';
  }
}

function copyFastTrackToClipboard() {
  const body = document.getElementById('ft-body').value;
  navigator.clipboard.writeText(body);
  const lbl = document.getElementById('ft-copy-btn-label');
  lbl.textContent = '✓ Copiado para o Clipboard!';
  setTimeout(() => { lbl.textContent = 'Copiar E-mail'; }, 1800);
}

// --- MODAL 2: AUDITORIA DE MARGEM & SIMULADOR TMB 25-26 ---
function openMarginModal() {
  document.getElementById('modal-margin').classList.remove('hidden');
  runMarginAudit();
}

function onMarginAreaChange() {
  const rate = document.getElementById('mrg-area').value;
  document.getElementById('mrg-rate').value = rate;
  runMarginAudit();
}

async function runMarginAudit() {
  const horas = parseFloat(document.getElementById('mrg-horas').value || '14');
  const rate = parseFloat(document.getElementById('mrg-rate').value || '50');
  const pax = parseInt(document.getElementById('mrg-pax').value || '12', 10);
  const estafeta = parseFloat(document.getElementById('mrg-estafeta').value || '9.05');
  const outros = parseFloat(document.getElementById('mrg-outros').value || '0');
  const local = document.getElementById('mrg-local').value || 'Lisboa';
  const kit = document.getElementById('mrg-kit').checked;
  const tabuleiro = document.getElementById('mrg-tabuleiro').checked;
  const pv = parseFloat(document.getElementById('mrg-preco-venda').value || '0');

  const res = await fetch('/api/margin/calculate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      preco_venda: pv,
      horas_formacao: horas,
      valor_hora_formador: rate,
      num_formandos: pax,
      incluir_kit: kit,
      estafeta: estafeta,
      outros_custos: outros,
      local_formacao: local,
      inclui_tabuleiro_jogo: tabuleiro
    })
  });
  const data = await res.json();
  STATE.lastMarginMin65 = data.preco_minimo_65;

  document.getElementById('mrg-pct-display').textContent = `${data.margem_percentual.toFixed(1)}%`;
  document.getElementById('mrg-custos-display').textContent = `${data.custos_diretos.toFixed(2)} €`;
  document.getElementById('mrg-abs-display').textContent = `${data.margem_absoluta.toFixed(2)} €`;
  document.getElementById('mrg-min65-display').textContent = `${data.preco_minimo_65.toFixed(2)} €`;
  document.getElementById('mrg-script-raw').textContent = data.script_output || '';

  const pill = document.getElementById('mrg-status-pill');
  const pctEl = document.getElementById('mrg-pct-display');
  if (data.aprovada) {
    pill.textContent = '✓ APROVADA ≥ 65%';
    pill.className = 'text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800';
    pctEl.className = 'text-[32px] font-bold tracking-tight text-emerald-600';
  } else {
    pill.textContent = '⚠️ SUB-OTIMIZADA (< 65%)';
    pill.className = 'text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-red-100 text-red-700';
    pctEl.className = 'text-[32px] font-bold tracking-tight text-red-600';
  }

  const alertsBox = document.getElementById('mrg-alerts-box');
  alertsBox.innerHTML = (data.alerts || []).map((a) => `
    <div class="p-2 rounded-lg bg-[#FFF5EC] border border-[#FF912B]/35 text-[11px] text-[#111827] leading-snug">
      ${escapeHtml(a)}
    </div>
  `).join('');
}

function applyMinimum65Price() {
  document.getElementById('mrg-preco-venda').value = Math.ceil(STATE.lastMarginMin65 / 10) * 10;
  runMarginAudit();
}

// --- MODAL 3: NOVA PROPOSTA PPT (SLIDE 6 + CONTACTOS) ---
function openPPTModal() {
  const d = STATE.activeClientDetail;
  document.getElementById('ppt-client-name').value = d ? d.name : 'Desentop Ambiente';
  if (d && d.areas_interesse && d.areas_interesse.length > 0) {
    document.getElementById('ppt-theme').value = d.areas_interesse[0].replace(/\s*\([^)]*\)/g, '');
  }
  document.getElementById('modal-ppt').classList.remove('hidden');
  generatePPTPreview();
}

async function generatePPTPreview() {
  const cname = document.getElementById('ppt-client-name').value;
  const theme = document.getElementById('ppt-theme').value;
  const impact = document.getElementById('ppt-impact').value;
  const pillars = document.getElementById('ppt-pillars').value;

  const res = await fetch('/api/actions/ppt-proposal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_name: cname,
      theme: theme,
      impact_goal: impact,
      pillars: pillars
    })
  });
  const data = await res.json();
  STATE.lastPPTData = data;

  const s6 = document.getElementById('ppt-slide6-preview');
  s6.innerHTML = (data.slide_6_paragraphs || []).map((p) => {
    const highlighted = escapeHtml(p).replace(
      /\*\*(.+?)\*\*/g,
      '<strong style="color: #FF912B;">$1</strong>'
    );
    return `<p>${highlighted}</p>`;
  }).join('');

  const s12 = document.getElementById('ppt-slide12-preview');
  s12.innerHTML = (data.slide_12_competencias || []).map((c) => `
    <span class="inline-flex items-center gap-1.5 text-[11.5px] font-medium px-2.5 py-1 rounded-lg bg-white border border-[#E5E7EB] text-[#111827]">
      <span class="w-3.5 h-3.5 text-[#FF912B] lucide-inline" data-lucide="${c.icon}"></span>
      <span>${escapeHtml(c.tag)}</span>
    </span>
  `).join('');

  hydrateLucideIcons(s12);
}

function copyPPTFramework() {
  if (!STATE.lastPPTData) return;
  const plain = STATE.lastPPTData.slide_6_paragraphs
    .map((p) => p.replace(/\*\*/g, ''))
    .join('\n\n');
  navigator.clipboard.writeText(plain);
  const lbl = document.getElementById('ppt-copy-btn-label');
  lbl.textContent = '✓ Enquadramento Copiado!';
  setTimeout(() => { lbl.textContent = 'Copiar Enquadramento Slide 6'; }, 1800);
}

// --- MODAL 4: BIBLIOTECA DE ÍCONES LUCIDE ---
async function openIconsModal() {
  document.getElementById('modal-icons').classList.remove('hidden');
  await searchLucideLibrary();
}

async function searchLucideLibrary() {
  const q = document.getElementById('lucide-search-input').value || '';
  const res = await fetch(`/api/icons?q=${encodeURIComponent(q)}&limit=96`);
  const data = await res.json();
  document.getElementById('lucide-total-badge').textContent = data.total;

  const grid = document.getElementById('lucide-grid-container');
  grid.innerHTML = (data.icons || []).map((ic) => `
    <button onclick="copyLucideIconName('${ic}')"
      title="Clique para copiar '${ic}.svg'"
      class="p-2.5 rounded-xl bg-[#FBFBFD] hover:bg-[#FFF5EC] border border-[#E5E7EB] hover:border-[#FF912B] flex flex-col items-center justify-center gap-1.5 transition group cursor-pointer">
      <img src="/icons/lucide/${encodeURIComponent(ic)}.svg" alt="${ic}" class="w-5 h-5 opacity-80 group-hover:opacity-100" loading="lazy" />
      <span class="text-[10px] text-[#4B5563] group-hover:text-[#111827] truncate w-full text-center">${ic}</span>
    </button>
  `).join('');
}

function copyLucideIconName(ic) {
  navigator.clipboard.writeText(`assets/icons/lucide/${ic}.svg`);
  const toast = document.getElementById('lucide-copy-toast');
  toast.textContent = `✓ Copiado: ${ic}.svg`;
  toast.classList.remove('hidden');
  setTimeout(() => toast.classList.add('hidden'), 1800);
}

// --- MODAL 5: BASE DE CONTACTOS EXCEL ---
async function openContactsModal() {
  document.getElementById('modal-contacts').classList.remove('hidden');
  await searchContactsDatabase();
}

async function searchContactsDatabase() {
  const q = document.getElementById('contacts-search-input').value || '';
  const res = await fetch(`/api/contacts?q=${encodeURIComponent(q)}&limit=80`);
  const data = await res.json();
  document.getElementById('contacts-count-label').textContent = `${data.matched} de ${data.total_database} contactos`;

  const tbody = document.getElementById('contacts-table-body');
  tbody.innerHTML = (data.contacts || []).map((c) => `
    <tr class="hover:bg-[#FBFBFD]">
      <td class="py-2 px-3 font-medium text-[#111827]">${escapeHtml(c.company)}</td>
      <td class="py-2 px-3 text-[#374151]">${escapeHtml(c.name)}</td>
      <td class="py-2 px-3 text-[#6B7280]">${escapeHtml(c.role)}</td>
      <td class="py-2 px-3">
        ${c.email ? `<button onclick="navigator.clipboard.writeText('${escapeHtml(c.email)}')" class="text-[#FF912B] hover:underline font-mono text-[11.5px] cursor-pointer">${escapeHtml(c.email)}</button>` : ''}
        ${c.phone ? `<div class="text-[11px] text-[#6B7280]">${escapeHtml(c.phone)}</div>` : ''}
      </td>
      <td class="py-2 px-3 text-[11px] text-[#6B7280]">${escapeHtml(c.source)}</td>
    </tr>
  `).join('');
}

// --- MODAL 6: TAREFAS DA SEMANA ---
function openTasksModal() {
  if (!STATE.dashboard) return;
  document.getElementById('modal-tasks').classList.remove('hidden');
  renderTasksModalList();
}

function renderTasksModalList() {
  const listEl = document.getElementById('tasks-modal-list');
  const tasks = STATE.dashboard?.current_week_tasks || [];
  listEl.innerHTML = tasks.map((t) => `
    <div onclick="toggleWeekTask('${t.id}')"
      class="p-3 rounded-xl bg-[#FBFBFD] hover:bg-white border border-[#E5E7EB] flex items-center justify-between gap-3 cursor-pointer transition">
      <div class="flex items-center gap-3 min-w-0">
        <input type="checkbox" ${t.completed ? 'checked' : ''} class="accent-[#FF912B] w-4 h-4 pointer-events-none" />
        <div class="min-w-0">
          <div class="text-[13px] font-medium ${t.completed ? 'line-through text-[#9CA3AF]' : 'text-[#111827]'} truncate">
            ${escapeHtml(t.title)}
          </div>
          <div class="text-[11px] text-[#6B7280]">${escapeHtml(t.client)} · ${escapeHtml(t.day_name)} (${escapeHtml(t.date)})</div>
        </div>
      </div>
      <span class="text-[10.5px] font-semibold px-2 py-0.5 rounded-md bg-[#FFF5EC] text-[#FF912B] flex-shrink-0">
        ${escapeHtml(t.category)}
      </span>
    </div>
  `).join('');
}

async function toggleWeekTask(taskId) {
  await fetch('/api/dashboard/toggle-task', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task_id: taskId })
  });
  await loadDashboard();
  renderTasksModalList();
}

// ============================================================================
// 7. INICIALIZAÇÃO DA APLICAÇÃO
// ============================================================================
window.addEventListener('DOMContentLoaded', async () => {
  await hydrateLucideIcons();
  await Promise.all([loadDashboard(), loadClientsList()]);
  await selectClient('Desentop_Ambiente');

  // Mensagem inicial limpa e orientada à ação
  appendChatMessage(
    'assistant',
    `### Bem-vindo ao BIZZ DEV AI (SKOLAE Formação)\n\n` +
    `O teu ambiente local está sincronizado com as **146 contas** em \`03_Carteira_Clientes/032_Clientes/\`, as bases de dados Excel em \`031_Bases_Dados/\` e a **Matriz Oficial TMB 25-26**.\n\n` +
    `- **Conta ativa selecionada:** **Desentop Ambiente** (*Patrícia Bicho* — Programa Master de Liderança Operacional p/ 8 líderes com Assessments Thomas PPA/HPTI/GIA + saldo FCT).\n` +
    `- **Ações Rápidas:** Usa a barra lateral para gerar um **Follow-up Fast-Track (35–55 palavras)**, desenhar o **Enquadramento de Proposta PPT (Slide 6)** ou **Auditar a Margem (≥ 65%)**.`,
    'Sistema Operacional Ativo'
  );
});
