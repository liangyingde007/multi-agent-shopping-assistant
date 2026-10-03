'use strict';
const form = document.querySelector('#shopping-form');
const category = document.querySelector('#category');
const query = document.querySelector('#query');
const budget = document.querySelector('#budget');
const priorities = document.querySelector('#priorities');
const status = document.querySelector('#status');
const submit = document.querySelector('#submit');
const panel = document.querySelector('.result-panel');
const results = document.querySelector('#results');
const meta = document.querySelector('#result-meta');
const labels = {camera:'拍照',performance:'性能',battery:'续航',portable:'便携',value:'性价比',office:'办公',gaming:'游戏',audio:'音质',noise:'降噪'};
const available = {phone:['camera','performance','battery','portable','value','gaming'],laptop:['performance','portable','office','gaming','battery','value'],headphones:['audio','noise','battery','portable','value']};
const examples = {
  camera:{query:'预算4000元，想买拍照好、续航不错的手机。',budget:4000,category:'phone',priorities:['camera','battery']},
  work:{query:'预算6000元，想买用于编程开发和办公的笔记本。',budget:6000,category:'laptop',priorities:['performance','office']},
  audio:{query:'预算800元，想买通勤用的耳机，比较重视降噪。',budget:800,category:'headphones',priorities:['noise','portable']}
};
let busy = false;
function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function showPriorities(selected = []) {
  priorities.replaceChildren();
  for (const key of available[category.value]) {
    const label = element('label');
    const input = element('input');
    input.type = 'checkbox'; input.name = 'priorities'; input.value = key; input.checked = selected.includes(key);
    label.append(input, element('span', '', labels[key])); priorities.append(label);
  }
}
category.addEventListener('change', () => showPriorities());
showPriorities();
function graphic(product) {
  const box = element('div', 'product-visual');
  box.setAttribute('aria-hidden', 'true');
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 100 100');
  const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
  use.setAttribute('href', '/assets/icons.svg#' + product.category);
  svg.append(use); box.append(svg); return box;
}
function productCard(product, featured) {
  const card = element('article', 'product-card' + (featured ? ' featured' : ''));
  const body = element('div');
  body.append(element('p', 'product-label', featured ? '优先推荐 / FIRST CHOICE' : '备选方案'));
  body.append(element('h3', '', product.name));
  const price = element('p', 'product-price', '¥ ' + product.price.toLocaleString('zh-CN'));
  price.append(element('small', '', '示例价格')); body.append(price);
  body.append(element('p', 'product-feature', product.feature));
  const reasons = element('ul', 'product-reasons');
  product.reasons.forEach(reason => reasons.append(element('li', '', reason)));
  body.append(reasons); card.append(graphic(product), body); return card;
}
function comparison(products, task) {
  const container = element('div');
  container.append(element('h3', 'compare-title', '放在一起，比一比'));
  const wrap = element('div', 'table-wrap');
  wrap.tabIndex = 0; wrap.setAttribute('role','region'); wrap.setAttribute('aria-label','示例商品比较表，可横向滚动');
  const table = element('table');
  const head = element('thead'); const header = element('tr');
  const nameCell = element('th', '', '比较项'); nameCell.scope='col'; header.append(nameCell);
  products.forEach(product => { const cell=element('th','',product.name); cell.scope='col'; header.append(cell); });
  head.append(header); table.append(head);
  const body = element('tbody');
  const rows = [['示例价格',product=>'¥ '+product.price.toLocaleString('zh-CN')], ...task.priorities.map(key=>[labels[key],product=>product.ratings[key]===undefined?'未设置':product.ratings[key]+'/5']), ['偏好评分',product=>product.score+'/100']];
  rows.forEach(([label,getValue])=>{ const row=element('tr'); const cell=element('th','',label); cell.scope='row'; row.append(cell); products.forEach(product=>row.append(element('td','',getValue(product)))); body.append(row); });
  table.append(body); wrap.append(table); container.append(wrap); return container;
}
function render(answer) {
  const task=answer.task;
  const content=element('div');
  const summary=element('div','result-summary');
  summary.append(element('span','',task.category_label || '待选择品类'),element('span','',task.budget===null?'预算未限定':'预算 ¥ '+task.budget.toLocaleString('zh-CN')),element('span','',task.priority_labels.join(' / ')));
  content.append(summary,element('p','result-caption',answer.message));
  if(answer.recommendation) {
    const products=[answer.recommendation,...answer.alternatives];
    const grid=element('div','product-grid'); products.forEach((product,i)=>grid.append(productCard(product,i===0))); content.append(grid,comparison(products,task));
  } else {
    const empty=element('div','no-results'); empty.append(element('h3','',task.needs_clarification?'先告诉我想选什么':'暂时没有匹配的商品'),element('p','',task.needs_clarification?answer.message:'没有用超出预算的商品替代推荐。调整预算或品类后，可以重新比较。')); content.append(empty);
  }
  const details=element('details','trace'); details.append(element('summary','','查看这次推荐的处理过程'));
  const list=element('ol'); answer.trace.forEach((step,i)=>{ const item=element('li'); const text=element('div'); text.append(element('h4','',step.label+' · '+step.role),element('p','',step.detail)); item.append(element('span','step',String(i+1).padStart(2,'0')),text); list.append(item); }); details.append(list); content.append(details);
  results.replaceChildren(content); meta.textContent=answer.matched_count+' 个匹配候选';
}
function setBusy(value) {
  busy=value; submit.disabled=value; panel.setAttribute('aria-busy',String(value));
  document.querySelectorAll('[data-example]').forEach(button=>button.disabled=value);
  submit.firstChild.textContent=value?'正在比较… ':'帮我选一选 ';
}
async function run() {
  if(busy || !form.reportValidity()) return;
  const payload={query:query.value.trim(),category:category.value,priorities:[...form.querySelectorAll('[name="priorities"]:checked')].map(input=>input.value)};
  if(!payload.query){ status.textContent='请写下你的使用场景。'; status.className='status error'; query.focus(); return; }
  if(budget.value!=='') payload.budget=Number(budget.value);
  status.className='status'; status.textContent='正在筛选和比较示例商品…'; setBusy(true);
  const controller=new AbortController(); const timer=setTimeout(()=>controller.abort(),20000);
  try {
    const response=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),signal:controller.signal});
    if(!response.ok) throw new Error(response.status===422?'输入未通过校验，请检查预算和需求。':'服务暂时不可用，请稍后重试。');
    const data=await response.json(); render(data.answer); status.textContent=data.answer.recommendation?'已完成比较，可查看推荐结果。':'已完成筛选，暂无匹配商品。';
    if(window.matchMedia('(max-width:700px)').matches) panel.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'start'});
  } catch(error) {
    status.className='status error'; status.textContent=error.name==='AbortError'?'请求超时，请稍后重试。':error instanceof TypeError?'连接失败，请检查网络后重试。':error.message;
  } finally { clearTimeout(timer); setBusy(false); }
}
form.addEventListener('submit',event=>{event.preventDefault();run();});
document.querySelectorAll('[data-example]').forEach(button=>button.addEventListener('click',()=>{const example=examples[button.dataset.example];query.value=example.query;budget.value=example.budget;category.value=example.category;showPriorities(example.priorities);run();}));
