#!/usr/bin/env python3
"""Rewrite task UI to Todoist-like quick-add + memo focus."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.js"
HTML = ROOT / "index.html"
CSS = ROOT / "styles.css"

# ---------- index.html ----------
html = HTML.read_text(encoding="utf-8")

old_task_section = (
    '        <section id="screen-tasks" class="screen">\n'
    '          <div class="screen-header">\n'
    '            <h2>タスク</h2>\n'
    '            <p>Todoist風の一覧で素早く確認・完了</p>\n'
    '          </div>\n'
    '          <article class="panel mobile-panel">\n'
    '            <div class="panel-header">\n'
    '              <h3>タスク一覧</h3>\n'
    '              <div class="panel-header-actions">\n'
    '                <span class="pill" id="taskCountPill"></span>\n'
    '                <button type="button" class="primary-btn small" onclick="openTaskEditor()">＋ 新規</button>\n'
    '              </div>\n'
    '            </div>\n'
    '            <div id="taskList" class="stack todoist-task-list"></div>\n'
    '          </article>\n'
    '        </section>\n'
)

new_task_section = (
    '        <section id="screen-tasks" class="screen">\n'
    '          <div class="screen-header">\n'
    '            <h2>タスク</h2>\n'
    '            <p>Todoist風の一覧＋メモとして使える詳細</p>\n'
    '          </div>\n'
    '          <article class="panel mobile-panel tasks-panel">\n'
    '            <div class="panel-header">\n'
    '              <h3>タスク一覧</h3>\n'
    '              <div class="panel-header-actions">\n'
    '                <span class="pill" id="taskCountPill"></span>\n'
    '                <button type="button" class="primary-btn small" id="quickTaskToggleBtn" onclick="toggleQuickTaskBar()">＋ 新規</button>\n'
    '              </div>\n'
    '            </div>\n'
    '            <div id="quickTaskBar" class="quick-task-bar hidden">\n'
    '              <div class="quick-task-input-wrap">\n'
    '                <button type="button" class="quick-task-check" aria-hidden="true">＋</button>\n'
    '                <input type="text" id="quickTaskInput" class="quick-task-input" placeholder="タスクを入力 (例: 山田様へ資料送付 明日 15:00 !1 #山田様 @港区マンション G)" autocomplete="off" />\n'
    '              </div>\n'
    '              <div class="quick-task-hint">\n'
    '                <span>Enter追加 / Esc閉じる</span>\n'
    '                <span>期限: today / 明日 / 月曜 / 7/30 / 7/30 15:00</span>\n'
    '                <span>優先度: !1 !2 !3</span>\n'
    '                <span>顧客: #名前</span>\n'
    '                <span>物件: @名称</span>\n'
    '              </div>\n'
    '            </div>\n'
    '            <div id="taskList" class="stack todoist-task-list"></div>\n'
    '          </article>\n'
    '        </section>\n'
)
assert old_task_section in html, "task section not found"
html = html.replace(old_task_section, new_task_section)

# Task edit screen: enlarge memo, add "memo mode" priority reorder
old_edit_form = (
    '            <form id="taskEditForm" class="form compact-form">\n'
    '              <input type="hidden" name="id" id="taskEditId" value="" />\n'
    '              <label><span>タイトル</span><input name="title" id="taskEditTitleInput" placeholder="例: 比較資料送付" /></label>\n'
)
new_edit_form = (
    '            <form id="taskEditForm" class="form compact-form task-edit-form">\n'
    '              <input type="hidden" name="id" id="taskEditId" value="" />\n'
    '              <label class="task-title-label"><span>タイトル</span><input name="title" id="taskEditTitleInput" placeholder="例: 比較資料送付" /></label>\n'
)
assert old_edit_form in html, "edit form head not found"
html = html.replace(old_edit_form, new_edit_form)

old_memo_label = (
    '              <label><span>メモ</span><textarea name="memo" id="taskEditMemo" placeholder="備考・次のアクションなど"></textarea></label>\n'
)
new_memo_label = (
    '              <label class="task-memo-label"><span>メモ</span><textarea name="memo" id="taskEditMemo" class="task-memo-area" rows="10" placeholder="メモとして自由に書けます。改行そのまま保存されます。&#10;・箇条書き&#10;・電話メモ&#10;・関連URLなど"></textarea></label>\n'
)
assert old_memo_label in html, "memo label not found"
html = html.replace(old_memo_label, new_memo_label)

# cache bust
html = html.replace('./styles.css?v=17', './styles.css?v=18')
html = html.replace('./app.js?v=17', './app.js?v=18')

HTML.write_text(html, encoding="utf-8")

# ---------- app.js ----------
app = APP.read_text(encoding="utf-8")

# 1) Update renderTaskCard to Todoist-like layout with memo preview and due-first badge
old_card = '''function renderTaskCard(task, options = {}) {
  const { compact = false } = options;
  const customer = getCustomer(task.customerId);
  const property = getProperty(task.propertyId);
  const due = escapeHtml(task.due || '-');
  const title = escapeHtml(task.title || 'タスク');
  const customerName = escapeHtml(customer?.name || '顧客未設定');
  const propertyName = escapeHtml(property?.title || '物件未設定');
  const statusText = escapeHtml(taskStatusLabel(task.status));
  const priorityText = escapeHtml(taskPriorityLabel(task.priority));
  const assignee = escapeHtml(task.assignedTo || state.session?.name || '担当未設定');
  const dealChip = property ? `<span class="todo-chip ${property.dealType}">${dealTypeLabel(property.dealType)}</span>` : '';
  return `
    <article class="todo-task ${compact ? 'compact' : ''} priority-${task.priority || 'medium'} status-${task.status || 'todo'} ${task.status === 'done' ? 'is-done' : ''}" onclick="openTaskEditor('${task.id}')">
      <button type="button" class="todo-check ${task.status === 'done' ? 'checked' : ''}" aria-label="${task.status === 'done' ? '未完了へ戻す' : '完了にする'}" onclick="toggleTaskDone(event, '${task.id}')">
        <span>${task.status === 'done' ? '✓' : ''}</span>
      </button>
      <div class="todo-main">
        <div class="todo-title-row">
          <div class="todo-title">${title}</div>
          <div class="todo-priority-badge priority-${task.priority || 'medium'}">${taskPriorityShort(task.priority)}</div>
        </div>
        <div class="todo-meta-row">
          <span class="todo-date">${due}</span>
          <span class="todo-dot">•</span>
          <span>${statusText}</span>
          <span class="todo-dot">•</span>
          <span>${priorityText}</span>
        </div>
        <div class="todo-context-row">
          <span>${customerName}</span>
          <span class="todo-dot">/</span>
          <span>${propertyName}</span>
        </div>
        <div class="todo-tags-row">
          <span class="todo-chip">担当 ${assignee}</span>
          ${dealChip}
        </div>
      </div>
      <div class="todo-arrow">›</div>
    </article>
  `;
}'''

new_card = '''function renderTaskCard(task, options = {}) {
  const { compact = false } = options;
  const customer = getCustomer(task.customerId);
  const property = getProperty(task.propertyId);
  const dueRaw = task.due || '';
  const dueClass = dueBadgeClass(dueRaw);
  const dueLabel = dueRaw ? escapeHtml(formatDueShort(dueRaw)) : '';
  const title = escapeHtml(task.title || '(無題)');
  const memoRaw = String(task.memo || '').trim();
  const memoPreview = memoRaw ? escapeHtml(memoRaw.split(/\\r?\\n/)[0].slice(0, 80)) : '';
  const priorityKey = task.priority || 'medium';
  const priorityBadge = `<span class="todo-priority-badge priority-${priorityKey}">${taskPriorityShort(priorityKey)}</span>`;
  const dueBadge = dueLabel ? `<span class="todo-due-badge ${dueClass}">${dueLabel}</span>` : '';
  const customerChip = customer ? `<span class="todo-chip cust">#${escapeHtml(customer.name)}</span>` : '';
  const propertyChip = property ? `<span class="todo-chip ${property.dealType}">@${escapeHtml(property.title)}</span>` : '';
  const isDone = task.status === 'done';
  return `
    <article class="todo-task ${compact ? 'compact' : ''} priority-${priorityKey} status-${task.status || 'todo'} ${isDone ? 'is-done' : ''}" onclick="openTaskEditor('${task.id}')">
      <button type="button" class="todo-check ${isDone ? 'checked' : ''}" aria-label="${isDone ? '未完了へ戻す' : '完了にする'}" onclick="toggleTaskDone(event, '${task.id}')">
        <span>${isDone ? '✓' : ''}</span>
      </button>
      <div class="todo-main">
        <div class="todo-title-row">
          <div class="todo-title">${title}</div>
          ${priorityBadge}
        </div>
        ${memoPreview ? `<div class="todo-memo-preview">${memoPreview}</div>` : ''}
        <div class="todo-badge-row">
          ${dueBadge}
          ${customerChip}
          ${propertyChip}
        </div>
      </div>
    </article>
  `;
}

function formatDueShort(due) {
  const d = parseWhen(due);
  if (!d) return due;
  const now = new Date();
  const today0 = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const target0 = new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const diffDays = Math.round((target0 - today0) / 86400000);
  const hh = String(d.getHours()).padStart(2, '0');
  const mm = String(d.getMinutes()).padStart(2, '0');
  const hasTime = /\\d{1,2}:\\d{2}/.test(String(due));
  const timePart = hasTime ? ` ${hh}:${mm}` : '';
  if (diffDays === 0) return `今日${timePart}`;
  if (diffDays === 1) return `明日${timePart}`;
  if (diffDays === -1) return `昨日${timePart}`;
  if (diffDays > 1 && diffDays < 7) {
    const dow = ['日','月','火','水','木','金','土'][d.getDay()];
    return `${dow}${timePart}`;
  }
  return `${d.getMonth()+1}/${d.getDate()}${timePart}`;
}

function dueBadgeClass(due) {
  const d = parseWhen(due);
  if (!d) return '';
  const now = new Date();
  const today0 = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const target0 = new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const diffDays = Math.round((target0 - today0) / 86400000);
  if (diffDays < 0) return 'overdue';
  if (diffDays === 0) return 'today';
  if (diffDays === 1) return 'tomorrow';
  if (diffDays < 7) return 'soon';
  return 'later';
}'''
assert old_card in app, "renderTaskCard not found"
app = app.replace(old_card, new_card)

# 2) Change task view sort: due-first (near future first), done pushed down
old_sort = '''function sortTasksForView(tasks) {
  const priorityScore = { high: 0, medium: 1, low: 2 };
  const statusScore = { doing: 0, todo: 1, hold: 2, returned: 3, done: 4 };
  return [...tasks].sort((a, b) => {
    const doneGap = (a.status === 'done') - (b.status === 'done');
    if (doneGap) return doneGap;
    const statusGap = (statusScore[a.status] ?? 9) - (statusScore[b.status] ?? 9);
    if (statusGap) return statusGap;
    const priorityGap = (priorityScore[a.priority] ?? 9) - (priorityScore[b.priority] ?? 9);
    if (priorityGap) return priorityGap;
    const ad = parseWhen(a.due);
    const bd = parseWhen(b.due);
    if (ad && bd) return ad - bd;
    return String(a.title || '').localeCompare(String(b.title || ''), 'ja');
  });
}'''

new_sort = '''function sortTasksForView(tasks) {
  const priorityScore = { high: 0, medium: 1, low: 2 };
  const FAR = 8640000000000000;
  return [...tasks].sort((a, b) => {
    const doneGap = (a.status === 'done') - (b.status === 'done');
    if (doneGap) return doneGap;
    const ad = parseWhen(a.due);
    const bd = parseWhen(b.due);
    const at = ad ? ad.getTime() : FAR;
    const bt = bd ? bd.getTime() : FAR;
    if (at !== bt) return at - bt;
    const priorityGap = (priorityScore[a.priority] ?? 9) - (priorityScore[b.priority] ?? 9);
    if (priorityGap) return priorityGap;
    return String(a.title || '').localeCompare(String(b.title || ''), 'ja');
  });
}'''
assert old_sort in app, "sortTasksForView not found"
app = app.replace(old_sort, new_sort)

# 3) Define renderTasks (it currently doesn't exist)
render_tasks_impl = '''
function renderTasks() {
  const pill = document.getElementById('taskCountPill');
  if (pill) {
    const openCount = state.tasks.filter((t) => t.status !== 'done').length;
    pill.textContent = `${openCount}件未完了 / 全${state.tasks.length}件`;
  }
  const list = document.getElementById('taskList');
  if (!list) return;
  const sorted = sortTasksForView(state.tasks);
  list.innerHTML = sorted.length
    ? sorted.map((t) => renderTaskCard(t)).join('')
    : '<div class="empty-state">タスクはありません。＋ 新規から追加できます。</div>';
}
window.renderTasks = renderTasks;

function toggleQuickTaskBar(forceOpen) {
  const bar = document.getElementById('quickTaskBar');
  if (!bar) return;
  const willOpen = typeof forceOpen === 'boolean' ? forceOpen : bar.classList.contains('hidden');
  bar.classList.toggle('hidden', !willOpen);
  if (willOpen) {
    const input = document.getElementById('quickTaskInput');
    if (input) {
      input.value = '';
      setTimeout(() => input.focus(), 30);
    }
  }
}
window.toggleQuickTaskBar = toggleQuickTaskBar;

function parseQuickTaskInput(raw) {
  let text = String(raw || '').trim();
  if (!text) return null;
  let priority = 'medium';
  const priMatch = text.match(/(^|\\s)!([123])(?=\\s|$)/);
  if (priMatch) {
    priority = priMatch[2] === '1' ? 'high' : priMatch[2] === '2' ? 'medium' : 'low';
    text = (text.slice(0, priMatch.index) + text.slice(priMatch.index + priMatch[0].length)).trim();
  }
  let customerId = '';
  const custMatch = text.match(/(^|\\s)#([^\\s@#]+)/);
  if (custMatch) {
    const name = custMatch[2];
    const hit = state.customers.find((c) => c.name === name || c.name.startsWith(name));
    if (hit) customerId = hit.id;
    text = (text.slice(0, custMatch.index) + text.slice(custMatch.index + custMatch[0].length)).trim();
  }
  let propertyId = '';
  const propMatch = text.match(/(^|\\s)@([^\\s#]+)/);
  if (propMatch) {
    const name = propMatch[2];
    const hit = state.properties.find((p) => p.title === name || p.title.startsWith(name));
    if (hit) propertyId = hit.id;
    text = (text.slice(0, propMatch.index) + text.slice(propMatch.index + propMatch[0].length)).trim();
  }
  const dueRes = extractDueFromText(text);
  text = dueRes.remaining;
  const title = text.trim();
  if (!title) return null;
  return {
    title,
    priority,
    customerId,
    propertyId,
    due: dueRes.due || '',
    status: 'todo',
    assignedTo: state.session?.name || DEFAULT_USER.name,
    memo: ''
  };
}

function extractDueFromText(text) {
  const trimmed = text.trim();
  const patterns = [
    { re: /(^|\\s)(今日|today)(?:\\s+(\\d{1,2}):(\\d{2}))?(?=\\s|$)/i, resolve: (m) => datePlusDays(0, m[3], m[4]) },
    { re: /(^|\\s)(明日|tomorrow)(?:\\s+(\\d{1,2}):(\\d{2}))?(?=\\s|$)/i, resolve: (m) => datePlusDays(1, m[3], m[4]) },
    { re: /(^|\\s)(明後日)(?:\\s+(\\d{1,2}):(\\d{2}))?(?=\\s|$)/, resolve: (m) => datePlusDays(2, m[3], m[4]) },
    { re: /(^|\\s)(月曜|火曜|水曜|木曜|金曜|土曜|日曜)(?:\\s+(\\d{1,2}):(\\d{2}))?(?=\\s|$)/, resolve: (m) => nextWeekday(m[2], m[3], m[4]) },
    { re: /(^|\\s)(\\d{1,2})\\/(\\d{1,2})(?:\\s+(\\d{1,2}):(\\d{2}))?(?=\\s|$)/, resolve: (m) => monthDay(m[2], m[3], m[4], m[5]) }
  ];
  for (const p of patterns) {
    const m = trimmed.match(p.re);
    if (m) {
      const due = p.resolve(m);
      const start = m.index + (m[1] ? m[1].length : 0);
      const end = m.index + m[0].length;
      const remaining = (trimmed.slice(0, start) + trimmed.slice(end)).replace(/\\s+/g, ' ').trim();
      return { due, remaining };
    }
  }
  return { due: '', remaining: trimmed };
}

function datePlusDays(delta, hh, mm) {
  const now = new Date();
  const d = new Date(now.getFullYear(), now.getMonth(), now.getDate() + delta);
  return dueString(d, hh, mm);
}

function nextWeekday(label, hh, mm) {
  const map = { '日曜': 0, '月曜': 1, '火曜': 2, '水曜': 3, '木曜': 4, '金曜': 5, '土曜': 6 };
  const target = map[label];
  const now = new Date();
  const base = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  let delta = (target - base.getDay() + 7) % 7;
  if (delta === 0) delta = 7;
  const d = new Date(base.getFullYear(), base.getMonth(), base.getDate() + delta);
  return dueString(d, hh, mm);
}

function monthDay(mo, day, hh, mm) {
  const now = new Date();
  let year = now.getFullYear();
  const candidate = new Date(year, Number(mo) - 1, Number(day));
  if (candidate < new Date(now.getFullYear(), now.getMonth(), now.getDate())) year += 1;
  const d = new Date(year, Number(mo) - 1, Number(day));
  return dueString(d, hh, mm);
}

function dueString(d, hh, mm) {
  const yy = d.getFullYear();
  const mo = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  if (hh != null && mm != null) {
    const h = String(hh).padStart(2, '0');
    const m = String(mm).padStart(2, '0');
    return `${yy}-${mo}-${dd} ${h}:${m}`;
  }
  return `${yy}-${mo}-${dd}`;
}

function submitQuickTask() {
  const input = document.getElementById('quickTaskInput');
  if (!input) return;
  const payload = parseQuickTaskInput(input.value);
  if (!payload) {
    input.focus();
    return;
  }
  const newTask = { id: uid('tk', state.tasks), sourcePostId: null, ...payload };
  state.tasks.unshift(newTask);
  saveState();
  rerenderAll();
  input.value = '';
  input.focus();
  showNotice('タスクを追加しました。続けて入力できます。');
}
window.submitQuickTask = submitQuickTask;

function initQuickTaskBar() {
  const input = document.getElementById('quickTaskInput');
  if (!input || input.dataset.bound) return;
  input.dataset.bound = '1';
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      submitQuickTask();
    } else if (e.key === 'Escape') {
      e.preventDefault();
      toggleQuickTaskBar(false);
    }
  });
}
'''

# Insert renderTasks and helpers just before rerenderAll definition
anchor = 'function rerenderAll() {'
assert anchor in app, 'rerenderAll anchor not found'
app = app.replace(anchor, render_tasks_impl + '\n' + anchor)

# 4) Ensure quick task bar events bound after DOM ready (attach in initEvents)
init_anchor = "function initEvents() {\n  document.querySelectorAll('.nav-btn').forEach"
new_init = "function initEvents() {\n  initQuickTaskBar();\n  document.querySelectorAll('.nav-btn').forEach"
assert init_anchor in app, 'initEvents anchor not found'
app = app.replace(init_anchor, new_init)

# 5) When re-rendering tasks screen, re-bind quick input (list re-render doesn't destroy it, but safety)
app = app.replace(
    "  renderTasks();\n  renderSchedules();",
    "  renderTasks();\n  initQuickTaskBar();\n  renderSchedules();"
)

APP.write_text(app, encoding="utf-8")

# ---------- styles.css ----------
css = CSS.read_text(encoding="utf-8")

extra_css = '''

/* ---------- Todoist-style task list & quick add ---------- */
.tasks-panel { padding: 12px; }
.quick-task-bar {
  display: grid;
  gap: 8px;
  padding: 12px;
  margin-bottom: 10px;
  border: 1px solid #bfdbfe;
  border-radius: 14px;
  background: linear-gradient(180deg, #ffffff, #eff6ff);
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.08);
}
.quick-task-bar.hidden { display: none; }
.quick-task-input-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 999px;
}
.quick-task-check {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px dashed #93c5fd;
  background: #eff6ff;
  color: #2563eb;
  font-weight: 900;
  font-size: 14px;
  line-height: 1;
  display: grid;
  place-items: center;
  cursor: default;
}
.quick-task-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  font-weight: 600;
  color: #0f172a;
  padding: 8px 4px;
  min-width: 0;
}
.quick-task-hint {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 12px;
  font-size: 11px;
  color: #475569;
  padding: 0 4px;
}
.quick-task-hint span {
  background: #ffffffaa;
  border: 1px solid #dbeafe;
  border-radius: 999px;
  padding: 2px 8px;
}

.todoist-task-list { gap: 6px; }
.todo-task {
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 10px;
  align-items: start;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-left-width: 4px;
  border-left-color: #cbd5e1;
  border-radius: 12px;
  background: #ffffff;
  cursor: pointer;
  transition: background .12s ease, transform .05s ease;
}
.todo-task:active { transform: scale(0.998); background: #f8fafc; }
.todo-task.priority-high { border-left-color: #ef4444; }
.todo-task.priority-medium { border-left-color: #f59e0b; }
.todo-task.priority-low { border-left-color: #94a3b8; }
.todo-task.is-done { opacity: 0.55; }
.todo-task.is-done .todo-title { text-decoration: line-through; color: #64748b; }

.todo-check {
  width: 22px;
  height: 22px;
  margin-top: 2px;
  border-radius: 50%;
  border: 2px solid #cbd5e1;
  background: #ffffff;
  color: transparent;
  font-size: 14px;
  font-weight: 900;
  display: grid;
  place-items: center;
  cursor: pointer;
  padding: 0;
}
.todo-check.checked {
  background: #10b981;
  border-color: #10b981;
  color: #ffffff;
}
.todo-task.priority-high .todo-check { border-color: #fca5a5; }
.todo-task.priority-medium .todo-check { border-color: #fbbf24; }

.todo-main { min-width: 0; display: grid; gap: 4px; }
.todo-title-row {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
}
.todo-title {
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.35;
  word-break: break-word;
}
.todo-priority-badge {
  font-size: 10px;
  font-weight: 900;
  padding: 2px 6px;
  border-radius: 6px;
  color: #ffffff;
  letter-spacing: .5px;
  flex-shrink: 0;
}
.todo-priority-badge.priority-high { background: #ef4444; }
.todo-priority-badge.priority-medium { background: #f59e0b; }
.todo-priority-badge.priority-low { background: #94a3b8; }

.todo-memo-preview {
  font-size: 12px;
  color: #64748b;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.todo-badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 2px;
}
.todo-due-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #f1f5f9;
  color: #475569;
}
.todo-due-badge.today { background: #ecfdf5; color: #047857; border-color: #86efac; }
.todo-due-badge.tomorrow { background: #eff6ff; color: #1d4ed8; border-color: #bfdbfe; }
.todo-due-badge.soon { background: #fff7ed; color: #c2410c; border-color: #fed7aa; }
.todo-due-badge.overdue { background: #fef2f2; color: #b91c1c; border-color: #fecaca; }
.todo-due-badge.later { background: #f8fafc; color: #475569; border-color: #e2e8f0; }

.todo-chip {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #334155;
}
.todo-chip.cust { background: #eef2ff; color: #3730a3; border-color: #c7d2fe; }
.todo-chip.sale { background: #eff6ff; color: #174ea6; border-color: #bfdbfe; }
.todo-chip.rental { background: #ecfeff; color: #0f766e; border-color: #99f6e4; }

.task-edit-form .task-title-label input { font-size: 17px; font-weight: 700; }
.task-memo-label { align-items: stretch; }
.task-memo-area {
  min-height: 220px;
  font-size: 14px;
  line-height: 1.6;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid var(--line);
  resize: vertical;
  background: #fffdf7;
}
'''

if '/* ---------- Todoist-style task list & quick add ---------- */' not in css:
    css += extra_css

CSS.write_text(css, encoding="utf-8")

print("OK")
