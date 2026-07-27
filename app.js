const STORAGE_KEY = 'reconnect_mvp_state_v2';

const DEMO_USERS = {
  admin: { id: 'u_admin', name: '鈴木', role: 'admin', email: 'admin@reconnect.local' },
  manager: { id: 'u_manager', name: '佐藤', role: 'manager', email: 'manager@reconnect.local' },
  sales: { id: 'u_sales', name: '田中', role: 'sales', email: 'sales@reconnect.local' },
  office: { id: 'u_office', name: '高橋', role: 'office', email: 'office@reconnect.local' }
};

function createInitialState() {
  return {
    session: null,
    role: 'sales',
    selectedTaskId: 'tk_001',
    lastDocumentHtml: '',
    notifications: [
      { id: 'nt_001', type: 'task_due_soon', title: '期限前通知', body: '比較資料送付の期限が近づいています', unread: true, priority: 'high' },
      { id: 'nt_002', type: 'comment', title: 'コメント通知', body: '価格改定共有にコメントが付きました', unread: true, priority: 'medium' },
      { id: 'nt_003', type: 'result_missing', title: '結果未入力', body: '予定完了後の結果入力が未完了です', unread: false, priority: 'high' }
    ],
    customers: [
      { id: 'cu_001', name: '山田様', owner: '田中', budget: '5,000万〜5,800万', needs: '駅近 / 2LDK / 収納重視', nextAction: '別物件提案', heat: 'high' },
      { id: 'cu_002', name: '中村様', owner: '田中', budget: '4,000万台', needs: '価格重視 / ペット可', nextAction: '価格交渉面談', heat: 'medium' }
    ],
    properties: [
      { id: 'pr_001', title: '港区マンション G', price: '5,480万円', layout: '2LDK', features: '収納多い / 再販案件 / 反響4件', status: '価格改定中' },
      { id: 'pr_002', title: '港南レジデンス 402', price: '5,480万円', layout: '2LDK', features: '収納重視 / 最適候補', status: '提案候補' },
      { id: 'pr_003', title: '白金タワー 1103', price: '5,620万円', layout: '2LDK', features: '駅近 / 比較候補', status: '提案候補' },
      { id: 'pr_004', title: '芝浦コート 805', price: '5,390万円', layout: '2LDK', features: '価格重視 / 補欠候補', status: '提案候補' }
    ],
    posts: [
      { id: 'sp_001', title: '価格改定共有 / 港区マンション G', visibility: 'グループ業者のみ', visibilityCode: 'broker_group_only', author: '田中', unread: 3, body: '価格改定に伴い再販開始前の共有を行います。', customerId: 'cu_001', propertyId: 'pr_001' },
      { id: 'sp_002', title: '内見結果共有', visibility: '店舗内', visibilityCode: 'store_only', author: '田中', unread: 0, body: '収納量に懸念あり。別物件提案へ進めます。', customerId: 'cu_001', propertyId: 'pr_001' }
    ],
    tasks: [
      { id: 'tk_001', title: '比較資料送付', status: 'doing', priority: 'high', due: '今日 10:00', customerId: 'cu_001', propertyId: 'pr_001', sourcePostId: 'sp_001', assignedTo: '田中' },
      { id: 'tk_002', title: '鍵手配確認', status: 'todo', priority: 'medium', due: '今日 13:00', customerId: 'cu_001', propertyId: 'pr_001', sourcePostId: null, assignedTo: '田中' }
    ],
    schedules: [
      { id: 'sc_001', title: '再内見候補確定', status: 'planned', when: '今日 11:00', customerId: 'cu_001', propertyId: 'pr_001', sync: 'Google / iPhone queued', resultStatus: '', memo: '' },
      { id: 'sc_002', title: '価格会議', status: 'planned', when: '今日 15:00', customerId: null, propertyId: 'pr_001', sync: '未同期', resultStatus: '', memo: '' }
    ]
  };
}

