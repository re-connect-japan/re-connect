from pathlib import Path

path = Path('/home/user/re-connect-repo/app.js')
text = path.read_text()

helpers = '''
function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
function taskStatusLabel(status) {
  return ({ todo: '未着手', doing: '進行中', hold: '保留', done: '完了', returned: '差戻し' })[status] || (status || '-');
}
function taskPriorityLabel(priority) {
  return ({ high: '優先度高', medium: '優先度中', low: '優先度低' })[priority] || '優先度未設定';
}
function taskPriorityShort(priority) {
  return ({ high: 'P1', medium: 'P2', low: 'P3' })[priority] || 'P2';
}
function sortTasksForView(tasks) {
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
}
function renderTaskCard(task, options = {}) {
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
}
function toggleTaskDone(event, taskId) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
  const task = state.tasks.find((t) => t.id === taskId);
  if (!task) return;
  task.status = task.status === 'done' ? 'todo' : 'done';
  saveState();
  rerenderAll();
  showNotice(task.status === 'done' ? 'タスクを完了にしました。' : 'タスクを未完了に戻しました。');
}
window.toggleTaskDone = toggleTaskDone;
'''

old_marker = "function renderHome() {"
if helpers not in text:
    text = text.replace(old_marker, helpers + "\n" + old_marker)

old_home = """  document.getElementById('homeTasks').innerHTML = state.tasks.map((t) => {
    const c = getCustomer(t.customerId); const p = getProperty(t.propertyId);
    return `
      <div class=\"item clickable\" onclick=\"openTaskEditor('${t.id}')\">
        <div class=\"item-title\">${t.due} ${t.title}</div>
        <div class=\"item-sub\">${c?.name || '-'} / ${p?.title || '-'} / ${t.status}</div>
        <div class=\"top-meta\">
          <span class=\"chip ${t.priority === 'high' ? 'active' : ''}\">${t.priority}</span>
          ${p ? `<span class=\"chip ${p.dealType}\">${dealTypeLabel(p.dealType)}</span>` : ''}
        </div>
      </div>
    `;
  }).join('') || '<div class=\"empty-state\">タスクはありません</div>';"""
new_home = """  document.getElementById('homeTasks').innerHTML = sortTasksForView(state.tasks)
    .slice(0, 6)
    .map((t) => renderTaskCard(t, { compact: true }))
    .join('') || '<div class=\"empty-state\">タスクはありません</div>';"""
text = text.replace(old_home, new_home)

old_day_detail = """    ${tks.length ? `<div class="cal-day-section"><div class="cal-day-subtitle">タスク</div>${tks.map((t) => {
      const c = getCustomer(t.customerId); const p = getProperty(t.propertyId);
      return `<div class="item clickable" onclick="openTaskEditor('${t.id}')"><div class="item-title">${t.due} ${t.title}</div><div class="item-sub">${c?.name || '-'} / ${p?.title || '-'} / ${t.status}</div></div>`;
    }).join('')}</div>` : ''}
  `;"""
new_day_detail = """    ${tks.length ? `<div class="cal-day-section"><div class="cal-day-subtitle">タスク</div>${sortTasksForView(tks).map((t) => renderTaskCard(t, { compact: true })).join('')}</div>` : ''}
  `;"""
text = text.replace(old_day_detail, new_day_detail)

old_render_tasks = """function renderTasks() {
  const countEl = document.getElementById('taskCountPill');
  if (countEl) countEl.textContent = `${state.tasks.length}件`;
  const listEl = document.getElementById('taskList');
  if (listEl) listEl.innerHTML = state.tasks.map((task) => {
    const customer = getCustomer(task.customerId);
    const property = getProperty(task.propertyId);
    return `
      <div class="item clickable" onclick="openTaskEditor('${task.id}')">
        <div class="item-title">${task.title}</div>
        <div class="item-sub">${task.status} / ${task.priority} / ${task.due}</div>
        <div class="item-sub">${customer?.name || '-'} / 担当: ${task.assignedTo || '-'}</div>
        <div class="top-meta">${property ? `<span class="chip ${property.dealType}">${dealTypeLabel(property.dealType)}</span>` : ''}</div>
      </div>
    `;
  }).join('') || '<div class="empty-state">タスクはありません</div>';
}"""
new_render_tasks = """function renderTasks() {
  const countEl = document.getElementById('taskCountPill');
  if (countEl) countEl.textContent = `${state.tasks.length}件`;
  const listEl = document.getElementById('taskList');
  if (listEl) listEl.innerHTML = sortTasksForView(state.tasks)
    .map((task) => renderTaskCard(task))
    .join('') || '<div class="empty-state">タスクはありません</div>';
}"""
text = text.replace(old_render_tasks, new_render_tasks)

