import { formatDate } from './utils.js';
let chartInstance = null;
export function renderKpChart(eventos, canvasId = 'kpChart') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const sorted = [...eventos].sort((a, b) => new Date(a.startTime) - new Date(b.startTime));
    const labels = sorted.map(ev => formatDate(ev.startTime));
    const kpValues = sorted.map(ev => ev.kpIndex !== undefined ? ev.kpIndex : 0);
    if (chartInstance) chartInstance.destroy();
    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Índice Kp',
                data: kpValues,
                borderColor: '#22D3EE',
                backgroundColor: 'rgba(34, 211, 238, 0.1)',
                borderWidth: 2,
                pointBackgroundColor: '#8B5CF6',
                pointBorderColor: '#fff',
                pointRadius: 4,
                tension: 0.2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#e0e0e0' } } },
            scales: {
                x: { ticks: { color: '#a0aec0', maxTicksLimit: 10 } },
                y: { ticks: { color: '#a0aec0', stepSize: 1 }, min: 0 }
            }
        }
    });
}