let state = loadState();

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : createInitialState();
  } catch {
    return createInitialState();
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function resetState() {
  state = createInitialState();
  saveState();
}

function uid(prefix, list) {
  return `${prefix}_${String(list.length + 1).padStart(3, '0')}`;
}

function getCustomer(id) {
  return state.customers.find((x) => x.id === id) || null;
}

function getProperty(id) {
  return state.properties.find((x) => x.id === id) || null;
}

function visibilityLabel(code) {
  return ({
    store_only: '店舗内',
    internal_only: '社内のみ',
    broker_group_only: 'グループ業者のみ',
    public: '一般公開'
  })[code] || code;
}

function roleLabel(role) {
  return ({ admin: '管理者', manager: '管理職', sales: '営業', office: '事務' })[role] || role;
}

function can(action) {
  const role = state.role;
  const rules = {
    viewAll: ['admin', 'manager'],
    createPublicPost: ['admin'],
    reassignTask: ['admin', 'manager'],
    saveCloud: ['admin', 'manager', 'sales', 'office'],
    addCustomer: ['admin', 'manager', 'sales', 'office'],
    addProperty: ['admin', 'manager', 'sales'],
    exportDocument: ['admin', 'manager', 'sales'],
    markResult: ['admin', 'manager', 'sales']
  };
  return (rules[action] || []).includes(role);
}

function showNotice(message, type = 'success') {
  const el = document.getElementById('globalNotice');
  if (!el) return;
  el.textContent = message;
  el.classList.remove('hidden');
  el.style.borderColor = type === 'error' ? '#fca5a5' : '#86efac';
  el.style.background = type === 'error' ? '#fef2f2' : '#ecfdf5';
  el.style.color = type === 'error' ? '#991b1b' : '#166534';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function requirePermission(action, message) {
  if (can(action)) return true;
  showNotice(message, 'error');
  return false;
}

function go(screenId) {
  document.querySelectorAll('.screen').forEach((el) => el.classList.remove('active'));
  const target = document.getElementById(`screen-${screenId}`);
  if (target) target.classList.add('active');
  document.querySelectorAll('.nav-btn').forEach((btn) => btn.classList.toggle('active', btn.dataset.screen === screenId));
}

function updateUserSummary() {
  const session = state.session || DEMO_USERS[state.role];
  document.getElementById('userSummary').textContent = `${session.name} / ${roleLabel(state.role)} / ${session.email}`;
  document.getElementById('roleSelect').value = state.role;
}

function fillSelect(selectId, items, formatter, includeBlank = false) {
  const el = document.getElementById(selectId);
  if (!el) return;
  el.innerHTML = '';
  if (includeBlank) {
    const blank = document.createElement('option');
    blank.value = '';
    blank.textContent = '未選択';
    el.appendChild(blank);
  }
  items.forEach((item) => {
    const opt = document.createElement('option');
    opt.value = item.id;
    opt.textContent = formatter(item);
    el.appendChild(opt);
  });
}

function populateLinkedSelects() {
  fillSelect('snsCustomerSelect', state.customers, (c) => c.name);
  fillSelect('snsPropertySelect', state.properties, (p) => `${p.title} / ${p.price}`);
  fillSelect('documentCustomerSelect', state.customers, (c) => c.name);
  fillSelect('documentBasePropertySelect', state.properties, (p) => `${p.title} / ${p.price}`);
  fillSelect('candidateASelect', state.properties, (p) => `${p.title} / ${p.price}`);
  fillSelect('candidateBSelect', state.properties, (p) => `${p.title} / ${p.price}`);
  fillSelect('resultScheduleSelect', state.schedules, (s) => `${s.when} / ${s.title}`);
  document.getElementById('candidateASelect').value = state.properties[1]?.id || state.properties[0]?.id || '';
  document.getElementById('candidateBSelect').value = state.properties[2]?.id || state.properties[0]?.id || '';
  document.getElementById('documentBasePropertySelect').value = state.properties[0]?.id || '';
}

function renderHome() {
  const unreadCount = state.notifications.filter((n) => n.unread).length;
  const highHeat = state.customers.filter((c) => c.heat === 'high').length;
  document.getElementById('homeKpis').innerHTML = [
    { label: '本日予定', value: state.schedules.length, sub: '結果未入力を含む' },
    { label: '今日期限タスク', value: state.tasks.length, sub: '主導線を維持' },
    { label: 'SNS未読', value: unreadCount, sub: 'コメント / メンション' },
    { label: '優先顧客', value: highHeat, sub: '再提案含む' }
  ].map((kpi) => `
    <div class="metric-card">
      <div class="metric-label">${kpi.label}</div>
      <div class="metric-value">${kpi.value}</div>
      <div class="metric-sub">${kpi.sub}</div>
    </div>
  `).join('');

  document.getElementById('todayTasks').innerHTML = state.tasks.map((task) => {
    const customer = getCustomer(task.customerId);
    const property = getProperty(task.propertyId);
    return `
      <div class="item">
        <div class="item-title">${task.due} ${task.title}</div>
        <div class="item-sub">${customer?.name || '-'} / ${property?.title || '-'} / ${task.status}</div>
        <div class="top-meta"><span class="chip ${task.priority === 'high' ? 'active' : ''}">${task.priority}</span></div>
      </div>
    `;
  }).join('');

  document.getElementById('priorityCases').innerHTML = state.customers.map((customer) => `
    <div class="item">
      <div class="item-title">${customer.name}</div>
      <div class="item-sub">担当: ${customer.owner} / 予算: ${customer.budget}</div>
      <div class="top-meta">
        <span class="tag ${customer.heat === 'high' ? 'danger' : 'warning'}">${customer.nextAction}</span>
      </div>
    </div>
  `).join('');
}

function renderCustomers() {
  document.getElementById('customerCountPill').textContent = `${state.customers.length}件`;
  document.getElementById('customerList').innerHTML = state.customers.map((customer) => `
    <div class="item">
      <div class="item-title">${customer.name}</div>
      <div class="item-sub">担当: ${customer.owner} / 予算: ${customer.budget}</div>
      <div class="item-sub">条件: ${customer.needs}</div>
      <div class="top-meta">
        <span class="tag ${customer.heat === 'high' ? 'danger' : 'warning'}">${customer.nextAction}</span>
      </div>
    </div>
  `).join('');
}

function renderProperties() {
  document.getElementById('propertyCountPill').textContent = `${state.properties.length}件`;
  document.getElementById('propertyList').innerHTML = state.properties.map((property) => `
    <div class="item">
      <div class="item-title">${property.title}</div>
      <div class="item-sub">${property.price} / ${property.layout}</div>
      <div class="item-sub">${property.features}</div>
      <div class="top-meta"><span class="chip">${property.status}</span></div>
    </div>
  `).join('');
}

function renderPosts() {
  document.getElementById('snsUnreadPill').textContent = `未読 ${state.posts.reduce((sum, p) => sum + (p.unread || 0), 0)}`;
  document.getElementById('snsPosts').innerHTML = state.posts.map((post) => {
    const customer = getCustomer(post.customerId);
    const property = getProperty(post.propertyId);
    return `
      <div class="item">
        <div class="item-title">${post.title}</div>
        <div class="item-sub">公開範囲: ${post.visibility} / 投稿者: ${post.author}</div>
        <div class="item-sub">顧客: ${customer?.name || '-'} / 物件: ${property?.title || '-'}</div>
        <div class="item-sub">${post.body}</div>
        <div class="top-meta">
          ${post.unread ? `<span class="chip active">未読 ${post.unread}</span>` : ''}
          <span class="chip">${visibilityLabel(post.visibilityCode)}</span>
        </div>
        <div class="actions">
          <button class="primary-btn" onclick="createTaskFromPost('${post.id}')">タスク化</button>
        </div>
      </div>
    `;
  }).join('');
}

function renderTasks() {
  document.getElementById('taskCountPill').textContent = `${state.tasks.length}件`;
  document.getElementById('taskList').innerHTML = state.tasks.map((task) => {
    const customer = getCustomer(task.customerId);
    return `
      <div class="item" onclick="selectTask('${task.id}')" style="cursor:pointer; ${task.id === state.selectedTaskId ? 'border-color:#2563eb;background:#eff6ff;' : ''}">
        <div class="item-title">${task.title}</div>
        <div class="item-sub">${task.status} / ${task.priority} / ${task.due}</div>
        <div class="item-sub">${customer?.name || '-'} / 担当: ${task.assignedTo}</div>
      </div>
    `;
  }).join('');

  const task = state.tasks.find((t) => t.id === state.selectedTaskId) || state.tasks[0];
  if (!task) {
    document.getElementById('taskDetail').innerHTML = '<div class="empty-state">タスクがありません。</div>';
    return;
  }
  const customer = getCustomer(task.customerId);
  const property = getProperty(task.propertyId);
  document.getElementById('taskDetail').innerHTML = `
    <div class="task-detail">
      <div class="item-title">${task.title}</div>
      <p>状態: ${task.status}</p>
      <p>優先度: ${task.priority}</p>
      <p>担当: ${task.assignedTo}</p>
      <p>顧客: ${customer?.name || '-'}</p>
      <p>物件: ${property?.title || '-'}</p>
      <div class="actions">
        <button class="secondary-btn" onclick="markTaskDone('${task.id}')">完了にする</button>
        <button class="primary-btn" onclick="createScheduleFromTask('${task.id}')">予定化する</button>
      </div>
      ${can('reassignTask') ? '<div class="permission-note">管理職以上は他担当への再割当実装を追加しやすい構成です。</div>' : ''}
    </div>
  `;
}

function renderSchedules() {
  document.getElementById('scheduleCountPill').textContent = `${state.schedules.length}件`;
  document.getElementById('scheduleList').innerHTML = state.schedules.map((schedule) => {
    const customer = getCustomer(schedule.customerId);
    const property = getProperty(schedule.propertyId);
    return `
      <div class="item">
        <div class="item-title">${schedule.when} ${schedule.title}</div>
        <div class="item-sub">${customer?.name || '-'} / ${property?.title || '-'} / ${schedule.status}</div>
        <div class="top-meta">
          <span class="chip">${schedule.sync}</span>
          ${schedule.resultStatus ? `<span class="tag success">結果: ${schedule.resultStatus}</span>` : ''}
        </div>
      </div>
    `;
  }).join('');
}

function renderDocumentPreview() {
  const root = document.getElementById('documentPreview');
  if (!state.lastDocumentHtml) {
    root.className = 'document-preview empty-state';
    root.textContent = '比較資料を生成するとここに表示されます。';
    return;
  }
  root.className = 'document-preview';
  root.innerHTML = state.lastDocumentHtml;
}

function renderNotifications() {
  document.getElementById('notificationList').innerHTML = state.notifications.map((n) => `
    <div class="notice-item ${n.unread ? 'unread' : ''}">
      <div class="item-title">${n.title}</div>
      <div class="item-sub">${n.body}</div>
      <div class="top-meta">
        <span class="tag ${n.priority === 'high' ? 'danger' : 'warning'}">${n.type}</span>
        ${n.unread ? '<span class="chip active">未読</span>' : '<span class="chip">既読</span>'}
      </div>
      <div class="actions">
        ${n.unread ? `<button class="secondary-btn" onclick="markRead('${n.id}')">既読にする</button>` : ''}
      </div>
    </div>
  `).join('');
}

function selectTask(id) {
  state.selectedTaskId = id;
  saveState();
  renderTasks();
}
window.selectTask = selectTask;

function createTaskFromPost(postId) {
  const post = state.posts.find((p) => p.id === postId);
  if (!post) return;
  const customer = getCustomer(post.customerId);
  const newTask = {
    id: uid('tk', state.tasks),
    title: `${customer?.name || '顧客'}へ対応`,
    status: 'todo',
    priority: 'high',
    due: '明日 10:00',
    customerId: post.customerId,
    propertyId: post.propertyId,
    sourcePostId: post.id,
    assignedTo: state.session?.name || '田中'
  };
  state.tasks.unshift(newTask);
  state.selectedTaskId = newTask.id;
  state.notifications.unshift({ id: uid('nt', state.notifications), type: 'task_assigned', title: 'タスク作成', body: 'SNS投稿からタスクを作成しました', unread: true, priority: 'medium' });
  saveState();
  rerenderAll();
  showNotice('投稿からタスクを作成しました。顧客・物件を自動引継ぎしています。');
  go('tasks');
}
window.createTaskFromPost = createTaskFromPost;

function markTaskDone(taskId) {
  const task = state.tasks.find((t) => t.id === taskId);
  if (!task) return;
  task.status = 'done';
  saveState();
  rerenderAll();
  showNotice('タスクを完了にしました。');
}
window.markTaskDone = markTaskDone;

function createScheduleFromTask(taskId) {
  const task = state.tasks.find((t) => t.id === taskId);
  if (!task) return;
  const newSchedule = {
    id: uid('sc', state.schedules),
    title: `${task.title} 商談`,
    status: 'planned',
    when: '明日 11:00',
    customerId: task.customerId,
    propertyId: task.propertyId,
    sync: 'Google / iPhone queued',
    resultStatus: '',
    memo: ''
  };
  state.schedules.unshift(newSchedule);
  state.notifications.unshift({ id: uid('nt', state.notifications), type: 'schedule_reminder', title: '予定作成', body: 'タスクから予定を作成しました', unread: true, priority: 'medium' });
  saveState();
  rerenderAll();
  showNotice('予定を作成しました。Google / iPhone 同期待ちです。');
  go('calendar');
}
window.createScheduleFromTask = createScheduleFromTask;

function markRead(id) {
  const item = state.notifications.find((n) => n.id === id);
  if (item) item.unread = false;
  saveState();
  rerenderAll();
}
window.markRead = markRead;

function markAllRead() {
  state.notifications.forEach((n) => { n.unread = false; });
  saveState();
  rerenderAll();
  showNotice('通知を一括既読にしました。');
}

function applyRole(role) {
  state.role = role;
  if (state.session) state.session.role = role;
  updateUserSummary();
  applyPermissionUI();
  saveState();
  showNotice(`ロールを「${roleLabel(role)}」に切り替えました。`);
}

function applyPermissionUI() {
  const visibility = document.querySelector('#snsForm select[name="visibility"]');
  if (visibility) {
    Array.from(visibility.options).forEach((opt) => { opt.hidden = false; });
    const publicOpt = Array.from(visibility.options).find((o) => o.value === 'public');
    if (publicOpt && !can('createPublicPost')) {
      publicOpt.hidden = true;
      if (visibility.value === 'public') visibility.value = 'internal_only';
    }
  }
  const propertyFormBtn = document.querySelector('#propertyForm button[type="submit"]');
  if (propertyFormBtn) propertyFormBtn.disabled = !can('addProperty');
  const docPrint = document.getElementById('printDocumentBtn');
  if (docPrint) docPrint.disabled = !can('exportDocument');
}

function login(role) {
  const user = { ...DEMO_USERS[role] };
  state.session = user;
  state.role = role;
  saveState();
  document.getElementById('loginScreen').classList.add('hidden');
  document.getElementById('appShell').classList.remove('hidden');
  updateUserSummary();
  applyPermissionUI();
  rerenderAll();
  showNotice(`${roleLabel(role)}としてログインしました。`);
}

function logout() {
  state.session = null;
  saveState();
  document.getElementById('appShell').classList.add('hidden');
  document.getElementById('loginScreen').classList.remove('hidden');
}

function createDocumentPreview({ customer, base, candidateA, candidateB, comment, destination }) {
  return `
    <div>
      <div class="item-title">比較資料プレビュー</div>
      <p>${customer.name} 向け / 保存先: ${destination}</p>
      <table class="doc-table">
        <thead>
          <tr><th>項目</th><th>基準物件</th><th>比較A</th><th>比較B</th></tr>
        </thead>
        <tbody>
          <tr><td>物件名</td><td>${base.title}</td><td>${candidateA.title}</td><td>${candidateB.title}</td></tr>
          <tr><td>価格</td><td>${base.price}</td><td>${candidateA.price}</td><td>${candidateB.price}</td></tr>
          <tr><td>間取り</td><td>${base.layout}</td><td>${candidateA.layout}</td><td>${candidateB.layout}</td></tr>
          <tr><td>特徴</td><td>${base.features}</td><td>${candidateA.features}</td><td>${candidateB.features}</td></tr>
        </tbody>
      </table>
      <p><strong>営業コメント:</strong> ${comment}</p>
      <p>生成フロー: 別物件提案 → 比較資料作成 → ブラウザ印刷/PDF保存 → クラウド保存想定</p>
    </div>
  `;
}

function printDocument() {
  if (!requirePermission('exportDocument', 'このロールではPDF出力できません。')) return;
  if (!state.lastDocumentHtml) {
    showNotice('先に資料を生成してください。', 'error');
    return;
  }
  const win = window.open('', '_blank');
  win.document.write(`<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><title>比較資料</title><style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:24px;color:#111827}table{width:100%;border-collapse:collapse;margin-top:12px}th,td{border:1px solid #d1d5db;padding:8px;text-align:left;vertical-align:top}th{background:#eff6ff}</style></head><body>${state.lastDocumentHtml}</body></html>`);
  win.document.close();
  win.focus();
  win.print();
}

function rerenderAll() {
  populateLinkedSelects();
  renderHome();
  renderCustomers();
  renderProperties();
  renderPosts();
  renderTasks();
  renderSchedules();
  renderDocumentPreview();
  renderNotifications();
}

function initEvents() {
  document.querySelectorAll('.nav-btn').forEach((btn) => btn.addEventListener('click', () => go(btn.dataset.screen)));
  document.querySelectorAll('[data-screen-link]').forEach((btn) => btn.addEventListener('click', () => go(btn.dataset.screenLink)));

  document.getElementById('demoAccount').addEventListener('change', (e) => {
    const user = DEMO_USERS[e.target.value];
    document.getElementById('loginEmail').value = user.email;
  });

  document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const role = document.getElementById('demoAccount').value;
    login(role);
  });

  document.getElementById('resetDataBtn').addEventListener('click', () => {
    resetState();
    showNotice('デモデータを初期化しました。');
    if (state.session) rerenderAll();
  });

  document.getElementById('logoutBtn').addEventListener('click', logout);
  document.getElementById('roleSelect').addEventListener('change', (e) => applyRole(e.target.value));
  document.getElementById('markAllReadBtn').addEventListener('click', markAllRead);
  document.getElementById('printDocumentBtn').addEventListener('click', printDocument);

  document.getElementById('customerForm').addEventListener('submit', (e) => {
    e.preventDefault();
    if (!requirePermission('addCustomer', 'このロールでは顧客追加できません。')) return;
    const form = new FormData(e.target);
    state.customers.unshift({
      id: uid('cu', state.customers),
      name: form.get('name'),
      owner: form.get('owner'),
      budget: form.get('budget'),
      needs: form.get('needs'),
      nextAction: '初回追客',
      heat: 'medium'
    });
    saveState();
    e.target.reset();
    rerenderAll();
    showNotice('顧客を追加しました。');
  });

  document.getElementById('propertyForm').addEventListener('submit', (e) => {
    e.preventDefault();
    if (!requirePermission('addProperty', 'このロールでは物件追加できません。')) return;
    const form = new FormData(e.target);
    state.properties.unshift({
      id: uid('pr', state.properties),
      title: form.get('title'),
      price: form.get('price'),
      layout: form.get('layout'),
      features: form.get('features'),
      status: '新規登録'
    });
    saveState();
    e.target.reset();
    rerenderAll();
    showNotice('物件を追加しました。');
  });

  document.getElementById('snsForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const visibilityCode = form.get('visibility');
    if (visibilityCode === 'public' && !requirePermission('createPublicPost', '一般公開は管理者のみ可能です。')) return;
    state.posts.unshift({
      id: uid('sp', state.posts),
      title: form.get('title'),
      visibility: visibilityLabel(visibilityCode),
      visibilityCode,
      author: state.session?.name || '田中',
      unread: 0,
      body: form.get('body'),
      customerId: form.get('customerId'),
      propertyId: form.get('propertyId')
    });
    saveState();
    rerenderAll();
    showNotice('SNS投稿を保存しました。');
  });

  document.getElementById('resultForm').addEventListener('submit', (e) => {
    e.preventDefault();
    if (!requirePermission('markResult', 'このロールでは結果登録できません。')) return;
    const form = new FormData(e.target);
    const schedule = state.schedules.find((s) => s.id === form.get('scheduleId'));
    if (!schedule) return;
    schedule.status = 'done';
    schedule.resultStatus = form.get('resultStatus');
    schedule.memo = form.get('memo');
    const customer = getCustomer(schedule.customerId);
    if (customer) {
      customer.nextAction = form.get('resultStatus') === 're_propose' ? '別物件提案' : '追客継続';
      customer.heat = form.get('resultStatus') === 'positive' ? 'high' : 'medium';
    }
    state.notifications.unshift({ id: uid('nt', state.notifications), type: 'result_registered', title: '結果登録完了', body: '予定結果を登録しました', unread: true, priority: 'medium' });
    saveState();
    rerenderAll();
    showNotice('結果を登録しました。次回対応へ進めます。');
  });

  document.getElementById('documentForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const customer = getCustomer(form.get('customerId'));
    const base = getProperty(form.get('basePropertyId'));
    const candidateA = getProperty(form.get('candidateA'));
    const candidateB = getProperty(form.get('candidateB'));
    if (!customer || !base || !candidateA || !candidateB) {
      showNotice('資料作成に必要な顧客・物件を選択してください。', 'error');
      return;
    }
    state.lastDocumentHtml = createDocumentPreview({
      customer,
      base,
      candidateA,
      candidateB,
      comment: form.get('comment'),
      destination: form.get('destination')
    });
    state.notifications.unshift({ id: uid('nt', state.notifications), type: 'document_ready', title: '資料作成完了', body: '比較資料プレビューを生成しました', unread: true, priority: 'medium' });
    saveState();
    rerenderAll();
    showNotice('比較資料を生成しました。ブラウザ印刷からPDF保存できます。');
  });
}

function init() {
  initEvents();
  if (state.session) {
    document.getElementById('loginScreen').classList.add('hidden');
    document.getElementById('appShell').classList.remove('hidden');
    updateUserSummary();
    applyPermissionUI();
    rerenderAll();
  } else {
    document.getElementById('loginEmail').value = DEMO_USERS.sales.email;
  }
}

document.addEventListener('DOMContentLoaded', init);