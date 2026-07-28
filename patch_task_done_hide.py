#!/usr/bin/env python3
"""
Hide completed tasks from the task list, but keep them visible
on the home month calendar (using completedAt as the display date).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.js"
HTML = ROOT / "index.html"

# ---------- app.js ----------
app = APP.read_text(encoding="utf-8")

# 1) toggleTaskDone: stamp/clear completedAt
old_toggle = (
    "function toggleTaskDone(event, taskId) {\n"
    "  if (event) {\n"
    "    event.preventDefault();\n"
    "    event.stopPropagation();\n"
    "  }\n"
    "  const task = state.tasks.find((t) => t.id === taskId);\n"
    "  if (!task) return;\n"
    "  task.status = task.status === 'done' ? 'todo' : 'done';\n"
    "  saveState();\n"
    "  rerenderAll();\n"
    "  showNotice(task.status === 'done' ? 'タスクを完了にしました。' : 'タスクを未完了に戻しました。');\n"
    "}"
)
new_toggle = (
    "function toggleTaskDone(event, taskId) {\n"
    "  if (event) {\n"
    "    event.preventDefault();\n"
    "    event.stopPropagation();\n"
    "  }\n"
    "  const task = state.tasks.find((t) => t.id === taskId);\n"
    "  if (!task) return;\n"
    "  if (task.status === 'done') {\n"
    "    task.status = 'todo';\n"
    "    task.completedAt = '';\n"
    "  } else {\n"
    "    task.status = 'done';\n"
    "    const now = new Date();\n"
    "    const yy = now.getFullYear();\n"
    "    const mo = String(now.getMonth() + 1).padStart(2, '0');\n"
    "    const dd = String(now.getDate()).padStart(2, '0');\n"
    "    const hh = String(now.getHours()).padStart(2, '0');\n"
    "    const mi = String(now.getMinutes()).padStart(2, '0');\n"
    "    task.completedAt = `${yy}-${mo}-${dd} ${hh}:${mi}`;\n"
    "  }\n"
    "  saveState();\n"
    "  rerenderAll();\n"
    "  showNotice(task.status === 'done' ? 'タスクを完了にしました。' : 'タスクを未完了に戻しました。');\n"
    "}"
)
assert old_toggle in app, "toggleTaskDone block not found"
app = app.replace(old_toggle, new_toggle)

# 2) renderTasks: hide completed tasks
old_render = (
    "function renderTasks() {\n"
    "  const pill = document.getElementById('taskCountPill');\n"
    "  if (pill) {\n"
    "    const openCount = state.tasks.filter((t) => t.status !== 'done').length;\n"
    "    pill.textContent = `${openCount}件未完了 / 全${state.tasks.length}件`;\n"
    "  }\n"
    "  const list = document.getElementById('taskList');\n"
    "  if (!list) return;\n"
    "  const sorted = sortTasksForView(state.tasks);\n"
    "  list.innerHTML = sorted.length\n"
    "    ? sorted.map((t) => renderTaskCard(t)).join('')\n"
    "    : '<div class=\"empty-state\">タスクはありません。＋ 新規から追加できます。</div>';\n"
    "}"
)
new_render = (
    "function renderTasks() {\n"
    "  const openTasks = state.tasks.filter((t) => t.status !== 'done');\n"
    "  const pill = document.getElementById('taskCountPill');\n"
    "  if (pill) {\n"
    "    pill.textContent = `${openTasks.length}件未完了`;\n"
    "  }\n"
    "  const list = document.getElementById('taskList');\n"
    "  if (!list) return;\n"
    "  const sorted = sortTasksForView(openTasks);\n"
    "  list.innerHTML = sorted.length\n"
    "    ? sorted.map((t) => renderTaskCard(t)).join('')\n"
    "    : '<div class=\"empty-state\">未完了のタスクはありません。＋ 新規から追加できます。</div>';\n"
    "}"
)
assert old_render in app, "renderTasks block not found"
app = app.replace(old_render, new_render)

# 3) home tasks list (top of home): also hide done tasks
old_home_tasks = (
    "  document.getElementById('homeTasks').innerHTML = sortTasksForView(state.tasks)\n"
    "    .slice(0, 6)\n"
    "    .map((t) => renderTaskCard(t, { compact: true }))\n"
    "    .join('') || '<div class=\"empty-state\">タスクはありません</div>';\n"
)
new_home_tasks = (
    "  document.getElementById('homeTasks').innerHTML = sortTasksForView(state.tasks.filter((t) => t.status !== 'done'))\n"
    "    .slice(0, 6)\n"
    "    .map((t) => renderTaskCard(t, { compact: true }))\n"
    "    .join('') || '<div class=\"empty-state\">未完了のタスクはありません</div>';\n"
)
assert old_home_tasks in app, "home tasks block not found"
app = app.replace(old_home_tasks, new_home_tasks)

# 4) Month calendar: completed tasks show on completedAt date, open tasks on due date
old_month_agg = (
    "  const taskByDate = {};\n"
    "  state.tasks.forEach((t) => {\n"
    "    const d = parseWhen(t.due);\n"
    "    if (!d) return;\n"
    "    const key = dateKey(d);\n"
    "    (taskByDate[key] = taskByDate[key] || []).push(t);\n"
    "  });\n"
)
new_month_agg = (
    "  const taskByDate = {};\n"
    "  state.tasks.forEach((t) => {\n"
    "    const src = t.status === 'done' ? (t.completedAt || t.due) : t.due;\n"
    "    const d = parseWhen(src);\n"
    "    if (!d) return;\n"
    "    const key = dateKey(d);\n"
    "    (taskByDate[key] = taskByDate[key] || []).push(t);\n"
    "  });\n"
)
assert old_month_agg in app, "month calendar aggregation block not found"
app = app.replace(old_month_agg, new_month_agg)

# 5) createInitialState demo tasks: ensure completedAt field exists (optional cosmetic)
# skip; existing entries will just have completedAt undefined which is fine

APP.write_text(app, encoding="utf-8")

# ---------- index.html ----------
html = HTML.read_text(encoding="utf-8")
html = html.replace('./styles.css?v=19', './styles.css?v=20')
html = html.replace('./app.js?v=19', './app.js?v=20')
HTML.write_text(html, encoding="utf-8")

print("OK")
