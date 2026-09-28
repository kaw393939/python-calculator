'use strict';
const $ = id => document.getElementById(id);
let operations = [], records = [], mode = 'guided', category = 'all', latest = null, busy = false;
const arithmetic = ['add','subtract','multiply','divide'];
const statistics = ['mean','median','stddev'];
const fmt = n => Number(n).toLocaleString(undefined, {maximumSignificantDigits:12});
function notice(message='') { $('notice').textContent=message; $('notice').hidden=!message; }
async function api(path, options={}) {
  const response = await fetch(path, {headers:{'Content-Type':'application/json'}, ...options});
  if (!response.ok) {
    let body; try {body=await response.json();} catch {throw new Error('The server could not complete that request. Please try again.');}
    throw new Error(typeof body.detail==='string' ? body.detail : 'Check your input and try again.');
  }
  return response.status===204 ? null : response.json();
}
function expression(record) {return [record.operation,...record.args,...record.options.map(([key,value])=>`${key}=${value}`)].join(' ');}
function showResult(record) {
  latest=record;
  $('result-value').textContent=record?fmt(record.result):'Ready when you are.';
  $('result-value').classList.toggle('has-result',!!record);
  $('result-expression').textContent=record?expression(record):'Choose an operation and add your numbers to begin.';
  $('result-status').textContent=record?'Saved to your notebook':'Successful calculations are saved automatically';
  $('copy-result').disabled=!record;
  $('insert-answer').disabled=!records.length;
}
function setMode(value) {
  mode=value;
  for(const name of ['guided','command']) {
    $(name+'-mode').classList.toggle('selected',name===mode);
    $(name+'-mode').setAttribute('aria-pressed',String(name===mode));
    $(name+'-fields').hidden=name!==mode;
  }
  $('operands').required=mode==='guided'; $('operation').required=mode==='guided';
  $('command-input').required=mode==='command';
}
function updateHelp() {
  const operation=operations.find(op=>op.name===$('operation').value);
  $('operation-help').textContent=operation?`${operation.description} · ${operation.usage}`:'No plugins installed yet. Choose All operations to continue.';
  $('deviation-field').hidden=operation?.name!=='stddev';
  $('calculate').disabled=busy || (mode==='guided'&&!operation);
}
function populateOperations() {
  const current=$('operation').value;
  $('operation').replaceChildren();
  for(const op of operations.filter(op=>category==='all'||(category==='arithmetic'?arithmetic.includes(op.name):category==='statistics'?statistics.includes(op.name):!arithmetic.includes(op.name)&&!statistics.includes(op.name)))) {
    const option=document.createElement('option');option.value=op.name;option.textContent=op.name[0].toUpperCase()+op.name.slice(1)+' — '+op.description;$('operation').append(option);
  }
  if([...$('operation').options].some(op=>op.value===current)) $('operation').value=current;
  updateHelp();
}
function element(tag, className, text) {const node=document.createElement(tag);node.className=className;node.textContent=text;return node;}
function action(text, label, fn) {const button=element('button','',text);button.type='button';button.setAttribute('aria-label',label);button.addEventListener('click',()=>perform(fn));return button;}
async function perform(fn) {if(busy)return;busy=true;$('calculate').disabled=true;notice();try{await fn();}catch(error){notice(error.message);}finally{busy=false;updateHelp();}}
function renderHistory() {
  $('history-count').textContent=records.length;
  $('clear-history').disabled=!records.length;
  const query=$('history-search').value.toLowerCase();
  const filtered=records.filter(record=>(expression(record)+' '+record.result).toLowerCase().includes(query));
  const list=$('history-list');list.replaceChildren();
  if(!filtered.length) {
    const empty=element('div','empty-state','');empty.append(element('span','','↺'),element('h3','',records.length?'No matches.':'A fresh page.'),element('p','',records.length?'Try another operation or number.':'Your calculations will appear here. Come back to any result, anytime.'));list.append(empty);return;
  }
  for(const record of filtered) {
    const item=element('article','history-item','');const head=element('div','history-item-head','');
    head.append(element('span','history-op',record.operation),element('time','history-time',new Date(record.timestamp).toLocaleString(undefined,{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'})));
    item.append(head,element('p','history-expression',expression(record)),element('div','history-result',fmt(record.result)));
    const actions=element('div','record-actions','');
    actions.append(action('Reuse ↗',`Reuse ${record.operation} result ${record.result}`,()=>{$('operands').value=String(record.result);category='all';setCategory('all');setMode('guided');$('operands').focus();}),
      action('Details',`Details for ${record.operation} result ${record.result}`,()=>{$('record-details').textContent=`ID: ${record.id}\nUTC: ${record.timestamp}\n\n${expression(record)}\n\nFull precision result: ${record.result}`;$('record-dialog').showModal();}),
      action('Delete',`Delete ${record.operation} result ${record.result}`,async()=>{await api('/api/history/'+record.id,{method:'DELETE'});await loadHistory();}));
    item.append(actions);list.append(item);
  }
}
async function loadHistory(){const body=await api('/api/history');records=body.records;renderHistory();showResult(records[0]||null);}
function setCategory(value){category=value;document.querySelectorAll('[data-category]').forEach(button=>{button.classList.toggle('selected',button.dataset.category===value);button.setAttribute('aria-pressed',String(button.dataset.category===value));});populateOperations();}
$('calculation-form').addEventListener('submit',event=>{event.preventDefault();perform(async()=>{
  let command=$('command-input').value.trim();
  if(mode==='guided') {
    let options=$('options').value.trim();
    if($('operation').value==='stddev'&&!/(^|\s)ddof=/.test(options)) options+=` ddof=${$('deviation').value}`;
    command=[$('operation').value,$('operands').value.trim(),options].join(' ');
  }
  await api('/api/calculations',{method:'POST',body:JSON.stringify({command})});
  await loadHistory();
});});
$('guided-mode').onclick=()=>{setMode('guided');updateHelp();};$('command-mode').onclick=()=>{setMode('command');updateHelp();$('command-input').focus();};
$('operation').onchange=()=>{$('options').value='';updateHelp();};
document.querySelectorAll('[data-category]').forEach(button=>button.onclick=()=>setCategory(button.dataset.category));
document.querySelectorAll('[data-example]').forEach(button=>button.onclick=()=>{setCategory('all');setMode('guided');$('operation').value=button.dataset.example;$('options').value='';$('operands').value=button.dataset.example==='add'?'18.50 24 12.75':'2 4 4 4 5 5 7 9';$('deviation').value='0';updateHelp();$('operands').focus();});
$('insert-answer').onclick=()=>{$('operands').value=($('operands').value.trim()+' ans').trim();$('operands').focus();};
$('copy-result').onclick=()=>perform(async()=>{await navigator.clipboard.writeText(String(latest.result));$('copy-result').textContent='Copied ✓';setTimeout(()=>$('copy-result').textContent='Copy ↗',1500);});
$('history-search').oninput=renderHistory;$('refresh').onclick=()=>perform(loadHistory);
$('clear-history').onclick=()=>{$('confirm-message').textContent=`This will delete all ${records.length} saved calculations.`;$('confirm-dialog').showModal();};
$('cancel-clear').onclick=()=>$('confirm-dialog').close();$('confirm-clear').onclick=()=>perform(async()=>{await api('/api/history?confirm=true',{method:'DELETE'});$('confirm-dialog').close();await loadHistory();});
$('close-details').onclick=()=>$('record-dialog').close();
document.addEventListener('keydown',event=>{if((event.ctrlKey||event.metaKey)&&event.key==='Enter'){event.preventDefault();$('calculation-form').requestSubmit();}});
perform(async()=>{const body=await api('/api/operations');operations=body.operations;populateOperations();$('plugin-count').textContent=`${operations.length} operations · Ready to extend`;$('command-reference').textContent=operations.map(op=>op.usage).join('\n');await loadHistory();if(body.warnings.length)notice(body.warnings.join(' '));});
