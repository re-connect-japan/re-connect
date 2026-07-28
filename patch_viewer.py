#!/usr/bin/env python3
"""Tap-to-view single-page viewers for photos & PDFs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.js"
HTML = ROOT / "index.html"
CSS = ROOT / "styles.css"

# ---------- index.html ----------
html = HTML.read_text(encoding="utf-8")

viewer_section = (
    '\n        <section id="screen-viewer" class="screen viewer-screen">\n'
    '          <div class="viewer-topbar">\n'
    '            <button type="button" class="viewer-back" onclick="closeViewer()" aria-label="閉じる">‹ 戻る</button>\n'
    '            <div class="viewer-title" id="viewerTitle">表示</div>\n'
    '            <a class="viewer-open" id="viewerOpenBtn" href="#" target="_blank" rel="noopener">別タブで開く</a>\n'
    '          </div>\n'
    '          <div class="viewer-body" id="viewerBody"></div>\n'
    '        </section>\n'
)

anchor = '        <section id="screen-messages" class="screen">'
assert anchor in html
if 'id="screen-viewer"' not in html:
    html = html.replace(anchor, viewer_section + "\n" + anchor)

# cache bust
html = html.replace('./styles.css?v=23', './styles.css?v=24')
html = html.replace('./app.js?v=23', './app.js?v=24')
HTML.write_text(html, encoding="utf-8")

# ---------- app.js ----------
app = APP.read_text(encoding="utf-8")

# 1) Rewrite renderTaskAttachments to make photos tappable + PDFs open in viewer
old_render_attach_start = "function renderTaskAttachments() {"
assert old_render_attach_start in app

old_photo_block = (
    "    photoGrid.innerHTML = taskEditPhotos.map((p, i) => `\n"
    "      <div class=\"task-attach-photo\">\n"
    "        <img src=\"${p.dataUrl}\" alt=\"${escapeHtml(p.name || 'photo')}\" />\n"
    "        <button type=\"button\" class=\"task-attach-remove\" onclick=\"removeTaskPhoto(${i})\" aria-label=\"削除\">×</button>\n"
    "      </div>\n"
    "    `).join('');\n"
)
new_photo_block = (
    "    photoGrid.innerHTML = taskEditPhotos.map((p, i) => `\n"
    "      <div class=\"task-attach-photo\">\n"
    "        <img src=\"${p.dataUrl}\" alt=\"${escapeHtml(p.name || 'photo')}\" onclick=\"openPhotoViewer('task', ${i})\" />\n"
    "        <button type=\"button\" class=\"task-attach-remove\" onclick=\"event.stopPropagation(); removeTaskPhoto(${i})\" aria-label=\"削除\">×</button>\n"
    "      </div>\n"
    "    `).join('');\n"
)
assert old_photo_block in app
app = app.replace(old_photo_block, new_photo_block)

old_pdf_block = (
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
new_pdf_block = (
    "    pdfList.innerHTML = taskEditPdfs.map((p, i) => {\n"
    "      const hasBody = !!p.dataUrl;\n"
    "      const nameHtml = hasBody\n"
    "        ? `<button type=\"button\" class=\"task-attach-pdf-name link\" onclick=\"openPdfViewer('task', ${i})\">${escapeHtml(p.name || 'document.pdf')}</button>`\n"
    "        : `<span class=\"task-attach-pdf-name muted\" title=\"本文は端末保存されていません。再添付で復元できます。\">${escapeHtml(p.name || 'document.pdf')} <span class=\"tag-muted\">名称のみ</span></span>`;\n"
    "      return `\n"
    "        <div class=\"task-attach-pdf\">\n"
    "          <span class=\"task-attach-pdf-ico\">📄</span>\n"
    "          ${nameHtml}\n"
    "          <span class=\"task-attach-pdf-size\">${formatFileSize(p.size || 0)}</span>\n"
    "          <button type=\"button\" class=\"task-attach-remove\" onclick=\"event.stopPropagation(); removeTaskPdf(${i})\" aria-label=\"削除\">×</button>\n"
    "        </div>\n"
    "      `;\n"
    "    }).join('');\n"
)
assert old_pdf_block in app
app = app.replace(old_pdf_block, new_pdf_block)

# 2) Add viewer implementation before rerenderAll
viewer_impl = '''
let viewerReturnScreen = 'home';

function dataUrlToBlobUrl(dataUrl) {
  try {
    if (!dataUrl || !dataUrl.startsWith('data:')) return dataUrl;
    const [meta, b64] = dataUrl.split(',');
    const mimeMatch = /data:([^;]+);base64/.exec(meta);
    const mime = mimeMatch ? mimeMatch[1] : 'application/octet-stream';
    const bin = atob(b64);
    const len = bin.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) bytes[i] = bin.charCodeAt(i);
    const blob = new Blob([bytes], { type: mime });
    return URL.createObjectURL(blob);
  } catch (err) {
    console.error('dataUrl->blob failed', err);
    return dataUrl;
  }
}

let _currentBlobUrl = '';
function _revokeCurrentBlob() {
  if (_currentBlobUrl) {
    try { URL.revokeObjectURL(_currentBlobUrl); } catch(e) {}
    _currentBlobUrl = '';
  }
}

function _getAttach(kind, source, index) {
  if (source === 'task') {
    if (kind === 'photo') return taskEditPhotos[index];
    if (kind === 'pdf') return taskEditPdfs[index];
  }
  return null;
}

function openPhotoViewer(source, index) {
  const item = _getAttach('photo', source, index);
  if (!item || !item.dataUrl) {
    showNotice('画像が見つかりません。', 'error');
    return;
  }
  _revokeCurrentBlob();
  viewerReturnScreen = document.querySelector('.screen.active')?.id?.replace('screen-','') || 'tasks';
  const titleEl = document.getElementById('viewerTitle');
  const body = document.getElementById('viewerBody');
  const openBtn = document.getElementById('viewerOpenBtn');
  if (titleEl) titleEl.textContent = item.name || '写真';
  if (openBtn) { openBtn.href = item.dataUrl; openBtn.style.display = ''; }
  if (body) {
    body.innerHTML = `
      <div class="viewer-image-wrap">
        <img class="viewer-image" src="${item.dataUrl}" alt="${escapeHtml(item.name || 'photo')}" />
      </div>
    `;
  }
  go('viewer');
}
window.openPhotoViewer = openPhotoViewer;

function openPdfViewer(source, index) {
  const item = _getAttach('pdf', source, index);
  if (!item || !item.dataUrl) {
    showNotice('PDF本文が保存されていません。再添付してください。', 'error');
    return;
  }
  _revokeCurrentBlob();
  viewerReturnScreen = document.querySelector('.screen.active')?.id?.replace('screen-','') || 'tasks';
  const blobUrl = dataUrlToBlobUrl(item.dataUrl);
  _currentBlobUrl = blobUrl && blobUrl !== item.dataUrl ? blobUrl : '';
  const titleEl = document.getElementById('viewerTitle');
  const body = document.getElementById('viewerBody');
  const openBtn = document.getElementById('viewerOpenBtn');
  if (titleEl) titleEl.textContent = item.name || 'PDF';
  if (openBtn) { openBtn.href = blobUrl; openBtn.style.display = ''; }
  if (body) {
    body.innerHTML = `
      <iframe class="viewer-pdf" src="${blobUrl}#view=FitH" title="${escapeHtml(item.name || 'PDF')}"></iframe>
      <div class="viewer-pdf-fallback">
        <p>PDFがうまく表示されない場合は、右上の「別タブで開く」を押してください。</p>
        <a class="secondary-btn" href="${blobUrl}" download="${escapeHtml(item.name || 'document.pdf')}">ダウンロード</a>
      </div>
    `;
  }
  go('viewer');
}
window.openPdfViewer = openPdfViewer;

function closeViewer() {
  _revokeCurrentBlob();
  const body = document.getElementById('viewerBody');
  if (body) body.innerHTML = '';
  go(viewerReturnScreen || 'home');
}
window.closeViewer = closeViewer;
'''

anchor2 = "function rerenderAll() {"
assert anchor2 in app
if "function openPhotoViewer" not in app:
    app = app.replace(anchor2, viewer_impl + "\n" + anchor2)

APP.write_text(app, encoding="utf-8")

# ---------- styles.css ----------
css = CSS.read_text(encoding="utf-8")
add_css = """

