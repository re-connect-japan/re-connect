from pathlib import Path

app_path = Path('/home/user/re-connect-repo/app.js')
text = app_path.read_text()

insert_vars_after = "let homeCalendarSelected = null;\n"
if "let scheduleCalendarCursor = null;" not in text:
    text = text.replace(insert_vars_after, insert_vars_after + "let scheduleCalendarCursor = null;\nlet scheduleCalendarSelected = null;\n")

helpers = '''
function scheduleStatusLabel(status) {
  return ({ planned: '予定中', done: '完了', cancelled: 'キャンセル', rescheduled: '再調整' })[status] || (status || '-');
}
function scheduleStatusClass(status) {
  return ({ planned: 'planned', done: 'done', cancelled: 'cancelled', rescheduled: 'rescheduled' })[status] || 'planned';
}
function sortSchedulesForView(schedules) {
  return [...schedules].sort((a, b) => {
    const ad = parseWhen(a.when);
    const bd = parseWhen(b.when);
    if (ad && bd) return ad - bd;
    return String(a.title || '').localeCompare(String(b.title || ''), 'ja');
  });
}
function formatScheduleTimeLabel(when) {
  const d = parseWhen(when);
  if (!d) return escapeHtml(when || '-');
  return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}
function renderScheduleAgendaCard(schedule) {
  const customer = getCustomer(schedule.customerId);
  const property = getProperty(schedule.propertyId);
  const dealChip = property ? `<span class="gcal-chip ${property.dealType}">${dealTypeLabel(property.dealType)}</span>` : '';
  const customerName = escapeHtml(customer?.name || '顧客未設定');
  const propertyName = escapeHtml(property?.title || '物件未設定');
  const location = schedule.location ? `<span>${escapeHtml(schedule.location)}</span>` : '';
  return `
    <button type="button" class="gcal-agenda-card ${scheduleStatusClass(schedule.status)}" onclick="openScheduleEditor('${schedule.id}')">
      <div class="gcal-agenda-time">${formatScheduleTimeLabel(schedule.when)}</div>
      <div class="gcal-agenda-body">
        <div class="gcal-agenda-title">${escapeHtml(schedule.title || '予定')}</div>
        <div class="gcal-agenda-meta">
          <span>${customerName}</span>
          <span class="todo-dot">/</span>
          <span>${propertyName}</span>
          ${location ? '<span class="todo-dot">•</span>' + location : ''}
        </div>
        <div class="gcal-agenda-tags">
          <span class="gcal-chip status ${scheduleStatusClass(schedule.status)}">${escapeHtml(scheduleStatusLabel(schedule.status))}</span>
          ${dealChip}
          ${schedule.sync ? `<span class="gcal-chip">${escapeHtml(schedule.sync)}</span>` : ''}
        </div>
      </div>
    </button>
  `;
}
function shiftScheduleCalendar(delta) {
  if (!scheduleCalendarCursor) {
    const now = new Date();
    scheduleCalendarCursor = new Date(now.getFullYear(), now.getMonth(), 1);
  }
  scheduleCalendarCursor = new Date(scheduleCalendarCursor.getFullYear(), scheduleCalendarCursor.getMonth() + delta, 1);
  renderSchedules();
}
window.shiftScheduleCalendar = shiftScheduleCalendar;
function jumpScheduleCalendarToToday() {
  const now = new Date();
  scheduleCalendarCursor = new Date(now.getFullYear(), now.getMonth(), 1);
  scheduleCalendarSelected = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  renderSchedules();
}
window.jumpScheduleCalendarToToday = jumpScheduleCalendarToToday;
function selectScheduleCalendarDay(key) {
  const [yy, mm, dd] = key.split('-').map(Number);
  scheduleCalendarSelected = new Date(yy, mm - 1, dd);
  renderSchedules();
}
window.selectScheduleCalendarDay = selectScheduleCalendarDay;
'''
marker = "function renderTasks() {"
if "function scheduleStatusLabel(status)" not in text:
    text = text.replace(marker, helpers + "\n" + marker)

