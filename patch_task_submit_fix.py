#!/usr/bin/env python3
"""Make task save robust: dedicated submitTaskEditor() with try/catch,
attached to both form submit and Save button click; safer id handling."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.js"
HTML = ROOT / "index.html"

app = APP.read_text(encoding="utf-8")

# 1) Replace old inline submit handler with a named function + safer logic
old_block = (
    "  const taskEditForm = document.getElementById('taskEditForm');\n"
    "  if (taskEditForm) taskEditForm.addEventListener('submit', (e) => {\n"
    "    e.preventDefault();\n"
    "    const id = document.getElementById('taskEditId').value;\n"
    "    document.getElementById('taskEditDue').value = readDateTime('taskEdit');\n"
    "    const payload = {\n"
    "      title: document.getElementById('taskEditTitleInput').value.trim(),\n"
    "      due: document.getElementById('taskEditDue').value.trim(),\n"
    "      status: document.getElementById('taskEditStatus').value,\n"
    "      priority: document.getElementById('taskEditPriority').value,\n"
    "      assignedTo: document.getElementById('taskEditAssignee').value.trim(),\n"
    "      customerId: document.getElementById('taskEditCustomer').value || null,\n"
    "      propertyId: document.getElementById('taskEditProperty').value || null,\n"
    "      memo: document.getElementById('taskEditMemo').value,\n"
    "      photos: taskEditPhotos.map((p) => ({ ...p })),\n"
    "      pdfs: taskEditPdfs.map((p) => ({ ...p }))\n"
    "    };\n"
    "    // stash full bodies in session cache for viewer usage after save\n"
    "    const _cacheId = id || null;\n"
    "    const _cachePhotos = taskEditPhotos.map((p) => ({ name: p.name, dataUrl: p.dataUrl }));\n"
    "    const _cachePdfs = taskEditPdfs.map((p) => ({ name: p.name, dataUrl: p.dataUrl }));\n"
    "    if (!payload.title) { showNotice('タイトルを入力してください。', 'error'); return; }\n"
    "    let _savedId = id;\n"
    "    let _wasCreate = false;\n"
    "    if (id) {\n"
    "      const t = state.tasks.find((x) => x.id === id);\n"
    "      if (t) {\n"
    "        Object.assign(t, payload);\n"
    "      } else {\n"
    "        // id が指定されていたが該当タスクが無い場合は新規作成扱い\n"
    "        const newId = uid('tk', state.tasks);\n"
    "        const created = { id: newId, sourcePostId: null, ...payload };\n"
    "        state.tasks.unshift(created);\n"
    "        _savedId = newId;\n"
    "        _wasCreate = true;\n"
    "      }\n"
    "    } else {\n"
    "      const newId = uid('tk', state.tasks);\n"
    "      const created = { id: newId, sourcePostId: null, ...payload };\n"
    "      state.tasks.unshift(created);\n"
    "      _savedId = newId;\n"
    "      _wasCreate = true;\n"
    "    }\n"
    "    if (_savedId) attachmentSessionCache[_savedId] = { photos: _cachePhotos, pdfs: _cachePdfs };\n"
    "    saveState();\n"
    "    rerenderAll();\n"
    "    showNotice(_wasCreate ? 'タスクを作成しました。' : 'タスクを更新しました。');\n"
    "    goBackFromEditor('tasks');\n"
    "  });"
)

new_block = (
    "  function submitTaskEditor(e) {\n"
    "    if (e && typeof e.preventDefault === 'function') e.preventDefault();\n"
    "    try {\n"
    "      const idEl = document.getElementById('taskEditId');\n"
    "      const id = idEl ? String(idEl.value || '').trim() : '';\n"
    "      const dueEl = document.getElementById('taskEditDue');\n"
    "      if (dueEl) dueEl.value = readDateTime('taskEdit');\n"
    "      const titleEl = document.getElementById('taskEditTitleInput');\n"
    "      const title = titleEl ? String(titleEl.value || '').trim() : '';\n"
    "      if (!title) { showNotice('タイトルを入力してください。', 'error'); if (titleEl) titleEl.focus(); return false; }\n"
    "      const payload = {\n"
    "        title: title,\n"
    "        due: (dueEl?.value || '').trim(),\n"
    "        status: document.getElementById('taskEditStatus')?.value || 'todo',\n"
    "        priority: document.getElementById('taskEditPriority')?.value || 'medium',\n"
    "        assignedTo: (document.getElementById('taskEditAssignee')?.value || '').trim(),\n"
    "        customerId: document.getElementById('taskEditCustomer')?.value || null,\n"
    "        propertyId: document.getElementById('taskEditProperty')?.value || null,\n"
    "        memo: document.getElementById('taskEditMemo')?.value || '',\n"
    "        photos: (Array.isArray(taskEditPhotos) ? taskEditPhotos : []).map((p) => ({ ...p })),\n"
    "        pdfs: (Array.isArray(taskEditPdfs) ? taskEditPdfs : []).map((p) => ({ ...p }))\n"
    "      };\n"
    "      const _cachePhotos = (Array.isArray(taskEditPhotos) ? taskEditPhotos : []).map((p) => ({ name: p.name, dataUrl: p.dataUrl }));\n"
    "      const _cachePdfs = (Array.isArray(taskEditPdfs) ? taskEditPdfs : []).map((p) => ({ name: p.name, dataUrl: p.dataUrl }));\n"
    "      let _savedId = id;\n"
    "      let _wasCreate = false;\n"
    "      if (id) {\n"
    "        const t = state.tasks.find((x) => x && x.id === id);\n"
    "        if (t) {\n"
    "          Object.assign(t, payload);\n"
    "        } else {\n"
    "          const newId = uid('tk', state.tasks);\n"
    "          state.tasks.unshift({ id: newId, sourcePostId: null, ...payload });\n"
    "          _savedId = newId;\n"
    "          _wasCreate = true;\n"
    "        }\n"
    "      } else {\n"
    "        const newId = uid('tk', state.tasks);\n"
    "        state.tasks.unshift({ id: newId, sourcePostId: null, ...payload });\n"
    "        _savedId = newId;\n"
    "        _wasCreate = true;\n"
    "      }\n"
    "      if (_savedId) attachmentSessionCache[_savedId] = { photos: _cachePhotos, pdfs: _cachePdfs };\n"
    "      saveState();\n"
    "      rerenderAll();\n"
    "      showNotice(_wasCreate ? 'タスクを作成しました。' : 'タスクを更新しました。');\n"
    "      goBackFromEditor('tasks');\n"
    "      return true;\n"
    "    } catch (err) {\n"
    "      console.error('submitTaskEditor error', err);\n"
    "      showNotice('保存に失敗しました: ' + (err && err.message ? err.message : String(err)), 'error');\n"
    "      return false;\n"
    "    }\n"
    "  }\n"
    "  window.submitTaskEditor = submitTaskEditor;\n"
    "\n"
    "  const taskEditForm = document.getElementById('taskEditForm');\n"
    "  if (taskEditForm && !taskEditForm.dataset.bound) {\n"
    "    taskEditForm.dataset.bound = '1';\n"
    "    taskEditForm.addEventListener('submit', submitTaskEditor);\n"
    "    // Backup: bind explicit click on the save button too (in case submit is blocked)\n"
    "    const saveBtn = taskEditForm.querySelector('button[type=\"submit\"]');\n"
    "    if (saveBtn) saveBtn.addEventListener('click', (ev) => { ev.preventDefault(); submitTaskEditor(ev); });\n"
    "  }"
)

assert old_block in app, "old submit block not found"
app = app.replace(old_block, new_block)

# 2) Guard: if state.tasks is undefined for some reason, coerce to []
old_guard = "let _savedId = id;"
# just leave — new block above already checks state.tasks

APP.write_text(app, encoding="utf-8")

# Cache bust
html = HTML.read_text(encoding="utf-8")
html = html.replace('./styles.css?v=26', './styles.css?v=27')
html = html.replace('./app.js?v=26', './app.js?v=27')
HTML.write_text(html, encoding="utf-8")

print("OK")
