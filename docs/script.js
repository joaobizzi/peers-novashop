const C = { accent:'#e8f43a', teal:'#3af4c8', red:'#f43a7a', purple:'#b07af4', orange:'#f4943a', blue:'#3a94f4', bg:'#12141a', border:'#22263a', textDim:'#6b7299', text:'#f0f2ff' };
Chart.defaults.color = C.textDim;
Chart.defaults.font.family = "'DM Mono', monospace";
Chart.defaults.font.size = 11;

function baseOpts(extra={}) {
  return { responsive:true, maintainAspectRatio:false,
    plugins:{ legend:{ labels:{ color:C.textDim, boxWidth:12, padding:16 } },
      tooltip:{ backgroundColor:'#1a1d26', borderColor:C.border, borderWidth:1, titleColor:C.text, bodyColor:C.textDim, padding:12 }
    }, ...extra };
}

function showSection(id, btn) {
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
}

// ── DADOS REAIS DOS CSVs ──────────────────────────────────────────────────────
const statusLabels = ['Entregue','Cancelado','Em Trânsito','Devolvido'];
const statusValues = [9959, 2537, 1371, 1133];
const statusColors = [C.teal, C.red, C.accent, C.purple];

const meses = ['Jan/23','Fev/23','Mar/23','Abr/23','Mai/23','Jun/23','Jul/23','Ago/23','Set/23','Out/23','Nov/23','Dez/23',
               'Jan/24','Fev/24','Mar/24','Abr/24','Mai/24','Jun/24','Jul/24','Ago/24','Set/24','Out/24','Nov/24','Dez/24'];
const totalMes  = [525,492,613,564,579,531,542,584,527,554,2317,558,542,499,551,558,608,498,588,599,521,545,585,520];
const ativosMes = [405,387,453,421,434,406,410,435,397,419,1747,432,404,376,401,435,459,371,443,456,392,402,454,391];
const cancelMes = [120,105,160,143,145,125,132,149,130,135,570,126,138,123,150,123,149,127,145,143,129,143,131,129];
const ticketsSup= [73,118,159,133,168,157,138,160,151,156,375,391,133,127,117,137,183,149,142,158,174,127,154,220];

const produtos = [
  { nome:'Tênis Esportivo 78',       qtd:543, bruta:1640951, liq:769203 },
  { nome:'Equipamentos Academia 83', qtd:507, bruta:1641293, liq:465337 },
  { nome:'Roupas Íntimas 48',        qtd:507, bruta:1494540, liq:465082 },
  { nome:'Vitaminas 111',            qtd:505, bruta:1246078, liq:461646 },
  { nome:'Tênis Esportivo 77',       qtd:503, bruta:732724,  liq:226103 },
  { nome:'Cosméticos 92',            qtd:496, bruta:938608,  liq:333026 },
  { nome:'Suplementos 194',          qtd:496, bruta:420481,  liq:157179 },
  { nome:'Calças 33',                qtd:489, bruta:1031249, liq:207988 },
  { nome:'Notebooks 172',            qtd:488, bruta:1248619, liq:700908 },
  { nome:'Vitaminas 106',            qtd:487, bruta:1044277, liq:543110 },
];

const canais      = ['Paid Search','Indicação','Orgânico','Redes Sociais'];
const cancelCanal = [30.74, 12.38, 11.78, 11.67];
const ticketCanal = [11862, 11625, 11893, 11743];
const volCanal    = [3965, 3658, 3616, 3761];

// ── TABELA PRODUTOS ───────────────────────────────────────────────────────────
const tbody = document.getElementById('tabelaProdutos');
produtos.forEach((p,i) => {
  const m = ((p.liq/p.bruta)*100).toFixed(1);
  tbody.innerHTML += `<tr>
    <td style="color:var(--text-dim);font-family:'DM Mono',monospace">${i+1}</td>
    <td>${p.nome}</td>
    <td style="font-family:'DM Mono',monospace">${p.qtd.toLocaleString('pt-BR')}</td>
    <td style="font-family:'DM Mono',monospace">R$ ${p.bruta.toLocaleString('pt-BR')}</td>
    <td style="font-family:'DM Mono',monospace;color:var(--accent2)">R$ ${p.liq.toLocaleString('pt-BR')}</td>
    <td><span class="badge badge-green">${m}%</span></td>
  </tr>`;
});

// ── CHARTS ────────────────────────────────────────────────────────────────────
function mk(id, type, data, options) {
  const ctx = document.getElementById(id); if (!ctx) return;
  return new Chart(ctx, { type, data, options });
}

mk('chartOverviewStatus','doughnut',{
  labels:statusLabels, datasets:[{ data:statusValues, backgroundColor:statusColors, borderWidth:0, hoverOffset:8 }]
}, baseOpts({ cutout:'68%', plugins:{ legend:{ position:'right', labels:{ color:C.textDim, padding:14, boxWidth:10 } } } }));

mk('chartOverviewCanal','bar',{
  labels:canais, datasets:[{ label:'Total de Pedidos', data:volCanal, backgroundColor:[C.red,C.accent2,C.teal,C.accent], borderRadius:6, borderSkipped:false }]
}, baseOpts({ plugins:{ legend:{ display:false } }, scales:{ y:{ grid:{ color:C.border } }, x:{ grid:{ display:false } } } }));

