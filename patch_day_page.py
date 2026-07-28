#!/usr/bin/env python3
"""Month calendar day tap -> dedicated single-day page (home + schedule)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.js"
HTML = ROOT / "index.html"
CSS = ROOT / "styles.css"

# ---------- index.html ----------
html = HTML.read_text(encoding="utf-8")

# 1) Remove the inline day-detail from the home month view (single-day page will replace it)
old_home_month = (
    '              <div class="cal-grid" id="calGrid"></div>\n'
    '              <div class="cal-day-detail" id="calDayDetail"></div>\n'
)
new_home_month = (
    '              <div class="cal-grid" id="calGrid"></div>\n'
)
assert old_home_month in html
html = html.replace(old_home_month, new_home_month)

# 2) Insert single-day page section right after screen-calendar
day_section = (
    '\n        <section id="screen-day" class="screen">\n'
    '          <div class="screen-header with-back">\n'
    '            <button type="button" class="back-btn" onclick="closeDayPage()">‹ 戻る</button>\n'
    '            <h2 id="dayPageTitle">日別ページ</h2>\n'
    '          </div>\n'
    '          <article class="panel mobile-panel day-page-panel">\n'
    '            <div class="day-page-toolbar">\n'
    '              <button type="button" class="secondary-btn small" onclick="shiftDayPage(-1)">‹ 前日</button>\n'
    '              <button type="button" class="secondary-btn small" onclick="jumpDayPageToToday()">今日</button>\n'
    '              <button type="button" class="secondary-btn small" onclick="shiftDayPage(1)">翌日 ›</button>\n'
    '            </div>\n'
    '            <div class="day-page-add">\n'
    '              <button type="button" class="primary-btn small" id="dayAddSchedule">＋ 予定を追加</button>\n'
    '              <button type="button" class="primary-btn small" id="dayAddTask">＋ タスクを追加</button>\n'
    '            </div>\n'
    '            <div id="dayPageBody" class="day-page-body"></div>\n'
    '          </article>\n'
    '        </section>\n'
)

anchor = '        <section id="screen-schedule-edit" class="screen">'
assert anchor in html
html = html.replace(anchor, day_section + "\n" + anchor)

# cache bust
html = html.replace('./styles.css?v=21', './styles.css?v=22')
html = html.replace('./app.js?v=21', './app.js?v=22')
HTML.write_text(html, encoding="utf-8")

# ---------- app.js ----------
app = APP.read_text(encoding="utf-8")

# 1) State for day page
inject_state = "let dayPageDate = null;\n"
if "let dayPageDate" not in app:
    app = app.replace(
        "let scheduleCalendarView = 'month';",
        "let scheduleCalendarView = 'month';\n" + inject_state,
        1,
    )

# 2) Remove day detail render call from home month, and change day click to open day page
old_home_click_block = (
    "  grid.innerHTML = cells.join('');\n"
    "  grid.querySelectorAll('.cal-day').forEach((btn) => {\n"
    "    btn.addEventListener('click', () => {\n"
    "      const [yy, mm, dd] = btn.dataset.key.split('-').map(Number);\n"
    "      homeCalendarSelected = new Date(yy, mm - 1, dd);\n"
    "      renderHomeCalendarMonth();\n"
    "    });\n"
    "  });\n"
    "  renderHomeCalendarDayDetail(scheduleByDate, taskByDate);\n"
    "}"
)
new_home_click_block = (
    "  grid.innerHTML = cells.join('');\n"
    "  grid.querySelectorAll('.cal-day').forEach((btn) => {\n"
    "    btn.addEventListener('click', () => {\n"
    "      openDayPage(btn.dataset.key);\n"
    "    });\n"
    "  });\n"
    "}"
)
assert old_home_click_block in app
app = app.replace(old_home_click_block, new_home_click_block)

# 3) Change schedule month grid click to open day page instead of just selecting
old_selectFn = (
    "function selectScheduleCalendarDay(key) {\n"
)
# safer: replace whole function
old_selectFn_full = (
    "  scheduleCalendarSelected = new Date(yy, mm - 1, dd);\n"
    "  scheduleCalendarCursor = new Date(yy, mm - 1, dd);\n"
    "  renderSchedules();\n"
    "}\n"
    "window.selectScheduleCalendarDay = selectScheduleCalendarDay;"
)
# in current file, selectScheduleCalendarDay body is above; we override behavior only when the schedule view is 'month' to open dedicated day page.
new_selectFn_full = (
    "  if (scheduleCalendarView === 'month') {\n"
    "    openDayPage(key);\n"
    "    return;\n"
    "  }\n"
    "  scheduleCalendarSelected = new Date(yy, mm - 1, dd);\n"
    "  scheduleCalendarCursor = new Date(yy, mm - 1, dd);\n"
    "  renderSchedules();\n"
    "}\n"
    "window.selectScheduleCalendarDay = selectScheduleCalendarDay;"
)
assert old_selectFn_full in app
app = app.replace(old_selectFn_full, new_selectFn_full)

# 4) Append day-page implementation & helpers before rerenderAll
day_impl = '''
function openDayPage(key) {
  if (!key) {
    const now = new Date();
    key = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
  }
  const [yy, mm, dd] = key.split('-').map(Number);
  dayPageDate = new Date(yy, mm - 1, dd);
  renderDayPage();
  go('day');
}
window.openDayPage = openDayPage;

function closeDayPage() {
  go('home');
}
window.closeDayPage = closeDayPage;

function shiftDayPage(delta) {
  if (!dayPageDate) dayPageDate = new Date();
  dayPageDate = new Date(dayPageDate.getFullYear(), dayPageDate.getMonth(), dayPageDate.getDate() + delta);
  renderDayPage();
}
window.shiftDayPage = shiftDayPage;

function jumpDayPageToToday() {
  const now = new Date();
  dayPageDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  renderDayPage();
}
window.jumpDayPageToToday = jumpDayPageToToday;

function renderDayPage() {
  const target = dayPageDate || new Date();
  const key = dateKey(target);
  const label = `${target.getFullYear()}年${target.getMonth()+1}月${target.getDate()}日 (${['日','月','火','水','木','金','土'][target.getDay()]})`;
  const titleEl = document.getElementById('dayPageTitle');
  if (titleEl) titleEl.textContent = label;

  const scheds = state.schedules.filter((s) => {
    const d = parseWhen(s.when);
    return d && dateKey(d) === key;
  });
  const tks = state.tasks.filter((t) => {
    const src = t.status === 'done' ? (t.completedAt || t.due) : t.due;
    const d = parseWhen(src);
    return d && dateKey(d) === key;
  });

  const body = document.getElementById('dayPageBody');
  if (!body) return;
  const scheduleHtml = scheds.length
    ? sortSchedulesForView(scheds).map((s) => {
        const c = getCustomer(s.customerId);
        const p = getProperty(s.propertyId);
        return `
          <button type="button" class="day-page-item schedule ${scheduleStatusClass(s.status)}" onclick="openScheduleEditor('${s.id}')">
            <div class="day-page-item-time">${escapeHtml(formatScheduleTimeLabel(s.when))}</div>
            <div class="day-page-item-main">
              <div class="day-page-item-title">${escapeHtml(s.title || '予定')}</div>
              <div class="day-page-item-sub">${escapeHtml(c?.name || '-')} / ${escapeHtml(p?.title || '-')} / ${escapeHtml(scheduleStatusLabel ? scheduleStatusLabel(s.status) : s.status)}</div>
            </div>
          </button>
        `;
      }).join('')
    : '<div class="empty-state compact-empty">予定はありません</div>';

  const taskHtml = tks.length
    ? sortTasksForView(tks).map((t) => renderTaskCard(t, { compact: true })).join('')
    : '<div class="empty-state compact-empty">タスクはありません</div>';

  body.innerHTML = `
    <div class="day-page-section">
      <div class="day-page-section-title">予定 (${scheds.length})</div>
      <div class="day-page-section-body">${scheduleHtml}</div>
    </div>
    <div class="day-page-section">
      <div class="day-page-section-title">タスク (${tks.length})</div>
      <div class="day-page-section-body">${taskHtml}</div>
    </div>
  `;

  const addSch = document.getElementById('dayAddSchedule');
  const addTk = document.getElementById('dayAddTask');
  if (addSch) addSch.onclick = () => openScheduleEditor('', key);
  if (addTk) addTk.onclick = () => openTaskEditor('', key);
}
window.renderDayPage = renderDayPage;

function scheduleStatusLabel(code) {
  return ({ planned: '予定', done: '完了', cancelled: 'キャンセル', rescheduled: '延期' })[code] || code || '';
}
'''

# scheduleStatusLabel may already exist; guard
if "function scheduleStatusLabel" in app:
    day_impl = day_impl.replace(
        "\nfunction scheduleStatusLabel(code) {\n"
        "  return ({ planned: '予定', done: '完了', cancelled: 'キャンセル', rescheduled: '延期' })[code] || code || '';\n"
        "}\n", ""
    )

anchor2 = "function rerenderAll() {"
assert anchor2 in app
app = app.replace(anchor2, day_impl + "\n" + anchor2)

# 5) Re-render day page when data changes; safe if screen-day is inactive
app = app.replace(
    "  renderTasks();\n  initQuickTaskBar();\n  renderSchedules();",
    "  renderTasks();\n  initQuickTaskBar();\n  renderSchedules();\n  if (document.getElementById('screen-day')?.classList.contains('active')) renderDayPage();",
)

APP.write_text(app, encoding="utf-8")

# ---------- styles.css ----------
css = CSS.read_text(encoding="utf-8")
add_css = """