path.write_text(text)

css_path = Path('/home/user/re-connect-repo/styles.css')
css = css_path.read_text()
css_block = '''
.todo-task {
  display: grid;
  grid-template-columns: 28px 1fr 14px;
  gap: 12px;
  align-items: start;
  background: var(--surface);
  border: 1px solid var(--line);
  border-left: 4px solid var(--line-strong);
  border-radius: 18px;
  padding: 14px 14px 14px 12px;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
  cursor: pointer;
  transition: transform .06s ease, box-shadow .15s ease, border-color .15s ease;
}
.todo-task:active {
  transform: scale(0.995);
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
}
.todo-task.compact { padding: 12px 12px 12px 10px; }
.todo-task.priority-high { border-left-color: #dc2626; }
.todo-task.priority-medium { border-left-color: #d97706; }
.todo-task.priority-low { border-left-color: #2563eb; }
.todo-task.is-done {
  background: #f8fafc;
  border-color: #e2e8f0;
  border-left-color: #94a3b8;
}
.todo-task.is-done .todo-title,
.todo-task.is-done .todo-meta-row,
.todo-task.is-done .todo-context-row { color: #94a3b8; }
.todo-check {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  border: 2px solid var(--line-strong);
  background: white;
  color: white;
  display: grid;
  place-items: center;
  padding: 0;
  margin-top: 2px;
  font-size: 14px;
  font-weight: 900;
  cursor: pointer;
}
.todo-task.priority-high .todo-check { border-color: #dc2626; }
.todo-task.priority-medium .todo-check { border-color: #d97706; }
.todo-task.priority-low .todo-check { border-color: #2563eb; }
.todo-check.checked {
  background: var(--success);
  border-color: var(--success);
}
.todo-main { min-width: 0; }
.todo-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}
.todo-title {
  font-size: 15px;
  font-weight: 800;
  line-height: 1.4;
  color: var(--text);
  word-break: break-word;
}
.todo-priority-badge {
  flex: 0 0 auto;
  min-width: 36px;
  text-align: center;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 800;
  border: 1px solid var(--line-strong);
  background: var(--surface-soft);
}
.todo-priority-badge.priority-high { color: #b91c1c; background: #fef2f2; border-color: #fca5a5; }
.todo-priority-badge.priority-medium { color: #b45309; background: #fff7ed; border-color: #fdba74; }
.todo-priority-badge.priority-low { color: #1d4ed8; background: #eff6ff; border-color: #93c5fd; }
.todo-meta-row,
.todo-context-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  align-items: center;
  margin-top: 6px;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.45;
}
.todo-date { font-weight: 700; color: var(--text); }
.todo-dot { color: #cbd5e1; }
.todo-tags-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 8px;
}
.todo-chip {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: var(--surface-soft);
  color: var(--muted);
  font-size: 11px;
  font-weight: 700;
}
.todo-chip.sale { background: var(--brand-soft); color: var(--brand); border-color: #93c5fd; }
.todo-chip.rental { background: var(--teal-soft); color: var(--teal); border-color: #99f6e4; }
.todo-arrow {
  align-self: center;
  color: #94a3b8;
  font-size: 18px;
  font-weight: 800;
}
'''
marker = ".item.clickable { cursor: pointer; }"
if css_block not in css:
    css = css.replace(marker, css_block + "\n" + marker)
css_path.write_text(css)

html_path = Path('/home/user/re-connect-repo/index.html')
html = html_path.read_text()
html = html.replace('<p>タップで詳細・編集へ</p>', '<p>Todoist風の一覧で素早く確認・完了</p>')
html = html.replace('<div id="taskList" class="stack"></div>', '<div id="taskList" class="stack todoist-task-list"></div>')
html = html.replace('<div id="homeTasks" class="stack"></div>', '<div id="homeTasks" class="stack todoist-task-list"></div>')
html_path.write_text(html)
print('updated')