old_render = '''function renderSchedules() {
  const countEl = document.getElementById('scheduleCountPill');
  if (countEl) countEl.textContent = `${state.schedules.length}件`;
  const listEl = document.getElementById('scheduleList');
  if (listEl) listEl.innerHTML = state.schedules.map((s) => {
    const customer = getCustomer(s.customerId);
    const property = getProperty(s.propertyId);
    return `
      <div class="item clickable" onclick="openScheduleEditor('${s.id}')">
        <div class="item-title">${s.when} ${s.title}</div>
        <div class="item-sub">${customer?.name || '-'} / ${property?.title || '-'} / ${s.status}</div>
        <div class="top-meta">
          ${property ? `<span class="chip ${property.dealType}">${dealTypeLabel(property.dealType)}</span>` : ''}
          <span class="chip">${s.sync || ''}</span>
          ${s.resultStatus ? `<span class="tag success">結果: ${s.resultStatus}</span>` : ''}
        </div>
      </div>
    `;
  }).join('') || '<div class="empty-state">予定はありません</div>';
}'''
new_render = '''function renderSchedules() {
  const countEl = document.getElementById('scheduleCountPill');
  if (countEl) countEl.textContent = `${state.schedules.length}件`;
  const listEl = document.getElementById('scheduleList');
  if (!listEl) return;

  if (!scheduleCalendarCursor) {
    const now = new Date();
    scheduleCalendarCursor = new Date(now.getFullYear(), now.getMonth(), 1);
  } else {
    scheduleCalendarCursor = new Date(scheduleCalendarCursor.getFullYear(), scheduleCalendarCursor.getMonth(), 1);
  }
  if (!scheduleCalendarSelected) {
    const now = new Date();
    scheduleCalendarSelected = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  }

  const y = scheduleCalendarCursor.getFullYear();
  const m = scheduleCalendarCursor.getMonth();
  const monthTitle = `${y}年${m + 1}月`;
  const scheduleByDate = {};
  state.schedules.forEach((s) => {
    const d = parseWhen(s.when);
    if (!d) return;
    const key = dateKey(d);
    (scheduleByDate[key] = scheduleByDate[key] || []).push(s);
  });
  Object.keys(scheduleByDate).forEach((key) => {
    scheduleByDate[key] = sortSchedulesForView(scheduleByDate[key]);
  });

  const firstDay = new Date(y, m, 1);
  const startWeekday = firstDay.getDay();
  const startDate = new Date(y, m, 1 - startWeekday);
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const weekLabels = ['日', '月', '火', '水', '木', '金', '土'];
  const cells = [];
  for (let i = 0; i < 42; i++) {
    const d = new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate() + i);
    const key = dateKey(d);
    const daySchedules = scheduleByDate[key] || [];
    const isCurrentMonth = d.getMonth() === m;
    const isToday = sameDay(d, today);
    const isSelected = scheduleCalendarSelected && sameDay(d, scheduleCalendarSelected);
    const previews = daySchedules.slice(0, 2).map((s) => `
      <span class="gcal-event-pill ${scheduleStatusClass(s.status)}">${formatScheduleTimeLabel(s.when)} ${escapeHtml(s.title || '予定')}</span>
    `).join('');
    const more = daySchedules.length > 2 ? `<span class="gcal-more">+${daySchedules.length - 2}</span>` : '';
    cells.push(`
      <button type="button" class="gcal-day ${isCurrentMonth ? '' : 'muted'} ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''}" onclick="selectScheduleCalendarDay('${key}')">
        <span class="gcal-day-num">${d.getDate()}</span>
        <span class="gcal-day-events">${previews}${more}</span>
      </button>
    `);
  }

  const selected = scheduleCalendarSelected || today;
  const selectedKey = dateKey(selected);
  const selectedSchedules = scheduleByDate[selectedKey] || [];
  const selectedLabel = `${selected.getFullYear()}年${selected.getMonth() + 1}月${selected.getDate()}日`;
  const agenda = selectedSchedules.length
    ? sortSchedulesForView(selectedSchedules).map((s) => renderScheduleAgendaCard(s)).join('')
    : '<div class="empty-state compact-empty">この日の予定はありません</div>';

  listEl.innerHTML = `
    <div class="gcal-shell">
      <div class="gcal-toolbar">
        <div class="gcal-toolbar-main">
          <button type="button" class="gcal-nav-btn" onclick="shiftScheduleCalendar(-1)" aria-label="前月">‹</button>
          <div class="gcal-month-block">
            <div class="gcal-month-label">${monthTitle}</div>
            <div class="gcal-month-sub">Googleカレンダー風 月表示</div>
          </div>
          <button type="button" class="gcal-nav-btn" onclick="shiftScheduleCalendar(1)" aria-label="翌月">›</button>
        </div>
        <div class="gcal-toolbar-actions">
          <button type="button" class="secondary-btn small" onclick="jumpScheduleCalendarToToday()">今日</button>
          <button type="button" class="primary-btn small" onclick="openScheduleEditor('', '${selectedKey}')">＋ 予定</button>
        </div>
      </div>
      <div class="gcal-weekdays">${weekLabels.map((w, i) => `<span class="${i === 0 ? 'sun' : i === 6 ? 'sat' : ''}">${w}</span>`).join('')}</div>
      <div class="gcal-grid">${cells.join('')}</div>
      <div class="gcal-agenda-panel">
        <div class="gcal-agenda-header">
          <div>
            <div class="gcal-agenda-title-main">${selectedLabel}</div>
            <div class="gcal-agenda-sub">${selectedSchedules.length}件の予定</div>
          </div>
          <button type="button" class="secondary-btn small" onclick="openScheduleEditor('', '${selectedKey}')">この日に追加</button>
        </div>
        <div class="gcal-agenda-list">${agenda}</div>
      </div>
    </div>
  `;
}'''
text = text.replace(old_render, new_render)