/* ---------- Attachment viewer ---------- */
.viewer-screen {
  display: none;
  padding: 0;
}
.viewer-screen.active {
  display: flex;
  flex-direction: column;
  gap: 0;
  height: calc(100vh - var(--safe-bottom) - 64px);
  min-height: 60vh;
}
.viewer-topbar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  background: #ffffff;
  position: sticky;
  top: 0;
  z-index: 5;
}
.viewer-back {
  border: none;
  background: transparent;
  color: var(--brand);
  font-weight: 800;
  font-size: 14px;
  cursor: pointer;
  padding: 6px 8px;
}
.viewer-title {
  flex: 1;
  font-size: 14px;
  font-weight: 800;
  color: #0f172a;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.viewer-open {
  font-size: 12px;
  font-weight: 800;
  color: var(--brand);
  text-decoration: none;
  padding: 6px 10px;
  border: 1px solid #bfdbfe;
  border-radius: 999px;
  background: #eff6ff;
}
.viewer-body {
  flex: 1;
  overflow: auto;
  background: #0b1220;
  display: flex;
  flex-direction: column;
}
.viewer-image-wrap {
  flex: 1;
  display: grid;
  place-items: center;
  padding: 12px;
  background: #0b1220;
  min-height: 60vh;
}
.viewer-image {
  max-width: 100%;
  max-height: 82vh;
  object-fit: contain;
  display: block;
  background: #0b1220;
  touch-action: pinch-zoom;
}
.viewer-pdf {
  flex: 1;
  width: 100%;
  min-height: 70vh;
  border: none;
  background: #ffffff;
}
.viewer-pdf-fallback {
  background: #ffffff;
  padding: 12px 14px;
  border-top: 1px solid var(--line);
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  font-size: 13px;
  color: #475569;
}
.task-attach-pdf-name.link {
  border: none;
  background: transparent;
  color: #1d4ed8;
  font-weight: 700;
  font-size: 13px;
  text-align: left;
  padding: 0;
  cursor: pointer;
  text-decoration: underline;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.task-attach-photo img {
  cursor: zoom-in;
}
"""
if "/* ---------- Attachment viewer ---------- */" not in css:
    css += add_css
CSS.write_text(css, encoding="utf-8")

print("OK")
