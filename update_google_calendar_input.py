from pathlib import Path

index_path = Path('/home/user/re-connect-repo/index.html')
html = index_path.read_text()
old_block = '''              <label><span>タイトル</span><input name="title" id="scheduleEditTitleInput" placeholder="例: 内見" /></label>
              <div class="datetime-row">
                <label class="dt-date"><span>日付</span><input type="date" id="scheduleEditDate" /></label>
                <div class="dt-time">
                  <span class="dt-label">時間</span>
                  <div class="time-roller">
                    <select id="scheduleEditHour" class="roll roll-hour" aria-label="時"></select>
                    <span class="roll-sep">:</span>
                    <select id="scheduleEditMinute" class="roll roll-min" aria-label="分"></select>
                  </div>
                </div>
              </div>
              <input type="hidden" name="when" id="scheduleEditWhen" value="" />'''
new_block = '''              <label><span>タイトル</span><input name="title" id="scheduleEditTitleInput" placeholder="例: 内見" /></label>
              <div class="gcal-compose-card">
                <div class="gcal-compose-summary" id="scheduleEditorSummary">日付と時間を選ぶとここに反映されます</div>
                <div class="gcal-quick-section">
                  <div class="gcal-quick-label">日付候補</div>
                  <div class="gcal-quick-row">
                    <button type="button" class="gcal-quick-chip" onclick="presetScheduleDate('today')">今日</button>
                    <button type="button" class="gcal-quick-chip" onclick="presetScheduleDate('tomorrow')">明日</button>
                    <button type="button" class="gcal-quick-chip" onclick="presetScheduleDate('nextweek')">来週</button>
                  </div>
                </div>
                <div class="gcal-quick-section">
                  <div class="gcal-quick-label">時間候補</div>
                  <div class="gcal-quick-row">
                    <button type="button" class="gcal-quick-chip" onclick="presetScheduleTime('allday')">終日</button>
                    <button type="button" class="gcal-quick-chip" onclick="presetScheduleTime('1000')">10:00</button>
                    <button type="button" class="gcal-quick-chip" onclick="presetScheduleTime('1300')">13:00</button>
                    <button type="button" class="gcal-quick-chip" onclick="presetScheduleTime('1500')">15:00</button>
                    <button type="button" class="gcal-quick-chip" onclick="presetScheduleTime('1800')">18:00</button>
                  </div>
                </div>
              </div>
              <div class="datetime-row gcal-editor-datetime">
                <label class="dt-date"><span>開始日</span><input type="date" id="scheduleEditDate" /></label>
                <label class="gcal-all-day-toggle"><input type="checkbox" id="scheduleEditAllDay" /> 終日</label>
                <div class="dt-time" id="scheduleEditTimeWrap">
                  <span class="dt-label">開始時間</span>
                  <div class="time-roller">
                    <select id="scheduleEditHour" class="roll roll-hour" aria-label="時"></select>
                    <span class="roll-sep">:</span>
                    <select id="scheduleEditMinute" class="roll roll-min" aria-label="分"></select>
                  </div>
                </div>
              </div>
              <input type="hidden" name="when" id="scheduleEditWhen" value="" />'''
if old_block in html:
    html = html.replace(old_block, new_block)
index_path.write_text(html)

app_path = Path('/home/user/re-connect-repo/app.js')
text = app_path.read_text()