app_path.write_text(text)

css_path = Path('/home/user/re-connect-repo/styles.css')
css = css_path.read_text()
css_block = '''
.gcal-shell {
  display: grid;
  gap: 12px;
}
.gcal-toolbar {
  display: grid;
  gap: 10px;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #f8fbff);
}
.gcal-toolbar-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
.gcal-month-block {
  flex: 1;
  min-width: 0;
}
.gcal-month-label {
  font-size: 22px;
  font-weight: 800;
  color: var(--text);
}
.gcal-month-sub {
  margin-top: 2px;
  font-size: 12px;
  color: var(--muted);
}
.gcal-nav-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1px solid var(--line);
  background: var(--surface);
  color: var(--brand-dark);
  font-size: 22px;
  line-height: 1;
  cursor: pointer;
}
.gcal-toolbar-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.gcal-weekdays {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 6px;
  padding: 0 2px;
  font-size: 11px;
  font-weight: 800;
  color: var(--muted);
  text-align: center;
}
.gcal-weekdays .sun { color: #dc2626; }
.gcal-weekdays .sat { color: #2563eb; }
.gcal-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 6px;
}
.gcal-day {
  min-height: 92px;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: var(--surface);
  padding: 8px 6px;
  display: grid;
  align-content: start;
  gap: 6px;
  text-align: left;
  cursor: pointer;
}
.gcal-day.muted {
  background: #fbfdff;
  color: #94a3b8;
}
.gcal-day.today {
  border-color: #93c5fd;
  box-shadow: inset 0 0 0 1px #bfdbfe;
}
.gcal-day.selected {
  background: #eff6ff;
  border-color: var(--brand);
}
.gcal-day-num {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  font-size: 13px;
  font-weight: 800;
}
.gcal-day.today .gcal-day-num {
  background: var(--brand);
  color: white;
}
.gcal-day.selected .gcal-day-num {
  background: var(--brand-dark);
  color: white;
}
.gcal-day-events {
  display: grid;
  gap: 4px;
  min-width: 0;
}
.gcal-event-pill,
.gcal-more {
  display: block;
  border-radius: 999px;
  padding: 3px 7px;
  font-size: 10px;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.gcal-event-pill {
  background: #e8f0fe;
  color: #174ea6;
}
.gcal-event-pill.done {
  background: #ecfdf5;
  color: #166534;
}
.gcal-event-pill.cancelled {
  background: #fef2f2;
  color: #b91c1c;
}
.gcal-event-pill.rescheduled {
  background: #fff7ed;
  color: #b45309;
}
.gcal-more {
  color: var(--muted);
  background: var(--surface-soft);
}
.gcal-agenda-panel {
  border: 1px solid var(--line);
  border-radius: 18px;
  background: var(--surface);
  overflow: hidden;
}
.gcal-agenda-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  padding: 14px;
  border-bottom: 1px solid var(--line);
  background: #fbfdff;
}
.gcal-agenda-title-main {
  font-size: 16px;
  font-weight: 800;
}
.gcal-agenda-sub {
  margin-top: 2px;
  font-size: 12px;
  color: var(--muted);
}
.gcal-agenda-list {
  display: grid;
  gap: 10px;
  padding: 12px;
}
.gcal-agenda-card {
  width: 100%;
  border: 1px solid var(--line);
  border-left: 4px solid #93c5fd;
  border-radius: 16px;
  background: var(--surface);
  display: grid;
  grid-template-columns: 58px 1fr;
  gap: 12px;
  padding: 12px;
  text-align: left;
  cursor: pointer;
}
.gcal-agenda-card.done { border-left-color: #86efac; }
.gcal-agenda-card.cancelled { border-left-color: #fca5a5; }
.gcal-agenda-card.rescheduled { border-left-color: #fdba74; }
.gcal-agenda-time {
  font-size: 14px;
  font-weight: 800;
  color: var(--brand-dark);
  padding-top: 2px;
}
.gcal-agenda-title {
  font-size: 15px;
  font-weight: 800;
  line-height: 1.4;
}
.gcal-agenda-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 5px;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.45;
}
.gcal-agenda-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}
.gcal-chip {
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
.gcal-chip.sale { background: var(--brand-soft); color: var(--brand); border-color: #93c5fd; }
.gcal-chip.rental { background: var(--teal-soft); color: var(--teal); border-color: #99f6e4; }
.gcal-chip.status.planned { background: #e8f0fe; color: #174ea6; border-color: #bfdbfe; }
.gcal-chip.status.done { background: #ecfdf5; color: #166534; border-color: #86efac; }
.gcal-chip.status.cancelled { background: #fef2f2; color: #b91c1c; border-color: #fca5a5; }
.gcal-chip.status.rescheduled { background: #fff7ed; color: #b45309; border-color: #fdba74; }
.compact-empty { min-height: 96px; }
@media (max-width: 640px) {
  .gcal-day {
    min-height: 78px;
    padding: 8px 4px;
  }
  .gcal-event-pill,
  .gcal-more {
    font-size: 9px;
    padding: 3px 6px;
  }
  .gcal-agenda-header {
    align-items: flex-start;
    flex-direction: column;
  }
}
'''
anchor = '.item.clickable { cursor: pointer; }'
if '.gcal-shell {' not in css:
    css = css.replace(anchor, css_block + '\n' + anchor)
css_path.write_text(css)

html_path = Path('/home/user/re-connect-repo/index.html')
html = html_path.read_text()
html = html.replace('<p>タップで詳細・編集・結果登録へ</p>', '<p>Googleカレンダー風の月表示と日別予定</p>')
html_path.write_text(html)

print('updated')
