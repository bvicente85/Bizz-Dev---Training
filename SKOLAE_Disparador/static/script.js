const API_URL = 'http://localhost:5000/api';
let batchesData = [];
let currentCategory = 'Todas as Contas';

async function init(category = 'Todas as Contas') {
    try {
        currentCategory = category;
        const res = await fetch(`${API_URL}/campaigns/eligible?category=${encodeURIComponent(category)}`);
        const data = await res.json();
        
        document.getElementById('subtitle').innerText = 'Filtro Anti-Spam Ativo';
        
        // Setup Datalist for Themes
        const datalist = document.getElementById('theme-suggestions');
        if (datalist && datalist.childElementCount === 0) {
            data.past_themes.forEach(theme => {
                datalist.insertAdjacentHTML('beforeend', `<option value="${theme}">`);
            });
        }
        
        // Render Filter Pills
        const pillsContainer = document.getElementById('filter-pills');
        if (pillsContainer) {
            let pillsHtml = `<button class="filter-pill ${currentCategory === 'Todas as Contas' ? 'active' : ''}" onclick="init('Todas as Contas')">Todas as Contas</button>`;
            if (data.available_categories) {
                data.available_categories.forEach(cat => {
                    pillsHtml += `<button class="filter-pill ${currentCategory === cat ? 'active' : ''}" onclick="init('${cat}')">${cat}</button>`;
                });
            }
            pillsContainer.innerHTML = pillsHtml;
        }

        if (data.total_eligible === 0) {
            document.getElementById('batch-list').innerHTML = `
                <div class="empty-state glass">
                    <h2>Tudo Feito! 🎉</h2>
                    <p>Não há nenhum cliente pronto a ser contactado. Estão todos a descansar.</p>
                </div>
            `;
            return;
        }

        document.getElementById('status-bar').style.display = 'flex';
        document.getElementById('val-eligible').innerText = data.total_eligible;
        document.getElementById('val-batches').innerText = data.batches.length;
        document.getElementById('val-rest').innerText = data.rest_days;

        batchesData = data.batches;
        renderBatches();
    } catch (err) {
        console.error(err);
        document.getElementById('subtitle').innerText = 'Erro ao ligar ao Excel local.';
    }
}

function renderBatches() {
    const list = document.getElementById('batch-list');
    list.innerHTML = '';

    batchesData.forEach((batch, index) => {
        const batchIds = batch.map(c => c.id);
        const emailList = batch.map(c => c.Email).join('; ');
        
        const cardHtml = `
            <div class="batch-card glass" id="batch-card-${index}">
                <div class="batch-info">
                    <h3>Lote ${index + 1}</h3>
                    <p>${batch.length} destinatários (Prontos a enviar)</p>
                </div>
                <div class="batch-actions">
                    <button class="btn btn-primary" id="copy-btn-${index}" onclick="copyEmails(${index}, '${emailList}')">
                        Copiar BCC
                    </button>
                    <button class="btn btn-success" id="done-btn-${index}" onclick="markAsSent(${index}, ${JSON.stringify(batchIds)})" disabled>
                        Marcar como Enviado
                    </button>
                </div>
            </div>
        `;
        list.insertAdjacentHTML('beforeend', cardHtml);
    });
}

async function copyEmails(index, emails) {
    try {
        await navigator.clipboard.writeText(emails);
        const btn = document.getElementById(`copy-btn-${index}`);
        btn.innerText = 'Copiado! ✓';
        btn.style.background = '#4b5563'; 
        
        document.getElementById(`done-btn-${index}`).disabled = false;
        
        setTimeout(() => {
            btn.innerText = 'Copiar BCC';
            btn.style.background = '';
        }, 3000);
    } catch (err) {
        alert('Erro ao copiar. Tenta novamente.');
    }
}

async function markAsSent(index, contactIds) {
    const theme = document.getElementById('campaign-theme').value.trim();
    if (!theme) {
        alert('Atenção: Por favor escreve um "Tema da Campanha" no topo da página antes de marcares como enviado. Isto é vital para o teu histórico!');
        return;
    }

    const btn = document.getElementById(`done-btn-${index}`);
    btn.innerText = 'A gravar no Excel...';
    btn.disabled = true;
    document.getElementById(`copy-btn-${index}`).disabled = true;

    try {
        const res = await fetch(`${API_URL}/campaigns/mark_sent`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contact_ids: contactIds, tema: theme })
        });
        
        if (!res.ok) {
            throw new Error('Erro do servidor (possivelmente o Excel está aberto)');
        }
        
        // Remove the batch card
        const card = document.getElementById(`batch-card-${index}`);
        card.style.opacity = '0';
        setTimeout(() => {
            card.remove();
            
            // Refetch to cleanly update the batches and top counters
            init(currentCategory);
        }, 300);
        
    } catch (err) {
        alert('Erro ao gravar. Garante que os ficheiros Excel estão fechados.');
        btn.innerText = 'Marcar como Enviado';
        btn.disabled = false;
        document.getElementById(`copy-btn-${index}`).disabled = false;
    }
}

