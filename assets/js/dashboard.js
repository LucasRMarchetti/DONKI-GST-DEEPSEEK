import { escapeHtml, formatDate, nowFormatted } from './utils.js';
import { renderKpChart } from './charts.js';

let eventos = [];
let ultimaAtualizacao = null;

const totalEventsEl = document.getElementById('totalEvents');
const kpMaxEl = document.getElementById('kpMax');
const kpMediaEl = document.getElementById('kpMedia');
const ultimaAtualizacaoEl = document.getElementById('ultimaAtualizacao');
const tableBody = document.getElementById('tableBody');
const timelineContainer = document.getElementById('timelineContainer');
const lastUpdateLabel = document.getElementById('lastUpdateLabel');
const refreshBtn = document.getElementById('refreshBtn');

async function loadData() {
    try {
        let response = await fetch('data/gst_latest.json');
        if (!response.ok) response = await fetch('data/sample_gst.json');
        if (!response.ok) throw new Error('Não foi possível carregar os dados.');
        const data = await response.json();
        if (!Array.isArray(data)) throw new Error('Dados inválidos.');
        eventos = data;
        ultimaAtualizacao = new Date();
        return true;
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        try {
            const resp = await fetch('data/sample_gst.json');
            if (resp.ok) {
                const data = await resp.json();
                eventos = data;
                ultimaAtualizacao = new Date();
                return true;
            }
        } catch (e) { console.error('Falha total:', e); }
        return false;
    }
}

function updateDashboard() {
    if (!eventos || eventos.length === 0) {
        totalEventsEl.textContent = '0';
        kpMaxEl.textContent = '-';
        kpMediaEl.textContent = '-';
        ultimaAtualizacaoEl.textContent = nowFormatted();
        tableBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Nenhum evento disponível.</td></tr>';
        timelineContainer.innerHTML = '<p style="text-align:center;color:#a0aec0;">Sem eventos para exibir.</p>';
        lastUpdateLabel.textContent = 'Última atualização: ' + nowFormatted();
        return;
    }
    const total = eventos.length;
    const kpValues = eventos.map(ev => ev.kpIndex).filter(v => v !== undefined && v !== null);
    const kpMax = kpValues.length ? Math.max(...kpValues) : 0;
    const kpMedia = kpValues.length ? (kpValues.reduce((a,b) => a+b, 0) / kpValues.length) : 0;
    totalEventsEl.textContent = total;
    kpMaxEl.textContent = kpMax.toFixed(1);
    kpMediaEl.textContent = kpMedia.toFixed(1);
    ultimaAtualizacaoEl.textContent = nowFormatted();
    let tableHtml = '';
    eventos.forEach(ev => {
        const id = escapeHtml(ev.gstID || '-');
        const start = escapeHtml(formatDate(ev.startTime));
        const kp = ev.kpIndex !== undefined ? escapeHtml(ev.kpIndex.toFixed(1)) : '-';
        const source = escapeHtml(ev.source || '-');
        tableHtml += `<tr><td>${id}</td><td>${start}</td><td>${kp}</td><td>${source}</td></tr>`;
    });
    tableBody.innerHTML = tableHtml;
    let timelineHtml = '';
    const sorted = [...eventos].sort((a,b) => new Date(b.startTime) - new Date(a.startTime));
    sorted.slice(0, 20).forEach(ev => {
        const time = escapeHtml(formatDate(ev.startTime));
        const kp = ev.kpIndex !== undefined ? escapeHtml(ev.kpIndex.toFixed(1)) : '-';
        const source = escapeHtml(ev.source || '-');
        timelineHtml += `<div class="timeline-item"><span class="time">${time}</span><span class="kp">Kp ${kp}</span><span class="source">${source}</span></div>`;
    });
    timelineContainer.innerHTML = timelineHtml;
    renderKpChart(eventos);
    lastUpdateLabel.textContent = 'Última atualização: ' + nowFormatted();
}

async function init() {
    const success = await loadData();
    if (!success) {
        document.querySelector('.dashboard').innerHTML = '<div style="text-align:center;padding:3rem;color:#ff6b6b;"><h2>Erro ao carregar dados</h2><p>Verifique a conexão com a internet e tente novamente.</p></div>';
        return;
    }
    updateDashboard();
    refreshBtn.addEventListener('click', async () => {
        refreshBtn.textContent = 'Carregando...';
        refreshBtn.disabled = true;
        const ok = await loadData();
        if (ok) updateDashboard();
        else alert('Não foi possível atualizar. Verifique sua conexão.');
        refreshBtn.textContent = 'Atualizar Dados';
        refreshBtn.disabled = false;
    });
}

document.addEventListener('DOMContentLoaded', init);