helper_anchor = '''function readDateTime(prefix) {
  const dateEl = document.getElementById(prefix + 'Date');
  const hourEl = document.getElementById(prefix + 'Hour');
  const minEl = document.getElementById(prefix + 'Minute');
  const date = (dateEl && dateEl.value) ? dateEl.value : '';
  const hour = String((hourEl && hourEl.value) || '0').padStart(2, '0');
  const min = String((minEl && minEl.value) || '0').padStart(2, '0');
  return date ? `${date} ${hour}:${min}` : `${hour}:${min}`;
}
'''
replacement = '''function readDateTime(prefix) {
  const dateEl = document.getElementById(prefix + 'Date');
  const hourEl = document.getElementById(prefix + 'Hour');
  const minEl = document.getElementById(prefix + 'Minute');
  const allDayEl = document.getElementById(prefix + 'AllDay');
  const date = (dateEl && dateEl.value) ? dateEl.value : '';
  if (allDayEl && allDayEl.checked) return date ? `${date} 終日` : '終日';
  const hour = String((hourEl && hourEl.value) || '0').padStart(2, '0');
  const min = String((minEl && minEl.value) || '0').padStart(2, '0');
  return date ? `${date} ${hour}:${min}` : `${hour}:${min}`;
}
function setRollValue(id, value) {
  const el = document.getElementById(id);
  if (el) el.value = String(value);
}
function syncScheduleEditorTimeUi() {
  const allDayEl = document.getElementById('scheduleEditAllDay');
  const wrap = document.getElementById('scheduleEditTimeWrap');
  const hourEl = document.getElementById('scheduleEditHour');
  const minEl = document.getElementById('scheduleEditMinute');
  const hidden = !!(allDayEl && allDayEl.checked);
  if (wrap) wrap.classList.toggle('hidden', hidden);
  if (hourEl) hourEl.disabled = hidden;
  if (minEl) minEl.disabled = hidden;
}
function formatScheduleEditorSummary() {
  const dateEl = document.getElementById('scheduleEditDate');
  const allDayEl = document.getElementById('scheduleEditAllDay');
  const locationEl = document.getElementById('scheduleEditLocation');
  const titleEl = document.getElementById('scheduleEditTitleInput');
  const when = readDateTime('scheduleEdit');
  const parsed = parseWhen(when);
  const whenText = parsed
    ? `${parsed.getFullYear()}年${parsed.getMonth() + 1}月${parsed.getDate()}日 ${allDayEl && allDayEl.checked ? '終日' : `${String(parsed.getHours()).padStart(2, '0')}:${String(parsed.getMinutes()).padStart(2, '0')}`}`
    : ((dateEl && dateEl.value) || '日付未設定');
  const parts = [whenText];
  if (titleEl && titleEl.value.trim()) parts.push(titleEl.value.trim());
  if (locationEl && locationEl.value.trim()) parts.push(locationEl.value.trim());
  return parts.join(' ・ ');
}
function updateScheduleEditorSummary() {
  syncScheduleEditorTimeUi();
  const hiddenEl = document.getElementById('scheduleEditWhen');
  if (hiddenEl) hiddenEl.value = readDateTime('scheduleEdit');
  const summaryEl = document.getElementById('scheduleEditorSummary');
  if (summaryEl) summaryEl.textContent = formatScheduleEditorSummary();
}
function presetScheduleDate(kind) {
  const now = new Date();
  let d = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  if (kind === 'tomorrow') d.setDate(d.getDate() + 1);
  if (kind === 'nextweek') d.setDate(d.getDate() + 7);
  const dateEl = document.getElementById('scheduleEditDate');
  if (dateEl) dateEl.value = dateKey(d);
  updateScheduleEditorSummary();
}
window.presetScheduleDate = presetScheduleDate;
function presetScheduleTime(code) {
  const allDayEl = document.getElementById('scheduleEditAllDay');
  if (code === 'allday') {
    if (allDayEl) allDayEl.checked = true;
    updateScheduleEditorSummary();
    return;
  }
  if (allDayEl) allDayEl.checked = false;
  const hour = code.slice(0, 2);
  const minute = code.slice(2, 4);
  setRollValue('scheduleEditHour', Number(hour));
  setRollValue('scheduleEditMinute', Number(minute));
  updateScheduleEditorSummary();
}
window.presetScheduleTime = presetScheduleTime;
'''
if helper_anchor in text:
    text = text.replace(helper_anchor, replacement)

fill_anchor = '''function fillDateTimeInputs(prefix, source, presetDateKey, defaultHour) {
  ensureTimeRollerOptions(prefix);
  const dateEl = document.getElementById(prefix + 'Date');
  const hourEl = document.getElementById(prefix + 'Hour');
  const minEl = document.getElementById(prefix + 'Minute');
  let d = source ? parseWhen(source) : null;
  if (!d && presetDateKey) {
    const [yy, mm, dd] = presetDateKey.split('-').map(Number);
    d = new Date(yy, mm - 1, dd, defaultHour, 0, 0, 0);
  }
  if (!d) {
    const now = new Date();
    d = new Date(now.getFullYear(), now.getMonth(), now.getDate(), defaultHour, 0, 0, 0);
  }
  if (dateEl) dateEl.value = dateKey(d);
  if (hourEl) hourEl.value = String(d.getHours());
  if (minEl) {
    // ロールは5分刻みなので丸めて一致させる
    const m = Math.round(d.getMinutes() / 5) * 5;
    minEl.value = String(m % 60);
  }
}
'''
fill_replacement = '''function fillDateTimeInputs(prefix, source, presetDateKey, defaultHour) {
  ensureTimeRollerOptions(prefix);
  const dateEl = document.getElementById(prefix + 'Date');
  const hourEl = document.getElementById(prefix + 'Hour');
  const minEl = document.getElementById(prefix + 'Minute');
  const allDayEl = document.getElementById(prefix + 'AllDay');
  let d = source ? parseWhen(source) : null;
  if (!d && presetDateKey) {
    const [yy, mm, dd] = presetDateKey.split('-').map(Number);
    d = new Date(yy, mm - 1, dd, defaultHour, 0, 0, 0);
  }
  if (!d) {
    const now = new Date();
    d = new Date(now.getFullYear(), now.getMonth(), now.getDate(), defaultHour, 0, 0, 0);
  }
  if (dateEl) dateEl.value = dateKey(d);
  if (hourEl) hourEl.value = String(d.getHours());
  if (minEl) {
    const m = Math.round(d.getMinutes() / 5) * 5;
    minEl.value = String(m % 60);
  }
  if (allDayEl) allDayEl.checked = !!(source && String(source).includes('終日'));
}
'''
if fill_anchor in text:
    text = text.replace(fill_anchor, fill_replacement)