// Navigation and Dashboard Logic
let chartsLoaded = false;
let chart1, chart2, chart3, chart4;

async function switchTab(tab) {
    document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById(`view-${tab}`).classList.add('active');

    if (tab === 'disparador') {
        init(currentCategory);
    }
    
    if (tab === 'dashboard') {
        if (chart1) chart1.destroy();
        if (chart2) chart2.destroy();
        if (chart3) chart3.destroy();
        if (chart4) chart4.destroy();
        await loadDashboard();
    }
}

async function loadDashboard() {
    try {
        const res = await fetch(`${API_URL}/stats`);
        const data = await res.json();
        
        // Draw Timeline Chart
        const ctxTimeline = document.getElementById('timelineChart').getContext('2d');
        chart1 = new Chart(ctxTimeline, {
            type: 'bar',
            data: {
                labels: Object.keys(data.timeline),
                datasets: [{
                    label: 'Emails Enviados',
                    data: Object.values(data.timeline),
                    backgroundColor: '#3b82f6',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.1)' } },
                    x: { grid: { display: false } }
                }
            }
        });

        // Draw Theme Chart
        const ctxTheme = document.getElementById('themeChart').getContext('2d');
        chart2 = new Chart(ctxTheme, {
            type: 'doughnut',
            data: {
                labels: Object.keys(data.themes),
                datasets: [{
                    data: Object.values(data.themes),
                    backgroundColor: ['#3b82f6', '#a78bfa', '#10b981', '#f59e0b', '#ec4899'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right', labels: { color: '#94a3b8' } }
                }
            }
        });
        
        // Draw Roles Chart
        const ctxRoles = document.getElementById('rolesChart').getContext('2d');
        chart3 = new Chart(ctxRoles, {
            type: 'bar',
            data: {
                labels: Object.keys(data.roles || {}),
                datasets: [{
                    label: 'Envios',
                    data: Object.values(data.roles || {}),
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#94a3b8', stepSize: 1 } },
                    y: { ticks: { color: '#94a3b8' } }
                }
            }
        });
        
        // Draw Categories Chart
        const ctxCategories = document.getElementById('categoriesChart').getContext('2d');
        chart4 = new Chart(ctxCategories, {
            type: 'doughnut',
            data: {
                labels: Object.keys(data.categories || {}),
                datasets: [{
                    data: Object.values(data.categories || {}),
                    backgroundColor: ['#60a5fa', '#34d399', '#f472b6', '#fbbf24', '#a78bfa', '#94a3b8'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right', labels: { color: '#f8fafc' } }
                }
            }
        });

        // Agrupar por Mês
        const grouped = {};
        data.recent_history.forEach(row => {
            const month = row.Data.substring(0, 7); // YYYY-MM
            if (!grouped[month]) grouped[month] = [];
            grouped[month].push(row);
        });

        const accordion = document.getElementById('history-accordion');
        accordion.innerHTML = '';

        const monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];

        Object.keys(grouped).sort().reverse().forEach(monthStr => {
            const [year, monthNum] = monthStr.split('-');
            const monthName = monthNames[parseInt(monthNum) - 1] + ' ' + year;
            const rows = grouped[monthStr];
            
            let tbodyHtml = '';
            rows.forEach(row => {
                tbodyHtml += `
                    <tr>
                        <td>${row.Data}</td>
                        <td>${row.Tema}</td>
                        <td>${row.Nome}</td>
                        <td>${row.Empresa}</td>
                        <td>${row.Funcao || 'Desconhecido'}</td>
                        <td>${row.AccountType || 'Desconhecido'}</td>
                    </tr>
                `;
            });

            const details = `
                <details class="month-group">
                    <summary class="month-summary">${monthName} (${rows.length} envios)</summary>
                    <table>
                        <thead>
                            <tr>
                                <th>Data</th>
                                <th>Tema</th>
                                <th>Nome</th>
                                <th>Empresa</th>
                                <th>Função</th>
                                <th>Tipo de Conta</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${tbodyHtml}
                        </tbody>
                    </table>
                </details>
            `;
            accordion.insertAdjacentHTML('beforeend', details);
        });

    } catch (err) {
        console.error('Erro a carregar stats', err);
    }
}

document.addEventListener('DOMContentLoaded', () => init('Todas as Contas'));
