#!/usr/bin/env python3
"""Add photo(5) + PDF(5) attachments to task memo."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.js"
HTML = ROOT / "index.html"
CSS = ROOT / "styles.css"

# ---------- index.html ----------
html = HTML.read_text(encoding="utf-8")

old_memo = (
    '              <label class="task-memo-label"><span>メモ</span><textarea name="memo" id="taskEditMemo" class="task-memo-area" rows="10" placeholder="メモとして自由に書けます。改行そのまま保存されます。&#10;・箇条書き&#10;・電話メモ&#10;・関連URLなど"></textarea></label>\n'
)
new_memo = (
    '              <label class="task-memo-label"><span>メモ</span><textarea name="memo" id="taskEditMemo" class="task-memo-area" rows="10" placeholder="メモとして自由に書けます。改行そのまま保存されます。&#10;・箇条書き&#10;・電話メモ&#10;・関連URLなど"></textarea></label>\n'
    '              <div class="task-attach-section">\n'
    '                <div class="task-attach-block">\n'
    '                  <div class="task-attach-head">\n'
    '                    <span class="task-attach-title">写真</span>\n'
    '                    <span class="task-attach-count" id="taskPhotoCount">0 / 5</span>\n'
    '                    <label class="secondary-btn small task-attach-btn">\n'
    '                      <span>写真を追加</span>\n'
    '                      <input type="file" id="taskPhotoInput" accept="image/*" multiple hidden />\n'
    '                    </label>\n'
    '                  </div>\n'
    '                  <div class="task-attach-grid" id="taskPhotoGrid"></div>\n'
    '                </div>\n'
    '                <div class="task-attach-block">\n'
    '                  <div class="task-attach-head">\n'
    '                    <span class="task-attach-title">PDF</span>\n'
    '                    <span class="task-attach-count" id="taskPdfCount">0 / 5</span>\n'
    '                    <label class="secondary-btn small task-attach-btn">\n'
    '                      <span>PDFを追加</span>\n'
    '                      <input type="file" id="taskPdfInput" accept="application/pdf" multiple hidden />\n'
    '                    </label>\n'
    '                  </div>\n'
    '                  <div class="task-attach-list" id="taskPdfList"></div>\n'
    '                </div>\n'
    '              </div>\n'
)
assert old_memo in html
html = html.replace(old_memo, new_memo)

html = html.replace('./styles.css?v=20', './styles.css?v=21')
html = html.replace('./app.js?v=20', './app.js?v=21')
HTML.write_text(html, encoding="utf-8")

# ---------- app.js ----------
app = APP.read_text(encoding="utf-8")

# 1) editor working buffers (module-level state for the currently-open task editor)
inject_buffers = (
    "\n// Task editor attachment buffers (per-open editing session)\n"
    "let taskEditPhotos = [];\n"
    "let taskEditPdfs = [];\n"
    "const TASK_ATTACH_MAX = 5;\n"
    "const TASK_PDF_MAX_BYTES = 5 * 1024 * 1024;\n"
    "\n"
    "function renderTaskAttachments() {\n"
    "  const photoGrid = document.getElementById('taskPhotoGrid');\n"
    "  const pdfList = document.getElementById('taskPdfList');\n"
    "  const photoCount = document.getElementById('taskPhotoCount');\n"
    "  const pdfCount = document.getElementById('taskPdfCount');\n"
    "  if (photoCount) photoCount.textContent = `${taskEditPhotos.length} / ${TASK_ATTACH_MAX}`;\n"
    "  if (pdfCount) pdfCount.textContent = `${taskEditPdfs.length} / ${TASK_ATTACH_MAX}`;\n"
    "  if (photoGrid) {\n"
    "    photoGrid.innerHTML = taskEditPhotos.map((p, i) => `\n"
    "      <div class=\"task-attach-photo\">\n"
    "        <img src=\"${p.dataUrl}\" alt=\"${escapeHtml(p.name || 'photo')}\" />\n"
    "        <button type=\"button\" class=\"task-attach-remove\" onclick=\"removeTaskPhoto(${i})\" aria-label=\"削除\">×</button>\n"
    "      </div>\n"
    "    `).join('');\n"
    "  }\n"
    "  if (pdfList) {\n"
    "    pdfList.innerHTML = taskEditPdfs.map((p, i) => `\n"
    "      <div class=\"task-attach-pdf\">\n"
    "        <span class=\"task-attach-pdf-ico\">📄</span>\n"
    "        <a class=\"task-attach-pdf-name\" href=\"${p.dataUrl}\" target=\"_blank\" rel=\"noopener\">${escapeHtml(p.name || 'document.pdf')}</a>\n"
    "        <span class=\"task-attach-pdf-size\">${formatFileSize(p.size || 0)}</span>\n"
    "        <button type=\"button\" class=\"task-attach-remove\" onclick=\"removeTaskPdf(${i})\" aria-label=\"削除\">×</button>\n"
    "      </div>\n"
    "    `).join('');\n"
    "  }\n"
    "}\n"
    "window.renderTaskAttachments = renderTaskAttachments;\n"
    "\n"
    "function removeTaskPhoto(index) {\n"
    "  taskEditPhotos.splice(index, 1);\n"
    "  renderTaskAttachments();\n"
    "}\n"
    "window.removeTaskPhoto = removeTaskPhoto;\n"
    "\n"
    "function removeTaskPdf(index) {\n"
    "  taskEditPdfs.splice(index, 1);\n"
    "  renderTaskAttachments();\n"
    "}\n"
    "window.removeTaskPdf = removeTaskPdf;\n"
    "\n"
    "function formatFileSize(bytes) {\n"
    "  if (!bytes) return '';\n"
    "  if (bytes < 1024) return `${bytes} B`;\n"
    "  if (bytes < 1024 * 1024) return `${(bytes/1024).toFixed(1)} KB`;\n"
    "  return `${(bytes/1024/1024).toFixed(2)} MB`;\n"
    "}\n"
    "\n"
    "function setupTaskAttachmentPickers() {\n"
    "  const photoInput = document.getElementById('taskPhotoInput');\n"
    "  if (photoInput && !photoInput.dataset.bound) {\n"
    "    photoInput.dataset.bound = '1';\n"
    "    photoInput.addEventListener('change', async (e) => {\n"
    "      const files = Array.from(e.target.files || []);\n"
    "      for (const file of files) {\n"
    "        if (taskEditPhotos.length >= TASK_ATTACH_MAX) {\n"
    "          showNotice(`写真は最大${TASK_ATTACH_MAX}枚までです。`, 'error');\n"
    "          break;\n"
    "        }\n"
    "        try {\n"
    "          const dataUrl = await fileToCompressedDataUrl(file);\n"
    "          taskEditPhotos.push({ name: file.name, size: dataUrl.length, dataUrl });\n"
    "        } catch (err) {\n"
    "          console.error(err);\n"
    "          showNotice('写真の読み込みに失敗しました。', 'error');\n"
    "        }\n"
    "      }\n"
    "      photoInput.value = '';\n"
    "      renderTaskAttachments();\n"
    "    });\n"
    "  }\n"
    "  const pdfInput = document.getElementById('taskPdfInput');\n"
    "  if (pdfInput && !pdfInput.dataset.bound) {\n"
    "    pdfInput.dataset.bound = '1';\n"
    "    pdfInput.addEventListener('change', async (e) => {\n"
    "      const files = Array.from(e.target.files || []);\n"
    "      for (const file of files) {\n"
    "        if (taskEditPdfs.length >= TASK_ATTACH_MAX) {\n"
    "          showNotice(`PDFは最大${TASK_ATTACH_MAX}件までです。`, 'error');\n"
    "          break;\n"
    "        }\n"
    "        if (file.size > TASK_PDF_MAX_BYTES) {\n"
    "          showNotice(`${file.name} は5MBを超えています。`, 'error');\n"
    "          continue;\n"
    "        }\n"
    "        try {\n"
    "          const dataUrl = await readFileAsDataUrl(file);\n"
    "          taskEditPdfs.push({ name: file.name, size: file.size, dataUrl });\n"
    "        } catch (err) {\n"
    "          console.error(err);\n"
    "          showNotice('PDFの読み込みに失敗しました。', 'error');\n"
    "        }\n"
    "      }\n"
    "      pdfInput.value = '';\n"
    "      renderTaskAttachments();\n"
    "    });\n"
    "  }\n"
    "}\n"
    "window.setupTaskAttachmentPickers = setupTaskAttachmentPickers;\n"
)

anchor = "function openTaskEditor(taskId, presetDateKey) {"
assert anchor in app
app = app.replace(anchor, inject_buffers + "\n" + anchor)

# 2) load photos/pdfs into buffers when opening editor
old_open_end = (
    "  document.getElementById('taskEditMemo').value = task?.memo || '';\n"
    "  editorReturnScreen = document.querySelector('.screen.active')?.id?.replace('screen-','') || 'home';\n"
    "  go('task-edit');\n"
    "}"
)
new_open_end = (
    "  document.getElementById('taskEditMemo').value = task?.memo || '';\n"
    "  taskEditPhotos = Array.isArray(task?.photos) ? task.photos.map((p) => ({ ...p })) : [];\n"
    "  taskEditPdfs = Array.isArray(task?.pdfs) ? task.pdfs.map((p) => ({ ...p })) : [];\n"
    "  renderTaskAttachments();\n"
    "  setupTaskAttachmentPickers();\n"
    "  editorReturnScreen = document.querySelector('.screen.active')?.id?.replace('screen-','') || 'home';\n"
    "  go('task-edit');\n"
    "}"
)
assert old_open_end in app
app = app.replace(old_open_end, new_open_end)

# 3) Save attachments with task on submit
old_submit_payload = (
    "    const payload = {\n"
    "      title: document.getElementById('taskEditTitleInput').value.trim(),\n"
    "      due: document.getElementById('taskEditDue').value.trim(),\n"
    "      status: document.getElementById('taskEditStatus').value,\n"
    "      priority: document.getElementById('taskEditPriority').value,\n"
    "      assignedTo: document.getElementById('taskEditAssignee').value.trim(),\n"
    "      customerId: document.getElementById('taskEditCustomer').value || null,\n"
    "      propertyId: document.getElementById('taskEditProperty').value || null,\n"
    "      memo: document.getElementById('taskEditMemo').value\n"
    "    };"
)
new_submit_payload = (
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
    "    };"
)
assert old_submit_payload in app
app = app.replace(old_submit_payload, new_submit_payload)

# 4) card preview: show a small attachment badge if any
old_memo_line = (
    "        ${memoPreview ? `<div class=\"todo-memo-preview\">${memoPreview}</div>` : ''}\n"
)
new_memo_line = (
    "        ${memoPreview ? `<div class=\"todo-memo-preview\">${memoPreview}</div>` : ''}\n"
    "        ${(task.photos?.length || task.pdfs?.length) ? `<div class=\"todo-attach-preview\">${task.photos?.length ? `📷×${task.photos.length}` : ''}${task.photos?.length && task.pdfs?.length ? '  ' : ''}${task.pdfs?.length ? `📄×${task.pdfs.length}` : ''}</div>` : ''}\n"
)
assert old_memo_line in app
app = app.replace(old_memo_line, new_memo_line)

# 5) Storage safety: writing large data URLs may exceed localStorage — best-effort try/catch already in saveState.
APP.write_text(app, encoding="utf-8")

# ---------- styles.css ----------
css = CSS.read_text(encoding="utf-8")
add_css = """

