#!/usr/bin/env python3
"""Raise PDF attach limit + auto-slim on save + graceful storage fallback."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.js"
HTML = ROOT / "index.html"
CSS = ROOT / "styles.css"

app = APP.read_text(encoding="utf-8")

# 1) Raise per-PDF limit and add soft threshold for slim mode
old_const = "const TASK_PDF_MAX_BYTES = 5 * 1024 * 1024;"
new_const = (
    "const TASK_PDF_MAX_BYTES = 20 * 1024 * 1024;\n"
    "const TASK_PDF_SLIM_ABOVE = 4 * 1024 * 1024; // over this size, store link-only in localStorage\n"
    "const TASK_PDF_HARD_INLINE = 2 * 1024 * 1024; // safe inline limit for localStorage"
)
assert old_const in app
app = app.replace(old_const, new_const)

# 2) PDF picker: allow larger, and mark heavy PDFs for slim-save
old_pdf_handler = (
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
    "    });"
)
new_pdf_handler = (
    "    pdfInput.addEventListener('change', async (e) => {\n"
    "      const files = Array.from(e.target.files || []);\n"
    "      for (const file of files) {\n"
    "        if (taskEditPdfs.length >= TASK_ATTACH_MAX) {\n"
    "          showNotice(`PDFは最大${TASK_ATTACH_MAX}件までです。`, 'error');\n"
    "          break;\n"
    "        }\n"
    "        if (file.size > TASK_PDF_MAX_BYTES) {\n"
    "          showNotice(`${file.name} は${Math.floor(TASK_PDF_MAX_BYTES/1024/1024)}MBを超えています。`, 'error');\n"
    "          continue;\n"
    "        }\n"
    "        try {\n"
    "          const dataUrl = await readFileAsDataUrl(file);\n"
    "          const heavy = file.size >= TASK_PDF_HARD_INLINE;\n"
    "          taskEditPdfs.push({ name: file.name, size: file.size, dataUrl, heavy });\n"
    "          if (heavy) {\n"
    "            showNotice(`${file.name} は大きいため、この端末では今のセッションのみ表示されます。`, 'info');\n"
    "          }\n"
    "        } catch (err) {\n"
    "          console.error(err);\n"
    "          showNotice('PDFの読み込みに失敗しました。', 'error');\n"
    "        }\n"
    "      }\n"
    "      pdfInput.value = '';\n"
    "      renderTaskAttachments();\n"
    "    });"
)
assert old_pdf_handler in app
app = app.replace(old_pdf_handler, new_pdf_handler)

# 3) saveState fallback: try dropping PDF dataUrls (keep metadata) when full
old_save_end = (
    "    // 2) それでもダメなら、すべての投稿の画像を落とす\n"
    "    clone.posts = clone.posts.map((p) => ({ ...p, images: [] }));\n"
    "    if (trySetItem(JSON.stringify(clone))) {\n"
    "      state.posts = state.posts.map((p) => ({ ...p, images: [] }));\n"
    "      showNotice('容量上限のため、保存先の画像をすべて除外しました（表示は今のセッション中のみ）。', 'error');\n"
    "      return true;\n"
    "    }\n"
    "  }\n"
    "  showNotice('ブラウザの保存領域が一杯です。デモデータ初期化をお願いします。', 'error');\n"
    "  return false;\n"
    "}"
)
new_save_end = (
    "    // 2) それでもダメなら、すべての投稿の画像を落とす\n"
    "    clone.posts = clone.posts.map((p) => ({ ...p, images: [] }));\n"
    "    if (trySetItem(JSON.stringify(clone))) {\n"
    "      state.posts = state.posts.map((p) => ({ ...p, images: [] }));\n"
    "      showNotice('容量上限のため、保存先の画像をすべて除外しました（表示は今のセッション中のみ）。', 'error');\n"
    "      return true;\n"
    "    }\n"
    "  }\n"
    "\n"
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
    "\n"
    "  showNotice('ブラウザの保存領域が一杯です。不要なタスク・投稿を削除してください。', 'error');\n"
    "  return false;\n"
    "}"
)
assert old_save_end in app
app = app.replace(old_save_end, new_save_end)

# 4) PDF list rendering: show stored=name_only badge if dataUrl empty
old_list = (
    "    pdfList.innerHTML = taskEditPdfs.map((p, i) => `\n"
    "      <div class=\"task-attach-pdf\">\n"
    "        <span class=\"task-attach-pdf-ico\">📄</span>\n"
    "        <a class=\"task-attach-pdf-name\" href=\"${p.dataUrl}\" target=\"_blank\" rel=\"noopener\">${escapeHtml(p.name || 'document.pdf')}</a>\n"
    "        <span class=\"task-attach-pdf-size\">${formatFileSize(p.size || 0)}</span>\n"
    "        <button type=\"button\" class=\"task-attach-remove\" onclick=\"removeTaskPdf(${i})\" aria-label=\"削除\">×</button>\n"
    "      </div>\n"
    "    `).join('');\n"
)
new_list = (
    "    pdfList.innerHTML = taskEditPdfs.map((p, i) => {\n"
    "      const hasBody = !!p.dataUrl;\n"
    "      const nameHtml = hasBody\n"
    "        ? `<a class=\"task-attach-pdf-name\" href=\"${p.dataUrl}\" target=\"_blank\" rel=\"noopener\">${escapeHtml(p.name || 'document.pdf')}</a>`\n"
    "        : `<span class=\"task-attach-pdf-name muted\" title=\"本文は端末保存されていません。再添付で復元できます。\">${escapeHtml(p.name || 'document.pdf')} <span class=\"tag-muted\">名称のみ</span></span>`;\n"
    "      return `\n"
    "        <div class=\"task-attach-pdf\">\n"
    "          <span class=\"task-attach-pdf-ico\">📄</span>\n"
    "          ${nameHtml}\n"
    "          <span class=\"task-attach-pdf-size\">${formatFileSize(p.size || 0)}</span>\n"
    "          <button type=\"button\" class=\"task-attach-remove\" onclick=\"removeTaskPdf(${i})\" aria-label=\"削除\">×</button>\n"
    "        </div>\n"
    "      `;\n"
    "    }).join('');\n"
)
assert old_list in app
app = app.replace(old_list, new_list)

APP.write_text(app, encoding="utf-8")

# ---------- index.html ----------
html = HTML.read_text(encoding="utf-8")
html = html.replace('./styles.css?v=22', './styles.css?v=23')
html = html.replace('./app.js?v=22', './app.js?v=23')
HTML.write_text(html, encoding="utf-8")

# ---------- styles.css ----------
css = CSS.read_text(encoding="utf-8")
if ".tag-muted" not in css:
    css += (
        "\n.task-attach-pdf-name.muted { color: #64748b; font-weight: 700; }\n"
        ".tag-muted { display: inline-block; margin-left: 6px; padding: 1px 6px; border-radius: 6px; background: #f1f5f9; color: #64748b; font-size: 10px; font-weight: 800; }\n"
    )
CSS.write_text(css, encoding="utf-8")

print("OK")