/* ---------- Single-day page ---------- */
.day-page-panel {
  display: grid;
  gap: 12px;
}
.day-page-toolbar {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.day-page-add {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.day-page-body {
  display: grid;
  gap: 14px;
}
.day-page-section {
  display: grid;
  gap: 8px;
}
.day-page-section-title {
  font-size: 13px;
  font-weight: 800;
  color: #0f172a;
  padding: 4px 2px;
  border-bottom: 1px solid var(--line);
}
.day-page-section-body {
  display: grid;
  gap: 6px;
}
.day-page-item {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 10px;
  align-items: center;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-left-width: 4px;
  border-left-color: #93c5fd;
  border-radius: 12px;
  background: #ffffff;
  text-align: left;
  cursor: pointer;
}
.day-page-item.done { border-left-color: #86efac; }
.day-page-item.cancelled { border-left-color: #fca5a5; }
.day-page-item.rescheduled { border-left-color: #fdba74; }
.day-page-item-time {
  font-size: 13px;
  font-weight: 800;
  color: #1d4ed8;
}
.day-page-item-title {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 2px;
}
.day-page-item-sub {
  font-size: 12px;
  color: #64748b;
}
"""
if "/* ---------- Single-day page ---------- */" not in css:
    css += add_css
CSS.write_text(css, encoding="utf-8")

print("OK")
