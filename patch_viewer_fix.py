#!/usr/bin/env python3
"""Fix: PDF unopenable after save & photo viewer not showing."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.js"
HTML = ROOT / "index.html"
CSS = ROOT / "styles.css"

app = APP.read_text(encoding="utf-8")

# --- 1) saveState: DO NOT mutate in-memory state; only trim the persisted clone.
old_save_block = (
    "  // 3) 大きいPDF本文を落として名前だけ残す (自動スリム化)\n"
    "  if (Array.isArray(clone.tasks)) {\n"
    "    const trimClone = JSON.parse(JSON.stringify(state));\n"
    "    let stripped = 0;\n"
    "    trimClone.tasks = (trimClone.tasks || []).map((t) => {\n"
    "      if (Array.isArray(t.pdfs)) {\n"
    "        t.pdfs = t.pdfs.map((p) => {\n"
    "          if (p && p.dataUrl && ((p.size || 0) >= TASK_PDF_HARD_INLINE || p.heavy)) {\n"
    "            stripped++;\n"
    "            return { name: p.name, size: p.size, dataUrl: '', heavy: true, stored: 'name_only' };\n"
    "          }\n"
    "          return p;\n"
    "        });\n"
    "      }\n"
    "      return t;\n"
    "    });\n"
    "    if (stripped && trySetItem(JSON.stringify(trimClone))) {\n"
    "      state.tasks = trimClone.tasks;\n"
    "      showNotice(`容量上限のため、大きいPDF ${stripped} 件は名称のみ保存しました。`, 'error');\n"
    "      return true;\n"
    "    }\n"
    "    // 4) 最終手段: すべてのPDF本文を除外\n"
    "    trimClone.tasks = (trimClone.tasks || []).map((t) => ({\n"
    "      ...t,\n"
    "      pdfs: Array.isArray(t.pdfs) ? t.pdfs.map((p) => ({ name: p?.name, size: p?.size, dataUrl: '', stored: 'name_only' })) : t.pdfs\n"
    "    }));\n"
    "    if (trySetItem(JSON.stringify(trimClone))) {\n"
    "      state.tasks = trimClone.tasks;\n"
    "      showNotice('容量上限のため、すべてのPDF本文を除外して名称のみ保存しました。', 'error');\n"
    "      return true;\n"
    "    }\n"
    "  }\n"
)
new_save_block = (
    "  // 3) 大きいPDF/写真本文は永続保存だけ軽量化 (メモリは保持したまま)\n"
    "  if (Array.isArray(clone.tasks)) {\n"
    "    const trimClone = JSON.parse(JSON.stringify(state));\n"
    "    let strippedPdf = 0;\n"
    "    let strippedPhoto = 0;\n"
    "    trimClone.tasks = (trimClone.tasks || []).map((t) => {\n"
    "      if (Array.isArray(t.pdfs)) {\n"
    "        t.pdfs = t.pdfs.map((p) => {\n"
    "          if (p && p.dataUrl && ((p.size || 0) >= TASK_PDF_HARD_INLINE || p.heavy)) {\n"
    "            strippedPdf++;\n"
    "            return { name: p.name, size: p.size, dataUrl: '', heavy: true, stored: 'name_only' };\n"
    "          }\n"
    "          return p;\n"
    "        });\n"
    "      }\n"
    "      return t;\n"
    "    });\n"
    "    if ((strippedPdf || strippedPhoto) && trySetItem(JSON.stringify(trimClone))) {\n"
    "      showNotice(`容量上限のため、大きいPDF ${strippedPdf} 件は端末には名称のみ保存しました (今のセッション中は開けます)。`, 'error');\n"
    "      return true;\n"
    "    }\n"
    "    // 4) 最終手段: 永続保存からPDF/写真本文をすべて除外 (メモリは保持)\n"
    "    trimClone.tasks = (trimClone.tasks || []).map((t) => ({\n"
    "      ...t,\n"
    "      pdfs: Array.isArray(t.pdfs) ? t.pdfs.map((p) => ({ name: p?.name, size: p?.size, dataUrl: '', stored: 'name_only' })) : t.pdfs,\n"
    "      photos: Array.isArray(t.photos) ? t.photos.map((p) => ({ name: p?.name, size: p?.size, dataUrl: '', stored: 'name_only' })) : t.photos\n"
    "    }));\n"
    "    if (trySetItem(JSON.stringify(trimClone))) {\n"
    "      showNotice('容量上限のため、添付本文は端末保存から除外しました (今のセッション中は開けます)。', 'error');\n"
    "      return true;\n"
    "    }\n"
    "  }\n"
)
assert old_save_block in app
app = app.replace(old_save_block, new_save_block)

# --- 2) When opening the task editor, merge in-memory buffers if the current task matches
old_open_block = (
    "  taskEditPhotos = Array.isArray(task?.photos) ? task.photos.map((p) => ({ ...p })) : [];\n"
    "  taskEditPdfs = Array.isArray(task?.pdfs) ? task.pdfs.map((p) => ({ ...p })) : [];\n"
)
new_open_block = (
    "  taskEditPhotos = Array.isArray(task?.photos) ? task.photos.map((p) => ({ ...p })) : [];\n"
    "  taskEditPdfs = Array.isArray(task?.pdfs) ? task.pdfs.map((p) => ({ ...p })) : [];\n"
    "  // Fill missing dataUrl from session-only cache when available\n"
    "  if (task?.id && attachmentSessionCache[task.id]) {\n"
    "    const cache = attachmentSessionCache[task.id];\n"
    "    taskEditPhotos = taskEditPhotos.map((p, i) => (!p.dataUrl && cache.photos?.[i]?.dataUrl && cache.photos[i].name === p.name) ? { ...p, dataUrl: cache.photos[i].dataUrl } : p);\n"
    "    taskEditPdfs = taskEditPdfs.map((p, i) => (!p.dataUrl && cache.pdfs?.[i]?.dataUrl && cache.pdfs[i].name === p.name) ? { ...p, dataUrl: cache.pdfs[i].dataUrl } : p);\n"
    "  }\n"
)
assert old_open_block in app
app = app.replace(old_open_block, new_open_block)

# --- 3) Add session cache & save it on submit
inject_cache = (
    "\n// Session-only cache: keeps attachment bodies even when localStorage saved them as name-only.\n"
    "const attachmentSessionCache = {};\n"
)
if "attachmentSessionCache" not in app:
    app = app.replace(
        "let taskEditPhotos = [];",
        inject_cache + "\nlet taskEditPhotos = [];",
        1,
    )

# --- 4) On submit, remember the full bodies for this session, keyed by task id
old_submit_after = (
    "      photos: taskEditPhotos.map((p) => ({ ...p })),\n"
    "      pdfs: taskEditPdfs.map((p) => ({ ...p }))\n"
    "    };"
)
new_submit_after = (
    "      photos: taskEditPhotos.map((p) => ({ ...p })),\n"
    "      pdfs: taskEditPdfs.map((p) => ({ ...p }))\n"
    "    };\n"
    "    // stash full bodies in session cache for viewer usage after save\n"
    "    const _cacheId = id || null;\n"
    "    const _cachePhotos = taskEditPhotos.map((p) => ({ name: p.name, dataUrl: p.dataUrl }));\n"
    "    const _cachePdfs = taskEditPdfs.map((p) => ({ name: p.name, dataUrl: p.dataUrl }));"
)
assert old_submit_after in app
app = app.replace(old_submit_after, new_submit_after)

# after the assign / unshift, write to cache
old_assign = (
    "    if (id) {\n"
    "      const t = state.tasks.find((x) => x.id === id);\n"
    "      if (t) Object.assign(t, payload);\n"
    "    } else {\n"
    "      state.tasks.unshift({ id: uid('tk', state.tasks), sourcePostId: null, ...payload });\n"
    "    }"
)
new_assign = (
    "    let _savedId = id;\n"
    "    if (id) {\n"
    "      const t = state.tasks.find((x) => x.id === id);\n"
    "      if (t) Object.assign(t, payload);\n"
    "    } else {\n"
    "      const created = { id: uid('tk', state.tasks), sourcePostId: null, ...payload };\n"
    "      state.tasks.unshift(created);\n"
    "      _savedId = created.id;\n"
    "    }\n"
    "    if (_savedId) attachmentSessionCache[_savedId] = { photos: _cachePhotos, pdfs: _cachePdfs };"
)
assert old_assign in app
app = app.replace(old_assign, new_assign)

# --- 5) Viewer screen: force display when active (override generic .screen)
APP.write_text(app, encoding="utf-8")

# ---------- styles.css ----------
css = CSS.read_text(encoding="utf-8")
old_viewer_css = (
    ".viewer-screen {\n"
    "  display: none;\n"
    "  padding: 0;\n"
    "}\n"
    ".viewer-screen.active {\n"
    "  display: flex;\n"
    "  flex-direction: column;\n"
    "  gap: 0;\n"
    "  height: calc(100vh - var(--safe-bottom) - 64px);\n"
    "  min-height: 60vh;\n"
    "}\n"
)
new_viewer_css = (
    "#screen-viewer.viewer-screen { padding: 0; }\n"
    "#screen-viewer.viewer-screen.active {\n"
    "  display: flex !important;\n"
    "  flex-direction: column;\n"
    "  gap: 0;\n"
    "  min-height: 70vh;\n"
    "}\n"
    "#screen-viewer.viewer-screen:not(.active) { display: none !important; }\n"
)
assert old_viewer_css in css
css = css.replace(old_viewer_css, new_viewer_css)

# viewer-body should not force column background over image
css = css.replace(
    ".viewer-body {\n"
    "  flex: 1;\n"
    "  overflow: auto;\n"
    "  background: #0b1220;\n"
    "  display: flex;\n"
    "  flex-direction: column;\n"
    "}\n",
    ".viewer-body {\n"
    "  flex: 1;\n"
    "  overflow: auto;\n"
    "  background: #0b1220;\n"
    "  display: flex;\n"
    "  flex-direction: column;\n"
    "  min-height: 60vh;\n"
    "}\n"
)

CSS.write_text(css, encoding="utf-8")

# ---------- index.html cache bust ----------
html = HTML.read_text(encoding="utf-8")
html = html.replace('./styles.css?v=24', './styles.css?v=25')
html = html.replace('./app.js?v=24', './app.js?v=25')
HTML.write_text(html, encoding="utf-8")

print("OK")
