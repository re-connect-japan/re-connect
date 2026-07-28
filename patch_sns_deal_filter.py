#!/usr/bin/env python3
"""Add deal-type (sale/rental/all) filter to SNS feed."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.js"
HTML = ROOT / "index.html"
CSS = ROOT / "styles.css"

# ---------- index.html ----------
html = HTML.read_text(encoding="utf-8")

old_tabs = (
    '          <div class="feed-tabs" id="feedTabs">\n'
    '            <button class="feed-tab active" data-feed="all">すべて</button>\n'
    '            <button class="feed-tab" data-feed="broker_group_only">業者</button>\n'
    '            <button class="feed-tab" data-feed="store_only">店舗</button>\n'
    '            <button class="feed-tab" data-feed="internal_only">社内</button>\n'
    '          </div>\n'
)
new_tabs = (
    '          <div class="feed-tabs" id="feedTabs">\n'
    '            <button class="feed-tab active" data-feed="all">すべて</button>\n'
    '            <button class="feed-tab" data-feed="broker_group_only">業者</button>\n'
    '            <button class="feed-tab" data-feed="store_only">店舗</button>\n'
    '            <button class="feed-tab" data-feed="internal_only">社内</button>\n'
    '          </div>\n'
    '          <div class="feed-deal-tabs" id="feedDealTabs">\n'
    '            <button type="button" class="feed-deal-tab active" data-deal="all">両方</button>\n'
    '            <button type="button" class="feed-deal-tab" data-deal="sale">売買</button>\n'
    '            <button type="button" class="feed-deal-tab" data-deal="rental">賃貸</button>\n'
    '          </div>\n'
)
assert old_tabs in html
html = html.replace(old_tabs, new_tabs)

# cache bust
html = html.replace('./styles.css?v=18', './styles.css?v=19')
html = html.replace('./app.js?v=18', './app.js?v=19')

HTML.write_text(html, encoding="utf-8")

# ---------- app.js ----------
app = APP.read_text(encoding="utf-8")

# 1) add activeFeedDeal state
app = app.replace(
    "    activeFeed: 'all',\n",
    "    activeFeed: 'all',\n    activeFeedDeal: 'all',\n",
    1,
)

# 2) migrate stored state on load: ensure activeFeedDeal exists
migrate_anchor = "      state.posts = state.posts.map((p) => ({ ...p, images: [] }));"
if migrate_anchor in app and "activeFeedDeal" not in app.split(migrate_anchor)[0].split("createInitialState")[-1]:
    pass  # already ensured above

# safety: ensure key exists after loadState too
load_fix = "if (state && typeof state.activeFeedDeal === 'undefined') state.activeFeedDeal = 'all';"
if load_fix not in app:
    app = app.replace(
        "function saveState()",
        load_fix + "\nfunction saveState()",
        1,
    )

# 3) update renderFeed to also filter by deal type
old_render = (
    "function renderFeed(targetId, limit) {\n"
    "  const container = document.getElementById(targetId);\n"
    "  if (!container) return;\n"
    "  let items = state.posts;\n"
    "  if (targetId === 'snsFeed' && state.activeFeed !== 'all') {\n"
    "    items = items.filter((p) => p.visibilityCode === state.activeFeed);\n"
    "  }\n"
    "  const list = limit ? items.slice(0, limit) : items;\n"
    "  container.innerHTML = list.map(feedItemHtml).join('') || '<div class=\"empty-state\">投稿はありません</div>';\n"
    "}"
)
new_render = (
    "function renderFeed(targetId, limit) {\n"
    "  const container = document.getElementById(targetId);\n"
    "  if (!container) return;\n"
    "  let items = state.posts;\n"
    "  if (targetId === 'snsFeed') {\n"
    "    if (state.activeFeed !== 'all') {\n"
    "      items = items.filter((p) => p.visibilityCode === state.activeFeed);\n"
    "    }\n"
    "    const deal = state.activeFeedDeal || 'all';\n"
    "    if (deal === 'sale' || deal === 'rental') {\n"
    "      items = items.filter((p) => {\n"
    "        const prop = getProperty(p.propertyId);\n"
    "        return prop && prop.dealType === deal;\n"
    "      });\n"
    "    }\n"
    "  }\n"
    "  const list = limit ? items.slice(0, limit) : items;\n"
    "  container.innerHTML = list.map(feedItemHtml).join('') || '<div class=\"empty-state\">投稿はありません</div>';\n"
    "}"
)
assert old_render in app
app = app.replace(old_render, new_render)

# 4) update renderFeedTabs to also toggle deal tabs
old_tabs_fn = (
    "function renderFeedTabs() {\n"
    "  document.querySelectorAll('.feed-tab').forEach((btn) => {\n"
    "    btn.classList.toggle('active', btn.dataset.feed === state.activeFeed);\n"
    "  });\n"
    "}"
)
new_tabs_fn = (
    "function renderFeedTabs() {\n"
    "  document.querySelectorAll('.feed-tab').forEach((btn) => {\n"
    "    btn.classList.toggle('active', btn.dataset.feed === state.activeFeed);\n"
    "  });\n"
    "  const deal = state.activeFeedDeal || 'all';\n"
    "  document.querySelectorAll('.feed-deal-tab').forEach((btn) => {\n"
    "    btn.classList.toggle('active', btn.dataset.deal === deal);\n"
    "  });\n"
    "}"
)
assert old_tabs_fn in app
app = app.replace(old_tabs_fn, new_tabs_fn)

# 5) wire deal tab click events near existing feed-tab handler
old_click = (
    "  document.querySelectorAll('.feed-tab').forEach((btn) => btn.addEventListener('click', () => {\n"
    "    state.activeFeed = btn.dataset.feed;\n"
    "    saveState();\n"
    "    renderFeed('snsFeed');\n"
    "    renderFeedTabs();\n"
    "  }));"
)
new_click = (
    "  document.querySelectorAll('.feed-tab').forEach((btn) => btn.addEventListener('click', () => {\n"
    "    state.activeFeed = btn.dataset.feed;\n"
    "    saveState();\n"
    "    renderFeed('snsFeed');\n"
    "    renderFeedTabs();\n"
    "  }));\n"
    "\n"
    "  document.querySelectorAll('.feed-deal-tab').forEach((btn) => btn.addEventListener('click', () => {\n"
    "    state.activeFeedDeal = btn.dataset.deal;\n"
    "    saveState();\n"
    "    renderFeed('snsFeed');\n"
    "    renderFeedTabs();\n"
    "  }));"
)
assert old_click in app
app = app.replace(old_click, new_click)

APP.write_text(app, encoding="utf-8")

# ---------- styles.css ----------
css = CSS.read_text(encoding="utf-8")
add_css = """

/* ---------- SNS deal-type filter tabs ---------- */
.feed-deal-tabs {
  display: inline-flex;
  gap: 4px;
  padding: 4px;
  margin: 6px 0 10px;
  border-radius: 999px;
  background: #eef2ff;
  border: 1px solid #c7d2fe;
}
.feed-deal-tab {
  border: none;
  background: transparent;
  color: #3730a3;
  font-size: 12px;
  font-weight: 800;
  padding: 6px 14px;
  border-radius: 999px;
  cursor: pointer;
  min-height: 32px;
}
.feed-deal-tab.active {
  background: #ffffff;
  color: #1d4ed8;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08);
}
"""
if "/* ---------- SNS deal-type filter tabs ---------- */" not in css:
    css += add_css
CSS.write_text(css, encoding="utf-8")

print("OK")