open_sched_anchor = '''function openScheduleEditor(scheduleId, presetDateKey) {
  populateEditorSelects();
  const isNew = !scheduleId;
  const s = isNew ? null : state.schedules.find((x) => x.id === scheduleId);
  document.getElementById('scheduleEditTitle').textContent = isNew ? '予定を新規作成' : '予定を編集';
  document.getElementById('scheduleEditId').value = s?.id || '';
  document.getElementById('scheduleEditTitleInput').value = s?.title || '';
  fillDateTimeInputs('scheduleEdit', s?.when, presetDateKey, 11);
  document.getElementById('scheduleEditWhen').value = readDateTime('scheduleEdit');
  document.getElementById('scheduleEditStatus').value = s?.status || 'planned';
  document.getElementById('scheduleEditLocation').value = s?.location || '';
  document.getElementById('scheduleEditSync').value = s?.sync || 'Google / iPhone queued';
  document.getElementById('scheduleEditCustomer').value = s?.customerId || '';
  document.getElementById('scheduleEditProperty').value = s?.propertyId || '';
  document.getElementById('scheduleEditResult').value = s?.resultStatus || '';
  document.getElementById('scheduleEditMemo').value = s?.memo || '';
  editorReturnScreen = document.querySelector('.screen.active')?.id?.replace('screen-','') || 'home';
  go('schedule-edit');
}
'''
open_sched_repl = '''function openScheduleEditor(scheduleId, presetDateKey) {
  populateEditorSelects();
  const isNew = !scheduleId;
  const s = isNew ? null : state.schedules.find((x) => x.id === scheduleId);
  document.getElementById('scheduleEditTitle').textContent = isNew ? '予定を新規作成' : '予定を編集';
  document.getElementById('scheduleEditId').value = s?.id || '';
  document.getElementById('scheduleEditTitleInput').value = s?.title || '';
  fillDateTimeInputs('scheduleEdit', s?.when, presetDateKey, 11);
  document.getElementById('scheduleEditWhen').value = readDateTime('scheduleEdit');
  document.getElementById('scheduleEditStatus').value = s?.status || 'planned';
  document.getElementById('scheduleEditLocation').value = s?.location || '';
  document.getElementById('scheduleEditSync').value = s?.sync || 'Google / iPhone queued';
  document.getElementById('scheduleEditCustomer').value = s?.customerId || '';
  document.getElementById('scheduleEditProperty').value = s?.propertyId || '';
  document.getElementById('scheduleEditResult').value = s?.resultStatus || '';
  document.getElementById('scheduleEditMemo').value = s?.memo || '';
  updateScheduleEditorSummary();
  editorReturnScreen = document.querySelector('.screen.active')?.id?.replace('screen-','') || 'home';
  go('schedule-edit');
}
'''
if open_sched_anchor in text:
    text = text.replace(open_sched_anchor, open_sched_repl)

listener_anchor = '''  ['scheduleEditDate','scheduleEditHour','scheduleEditMinute'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', () => {
      document.getElementById('scheduleEditWhen').value = readDateTime('scheduleEdit');
    });
  });
'''
listener_repl = '''  ['scheduleEditDate','scheduleEditHour','scheduleEditMinute','scheduleEditAllDay','scheduleEditTitleInput','scheduleEditLocation'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', updateScheduleEditorSummary);
    if (el && (id === 'scheduleEditTitleInput' || id === 'scheduleEditLocation')) el.addEventListener('input', updateScheduleEditorSummary);
  });
'''
if listener_anchor in text:
    text = text.replace(listener_anchor, listener_repl)

app_path.write_text(text)

styles_path = Path('/home/user/re-connect-repo/styles.css')
css = styles_path.read_text()
anchor = '.gcal-chip.status.rescheduled { background: #fff7ed; color: #b45309; border-color: #fdba74; }\n'
insert_css = '''.gcal-compose-card {
  display: grid;
  gap: 12px;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #f8fbff);
}
.gcal-compose-summary {
  font-size: 14px;
  font-weight: 800;
  line-height: 1.5;
  color: var(--brand-dark);
}
.gcal-quick-section {
  display: grid;
  gap: 8px;
}
.gcal-quick-label {
  font-size: 12px;
  font-weight: 800;
  color: var(--muted);
}
.gcal-quick-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.gcal-quick-chip {
  border: 1px solid #bfdbfe;
  background: #eff6ff;
  color: #174ea6;
  border-radius: 999px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
}
.gcal-editor-datetime {
  align-items: end;
}
.gcal-all-day-toggle {
  min-height: 48px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 12px;
  border: 1px solid var(--line-strong);
  border-radius: 12px;
  background: white;
  font-size: 14px;
  font-weight: 700;
}
.gcal-all-day-toggle input {
  width: 18px;
  height: 18px;
}
#scheduleEditTimeWrap.hidden {
  display: none;
}
'''
if insert_css not in css and anchor in css:
    css = css.replace(anchor, anchor + insert_css)
styles_path.write_text(css)

print('updated')