/* ---------- Task memo attachments ---------- */
.task-attach-section {
  display: grid;
  gap: 14px;
  margin-top: 4px;
}
.task-attach-block {
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 10px 12px;
  background: #ffffff;
}
.task-attach-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.task-attach-title {
  font-size: 13px;
  font-weight: 800;
  color: #0f172a;
}
.task-attach-count {
  font-size: 12px;
  color: #64748b;
  font-weight: 700;
}
.task-attach-btn {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}
.task-attach-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(84px, 1fr));
  gap: 8px;
}
.task-attach-photo {
  position: relative;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  overflow: hidden;
  background: #0b1220;
  border: 1px solid var(--line);
}
.task-attach-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.task-attach-remove {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: none;
  background: rgba(15, 23, 42, 0.75);
  color: #ffffff;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  display: grid;
  place-items: center;
  padding: 0;
}
.task-attach-list {
  display: grid;
  gap: 6px;
}
.task-attach-pdf {
  position: relative;
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: #f8fafc;
}
.task-attach-pdf .task-attach-remove {
  position: static;
  background: transparent;
  color: #b91c1c;
  border: 1px solid #fecaca;
  font-size: 16px;
  width: 24px;
  height: 24px;
}
.task-attach-pdf-ico {
  font-size: 18px;
}
.task-attach-pdf-name {
  color: #1d4ed8;
  font-weight: 700;
  font-size: 13px;
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.task-attach-pdf-size {
  font-size: 11px;
  color: #64748b;
}

.todo-attach-preview {
  font-size: 11px;
  color: #475569;
  font-weight: 700;
  margin-top: 2px;
}
"""
if "/* ---------- Task memo attachments ---------- */" not in css:
    css += add_css
CSS.write_text(css, encoding="utf-8")

print("OK")