mk('chartStatus','bar',{
  labels:statusLabels, datasets:[{ label:'Volume de Pedidos', data:statusValues, backgroundColor:statusColors, borderRadius:6, borderSkipped:false }]
}, baseOpts({ plugins:{ legend:{ display:false } }, scales:{ y:{ grid:{ color:C.border } }, x:{ grid:{ display:false } } } }));

mk('chartStatusPie','doughnut',{
  labels:statusLabels, datasets:[{ data:statusValues, backgroundColor:statusColors, borderWidth:0, hoverOffset:8 }]
}, baseOpts({ cutout:'60%', plugins:{ legend:{ position:'bottom', labels:{ color:C.textDim, padding:12, boxWidth:10 } } } }));

const dualCtx = document.getElementById('chartProdutosDual');
if (dualCtx) new Chart(dualCtx,{
  data:{ labels:produtos.map(p=>p.nome), datasets:[
    { type:'bar', label:'Qtd Vendida', data:produtos.map(p=>p.qtd), backgroundColor:'rgba(58,148,244,0.55)', borderRadius:4, yAxisID:'y' },
    { type:'line', label:'Receita Líquida (R$)', data:produtos.map(p=>p.liq), borderColor:C.teal, backgroundColor:'transparent', pointBackgroundColor:C.teal, pointRadius:5, borderWidth:2.5, yAxisID:'y2' }
  ]},
  options: baseOpts({ scales:{
    y:{ position:'left', grid:{ color:C.border } },
    y2:{ position:'right', grid:{ display:false }, ticks:{ color:C.teal, callback:v=>'R$'+v.toLocaleString('pt-BR') } },
    x:{ grid:{ display:false }, ticks:{ maxRotation:35 } }
  }})
});

mk('chartTicket','bar',{
  labels:['B2B','B2C'], datasets:[{ label:'Ticket Médio (R$)', data:[11880,11815], backgroundColor:[C.teal,C.red], borderRadius:8, borderSkipped:false }]
}, baseOpts({ plugins:{ legend:{ display:false } }, scales:{ y:{ grid:{ color:C.border }, min:11400, ticks:{ callback:v=>'R$'+v.toLocaleString('pt-BR') } }, x:{ grid:{ display:false } } } }));

mk('chartSegmentoPie','pie',{
  labels:['B2C (80,1%)','B2B (19,9%)'], datasets:[{ data:[9072,2258], backgroundColor:[C.teal,C.accent], borderWidth:0, hoverOffset:8 }]
}, baseOpts({ plugins:{ legend:{ position:'bottom', labels:{ color:C.textDim, padding:16 } } } }));

mk('chartTemporal','line',{
  labels:meses, datasets:[
    { label:'Total de Pedidos', data:totalMes, borderColor:'#27AE60', pointBackgroundColor:'#27AE60', borderWidth:3, pointRadius:3, fill:false },
    { label:'Ativos (Entregue/Trânsito)', data:ativosMes, borderColor:C.blue, pointBackgroundColor:C.blue, borderWidth:2, pointRadius:2, fill:false },
    { label:'Cancelados/Devolvidos', data:cancelMes, borderColor:C.red, pointBackgroundColor:C.red, borderWidth:2, pointRadius:2, fill:false },
  ]
}, baseOpts({ scales:{ y:{ grid:{ color:C.border } }, x:{ grid:{ color:C.border }, ticks:{ maxRotation:45 } } } }));

mk('chartTicketsSuporte','bar',{
  labels:meses, datasets:[{ label:'Tickets de Suporte', data:ticketsSup, backgroundColor:'rgba(244,148,58,0.7)', borderRadius:3 }]
}, baseOpts({ plugins:{ legend:{ display:false } }, scales:{ y:{ grid:{ color:C.border } }, x:{ grid:{ display:false }, ticks:{ maxRotation:45 } } } }));

mk('chartCancelCanal','bar',{
  labels:canais, datasets:[{ label:'Taxa de Cancelamento (%)', data:cancelCanal, backgroundColor:cancelCanal.map(v=>v>25?C.red:v>15?C.orange:C.teal), borderRadius:6, borderSkipped:false }]
}, baseOpts({ indexAxis:'y', plugins:{ legend:{ display:false } }, scales:{ x:{ grid:{ color:C.border }, ticks:{ callback:v=>v+'%' } }, y:{ grid:{ display:false } } } }));

mk('chartTicketCanal','bar',{
  labels:canais, datasets:[{ label:'Ticket Médio (R$)', data:ticketCanal, backgroundColor:[C.red,C.accent2,C.teal,C.accent], borderRadius:6, borderSkipped:false }]
}, baseOpts({ indexAxis:'y', plugins:{ legend:{ display:false } }, scales:{ x:{ grid:{ color:C.border }, min:11400, ticks:{ callback:v=>'R$'+v.toLocaleString('pt-BR') } }, y:{ grid:{ display:false } } } }));
