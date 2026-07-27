const STORAGE_KEY = 'reconnect_mvp_state_v4';

const DEFAULT_USER = { id: 'u_me', name: '田中' };

function createInitialState() {
  return {
    session: null,
    role: 'sales',
    selectedTaskId: 'tk_001',
    lastDocumentHtml: '',
    activeFeed: 'all',
    activeThreadId: 'th_001',
    notifications: [
      { id: 'nt_001', type: 'task_due_soon', title: '期限前通知', body: '比較資料送付の期限が近づいています', unread: true, priority: 'high' },
      { id: 'nt_002', type: 'comment', title: 'コメント通知', body: '価格改定共有にコメントが付きました', unread: true, priority: 'medium' },
      { id: 'nt_003', type: 'result_missing', title: '結果未入力', body: '予定完了後の結果入力が未完了です', unread: false, priority: 'high' }
    ],
    customers: [
      { id: 'cu_001', name: '山田様', owner: '田中', budget: '5,000万〜5,800万', needs: '駅近 / 2LDK / 収納重視', nextAction: '別物件提案', heat: 'high' },
      { id: 'cu_002', name: '中村様', owner: '田中', budget: '賃料18万円以内', needs: 'ペット可 / 2人入居 / 駅徒歩10分以内', nextAction: '内見候補調整', heat: 'medium' }
    ],
    properties: [
      {
        id: 'pr_001', customerId: 'cu_001', dealType: 'sale', title: '港区マンション G', propertyType: '中古マンション', area: '港区', address: '東京都港区芝浦1-2-3',
        line: '山手線', station: '田町', walk: '7分', bus: 'なし', layout: '2LDK', builtYearMonth: '2018/03', structure: 'RC', totalFloors: '15階', floorLevel: '4階', roomNumber: '402', commonMemo: '反響4件。収納量評価高め。',
        salePrice: '5,480万円', saleManagementFee: '12,000円', repairReserveFee: '8,500円', exclusiveArea: '68.40㎡', landArea: '-', buildingArea: '-', saleBalconyDirection: '南', totalUnits: '84戸', saleParking: '空有', saleParkingFee: '28,000円', topography: '平坦', zoning: '商業地域', coverageRatio: '80%', floorAreaRatio: '400%', saleCurrentStatus: '居住中', delivery: '相談', saleFacilities: 'オートロック / 宅配BOX / 追焚', ownerChange: 'なし',
        rent: '', rentalManagementFee: '', guaranteeDeposit: '', rightMoney: '', gratuityFee: '', deposit: '', cancellationFee: '', availableFrom: '', buildingUsageArea: '', partialArea: '', roomCount: '', rentalBalconyDirection: '', rentalParking: '', rentalParkingFee: '', rentalCurrentStatus: '', rentalFacilitiesSummary: '', rentalNotes: '',
        status: '価格改定中'
      },
      {
        id: 'pr_002', customerId: 'cu_001', dealType: 'sale', title: '港南レジデンス 402', propertyType: '中古マンション', area: '港区', address: '東京都港区港南2-4-8',
        line: '山手線', station: '品川', walk: '8分', bus: 'なし', layout: '2LDK', builtYearMonth: '2017/09', structure: 'RC', totalFloors: '14階', floorLevel: '4階', roomNumber: '402', commonMemo: '最適候補。収納重視。',
        salePrice: '5,480万円', saleManagementFee: '11,500円', repairReserveFee: '7,800円', exclusiveArea: '67.90㎡', landArea: '-', buildingArea: '-', saleBalconyDirection: '南東', totalUnits: '66戸', saleParking: '空無', saleParkingFee: '-', topography: '平坦', zoning: '準工業地域', coverageRatio: '60%', floorAreaRatio: '300%', saleCurrentStatus: '空室', delivery: '即可', saleFacilities: '宅配BOX / 食洗機', ownerChange: 'なし',
        rent: '', rentalManagementFee: '', guaranteeDeposit: '', rightMoney: '', gratuityFee: '', deposit: '', cancellationFee: '', availableFrom: '', buildingUsageArea: '', partialArea: '', roomCount: '', rentalBalconyDirection: '', rentalParking: '', rentalParkingFee: '', rentalCurrentStatus: '', rentalFacilitiesSummary: '', rentalNotes: '',
        status: '提案候補'
      },
      {
        id: 'pr_003', customerId: 'cu_001', dealType: 'sale', title: '白金タワー 1103', propertyType: '中古マンション', area: '港区', address: '東京都港区白金1-10-2',
        line: '南北線', station: '白金高輪', walk: '3分', bus: 'なし', layout: '2LDK', builtYearMonth: '2015/12', structure: 'RC', totalFloors: '23階', floorLevel: '11階', roomNumber: '1103', commonMemo: '駅近比較用。',
        salePrice: '5,620万円', saleManagementFee: '13,200円', repairReserveFee: '9,300円', exclusiveArea: '66.20㎡', landArea: '-', buildingArea: '-', saleBalconyDirection: '西', totalUnits: '102戸', saleParking: '空有', saleParkingFee: '32,000円', topography: '平坦', zoning: '商業地域', coverageRatio: '80%', floorAreaRatio: '500%', saleCurrentStatus: '空室', delivery: '相談', saleFacilities: '内廊下 / 床暖房', ownerChange: 'なし',
        rent: '', rentalManagementFee: '', guaranteeDeposit: '', rightMoney: '', gratuityFee: '', deposit: '', cancellationFee: '', availableFrom: '', buildingUsageArea: '', partialArea: '', roomCount: '', rentalBalconyDirection: '', rentalParking: '', rentalParkingFee: '', rentalCurrentStatus: '', rentalFacilitiesSummary: '', rentalNotes: '',
        status: '提案候補'
      },
      {
        id: 'pr_004', customerId: 'cu_002', dealType: 'rental', title: '芝浦コート 805', propertyType: '貸マンション', area: '港区', address: '東京都港区芝浦4-5-1',
        line: '山手線', station: '田町', walk: '9分', bus: 'なし', layout: '1LDK', builtYearMonth: '2020/05', structure: 'RC', totalFloors: '12階', floorLevel: '8階', roomNumber: '805', commonMemo: '2人入居可。ペット相談。',
        salePrice: '', saleManagementFee: '', repairReserveFee: '', exclusiveArea: '', landArea: '', buildingArea: '', saleBalconyDirection: '', totalUnits: '', saleParking: '', saleParkingFee: '', topography: '', zoning: '', coverageRatio: '', floorAreaRatio: '', saleCurrentStatus: '', delivery: '', saleFacilities: '', ownerChange: '',
        rent: '185,000円', rentalManagementFee: '10,000円', guaranteeDeposit: '1ヶ月', rightMoney: 'なし', gratuityFee: '1ヶ月', deposit: '1ヶ月', cancellationFee: 'なし', availableFrom: '即入居可', buildingUsageArea: '54.10㎡', partialArea: 'バルコニー 7.2㎡', roomCount: '2室', rentalBalconyDirection: '東', rentalParking: '近隣確保', rentalParkingFee: '22,000円', rentalCurrentStatus: '空室', rentalFacilitiesSummary: '都市ガス / 給湯 / 冷暖房', rentalNotes: '保証会社必須 / ペット相談',
        status: '賃貸提案中'
      }
    ],
    posts: [
      { id: 'sp_001', title: '価格改定共有 / 港区マンション G', visibility: 'グループ業者のみ', visibilityCode: 'broker_group_only', author: '田中', unread: 3, body: '価格改定に伴い再販開始前の共有を行います。反響4件、内見済み2件で、収納量の評価が高いです。', emoji: '🏢', customerId: 'cu_001', propertyId: 'pr_001' },
      { id: 'sp_002', title: '賃貸候補共有 / 芝浦コート 805', visibility: '店舗内', visibilityCode: 'store_only', author: '田中', unread: 0, body: 'ペット相談可。内見候補を調整したいです。2人入居OK。', emoji: '🐾', customerId: 'cu_002', propertyId: 'pr_004' },
      { id: 'sp_003', title: '成約報告 / 白金タワー 1103', visibility: '社内のみ', visibilityCode: 'internal_only', author: '佐藤', unread: 2, body: '駅近の比較物件として案内し、条件見直しから成約に繋がりました。', emoji: '🎉', customerId: 'cu_001', propertyId: 'pr_003' },
      { id: 'sp_004', title: '業者様向け内覧会案内', visibility: 'グループ業者のみ', visibilityCode: 'broker_group_only', author: '鈴木', unread: 1, body: '来週土曜、港区案件の内覧会を実施します。エントリーはこの投稿にコメントしてください。', emoji: '📣', customerId: null, propertyId: null }
    ],
    tasks: [
      { id: 'tk_001', title: '比較資料送付', status: 'doing', priority: 'high', due: '今日 10:00', customerId: 'cu_001', propertyId: 'pr_001', sourcePostId: 'sp_001', assignedTo: '田中' },
      { id: 'tk_002', title: '賃貸内見候補連絡', status: 'todo', priority: 'medium', due: '今日 13:00', customerId: 'cu_002', propertyId: 'pr_004', sourcePostId: 'sp_002', assignedTo: '田中' }
    ],
    schedules: [
      { id: 'sc_001', title: '再内見候補確定', status: 'planned', when: '今日 11:00', customerId: 'cu_001', propertyId: 'pr_001', sync: 'Google / iPhone queued', resultStatus: '', memo: '' },
      { id: 'sc_002', title: '賃貸内見', status: 'planned', when: '今日 15:00', customerId: 'cu_002', propertyId: 'pr_004', sync: '未同期', resultStatus: '', memo: '' }
    ],
    threads: [
      {
        id: 'th_001', name: '山田様 (顧客)', kind: 'customer', avatar: '山', unread: 2,
        messages: [
          { from: '山田様', mine: false, text: '別物件の提案お願いできますか？', at: '09:20' },
          { from: '田中', mine: true, text: '本日中に3件比較資料をお送りします。', at: '09:22' },
          { from: '山田様', mine: false, text: '駅近優先で見たいです。', at: '09:24' }
        ]
      },
      {
        id: 'th_002', name: '店舗グループ', kind: 'group', avatar: '店', unread: 1,
        messages: [
          { from: '佐藤', mine: false, text: '本日15時から価格会議です。', at: '08:40' },
          { from: '田中', mine: true, text: '了解しました。比較資料持参します。', at: '08:41' },
          { from: '高橋', mine: false, text: '会議室予約済みです。', at: '08:45' }
        ]
      },
      {
        id: 'th_003', name: 'グループ業者A', kind: 'broker', avatar: '業', unread: 0,
        messages: [
          { from: '業者A', mine: false, text: '内覧会は土曜10時開始で問題ないですか？', at: '昨日' },
          { from: '田中', mine: true, text: '大丈夫です。参加者リスト送ります。', at: '昨日' }
        ]
      },
      {
        id: 'th_004', name: '中村様 (顧客)', kind: 'customer', avatar: '中', unread: 0,
        messages: [
          { from: '中村様', mine: false, text: 'ペット可の物件でお願いします。', at: '一昨日' },
          { from: '田中', mine: true, text: '芝浦コート805をご案内予定です。', at: '一昨日' }
        ]
      }
    ]
  };
}

let state = loadState();
let snsAttachedImages = [];

function readFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function loadImageFromFile(file) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => { URL.revokeObjectURL(url); resolve(img); };
    img.onerror = (e) => { URL.revokeObjectURL(url); reject(e); };
    img.src = url;
  });
}

const MAX_IMAGE_BYTES = 220 * 1024; // 約220KB以内へ逐次圧縮

async function fileToCompressedDataUrl(file, initialMax = 1024, initialQuality = 0.72) {
  let img;
  try {
    img = await loadImageFromFile(file);
  } catch {
    return await readFileAsDataUrl(file);
  }
  const attempts = [
    { max: initialMax, q: initialQuality },
    { max: 960, q: 0.65 },
    { max: 800, q: 0.58 },
    { max: 640, q: 0.5 },
    { max: 480, q: 0.45 }
  ];
  let last = '';
  for (const step of attempts) {
    let { width, height } = img;
    if (width > step.max || height > step.max) {
      const ratio = Math.min(step.max / width, step.max / height);
      width = Math.max(1, Math.round(width * ratio));
      height = Math.max(1, Math.round(height * ratio));
    }
    const canvas = document.createElement('canvas');
    canvas.width = width; canvas.height = height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0, width, height);
    last = canvas.toDataURL('image/jpeg', step.q);
    if (last.length <= MAX_IMAGE_BYTES * 1.37) return last; // base64 overhead ~1.37
  }
  return last || await readFileAsDataUrl(file);
}

function renderSnsImagePreview() {
  const root = document.getElementById('snsImagePreview');
  if (!root) return;
  root.innerHTML = snsAttachedImages.map((src, idx) => `
    <div class="thumb">
      <img src="${src}" alt="">
      <button type="button" class="remove" onclick="removeSnsImage(${idx})" aria-label="削除">×</button>
    </div>
  `).join('');
}

function removeSnsImage(index) {
  snsAttachedImages.splice(index, 1);
  renderSnsImagePreview();
}
window.removeSnsImage = removeSnsImage;

function setupSnsImagePicker() {
  const input = document.getElementById('snsImageInput');
  if (!input) return;
  input.addEventListener('change', async (e) => {
    const file = (e.target.files || [])[0];
    if (!file) return;
    if (!file.type.startsWith('image/')) { e.target.value = ''; return; }
    if (file.size > 15 * 1024 * 1024) {
      showNotice(`${file.name} は大きすぎます（15MB以下）。`, 'error');
      e.target.value = '';
      return;
    }
    try {
      const dataUrl = await fileToCompressedDataUrl(file);
      snsAttachedImages = [dataUrl];
    } catch { /* skip */ }
    renderSnsImagePreview();
    e.target.value = '';
  });
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : createInitialState();
  } catch {
    return createInitialState();
  }
}
function trySetItem(payload) {
  try {
    localStorage.setItem(STORAGE_KEY, payload);
    return true;
  } catch (err) {
    return false;
  }
}

function saveState() {
  if (trySetItem(JSON.stringify(state))) return true;

  // 1) 古い投稿の画像を順に落として再試行
  const clone = JSON.parse(JSON.stringify(state));
  if (Array.isArray(clone.posts)) {
    for (let i = clone.posts.length - 1; i >= 0; i--) {
      const p = clone.posts[i];
      if (p && p.images && p.images.length) {
        p.images = [];
        if (trySetItem(JSON.stringify(clone))) {
          // 成功した形を実メモリにも反映 (同じ位置の実 state を更新)
          const target = state.posts[i];
          if (target) target.images = [];
          showNotice('容量上限のため、古い投稿の画像を除外して保存しました。', 'error');
          return true;
        }
      }
    }
    // 2) それでもダメなら、すべての投稿の画像を落とす
    clone.posts = clone.posts.map((p) => ({ ...p, images: [] }));
    if (trySetItem(JSON.stringify(clone))) {
      state.posts = state.posts.map((p) => ({ ...p, images: [] }));
      showNotice('容量上限のため、保存先の画像をすべて除外しました（表示は今のセッション中のみ）。', 'error');
      return true;
    }
  }
  showNotice('ブラウザの保存領域が一杯です。デモデータ初期化をお願いします。', 'error');
  return false;
}
function resetState() { state = createInitialState(); saveState(); }
function uid(prefix, list) { return `${prefix}_${String(list.length + 1).padStart(3, '0')}`; }
function getCustomer(id) { return state.customers.find((x) => x.id === id) || null; }
function getProperty(id) { return state.properties.find((x) => x.id === id) || null; }
function visibilityLabel(code) {
  return ({ store_only: '店舗内', internal_only: '社内のみ', broker_group_only: 'グループ業者のみ', public: '一般公開' })[code] || code;
}
function roleLabel(_role) { return ''; }
function dealTypeLabel(type) { return type === 'rental' ? '賃貸' : '売買'; }
function propertyPrimaryValue(property) {
  return property.dealType === 'rental' ? property.rent : property.salePrice;
}
function propertyAreaValue(property) {
  if (property.dealType === 'rental') return property.buildingUsageArea || property.partialArea || '-';
  return property.exclusiveArea || property.landArea || property.buildingArea || '-';
}
function can(_action) { return true; }
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
  document.querySelectorAll('.tab-btn').forEach((btn) => btn.classList.toggle('active', btn.dataset.screen === screenId));
  window.scrollTo({ top: 0, behavior: 'auto' });
}

function updateUserSummary() {
  const session = state.session || DEFAULT_USER;
  const el = document.getElementById('userSummary');
  if (!el) return;
  el.textContent = session.email ? `${session.name || 'ユーザー'} / ${session.email}` : (session.name || 'ユーザー');
}

function fillSelect(selectId, items, formatter, includeBlank = false) {
  const el = document.getElementById(selectId);
  if (!el) return;
  el.innerHTML = '';
  if (includeBlank) {
    const blank = document.createElement('option');
    blank.value = ''; blank.textContent = '未選択';
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
  fillSelect('propertyCustomerSelect', state.customers, (c) => c.name, true);
  fillSelect('snsPropertySelect', state.properties, (p) => `${dealTypeLabel(p.dealType)} / ${p.title}`);
  fillSelect('documentCustomerSelect', state.customers, (c) => c.name);
  fillSelect('documentBasePropertySelect', state.properties, (p) => `${dealTypeLabel(p.dealType)} / ${p.title}`);
  fillSelect('candidateASelect', state.properties, (p) => `${dealTypeLabel(p.dealType)} / ${p.title}`);
  fillSelect('candidateBSelect', state.properties, (p) => `${dealTypeLabel(p.dealType)} / ${p.title}`);
  fillSelect('resultScheduleSelect', state.schedules, (s) => `${s.when} / ${s.title}`);
  const base = state.properties.find((p) => p.dealType === 'sale') || state.properties[0];
  const a = state.properties[1] || state.properties[0];
  const b = state.properties[2] || state.properties[0];
  if (document.getElementById('documentBasePropertySelect')) document.getElementById('documentBasePropertySelect').value = base?.id || '';
  if (document.getElementById('candidateASelect')) document.getElementById('candidateASelect').value = a?.id || '';
  if (document.getElementById('candidateBSelect')) document.getElementById('candidateBSelect').value = b?.id || '';
  if (document.getElementById('propertyCustomerSelect')) document.getElementById('propertyCustomerSelect').value = state.customers[0]?.id || '';
}

function updatePropertyMode() {
  const select = document.getElementById('dealTypeSelect');
  if (!select) return;
  const dealType = select.value;
  const saleBlock = document.querySelector('.sale-fields');
  const rentalBlock = document.querySelector('.rental-fields');
  const pill = document.getElementById('propertyModePill');
  if (saleBlock) saleBlock.classList.toggle('hidden-block', dealType !== 'sale');
  if (rentalBlock) rentalBlock.classList.toggle('hidden-block', dealType !== 'rental');
  if (pill) pill.textContent = dealType === 'rental' ? '賃貸' : '売買';
}

/* ============ Renderers ============ */
function renderHome() {
  const dateEl = document.getElementById('homeDateLabel');
  if (dateEl) {
    const d = new Date();
    dateEl.textContent = `${d.getFullYear()}年${d.getMonth()+1}月${d.getDate()}日`;
  }
  document.getElementById('homeSchedules').innerHTML = state.schedules.map((s) => {
    const c = getCustomer(s.customerId); const p = getProperty(s.propertyId);
    return `
      <div class="item">
        <div class="item-title">${s.when} ${s.title}</div>
        <div class="item-sub">${c?.name || '-'} / ${p?.title || '-'}</div>
        <div class="top-meta">
          ${p ? `<span class="chip ${p.dealType}">${dealTypeLabel(p.dealType)}</span>` : ''}
          <span class="chip">${s.sync}</span>
        </div>
      </div>
    `;
  }).join('') || '<div class="empty-state">予定はありません</div>';

  document.getElementById('homeTasks').innerHTML = state.tasks.map((t) => {
    const c = getCustomer(t.customerId); const p = getProperty(t.propertyId);
    return `
      <div class="item">
        <div class="item-title">${t.due} ${t.title}</div>
        <div class="item-sub">${c?.name || '-'} / ${p?.title || '-'} / ${t.status}</div>
        <div class="top-meta">
          <span class="chip ${t.priority === 'high' ? 'active' : ''}">${t.priority}</span>
          ${p ? `<span class="chip ${p.dealType}">${dealTypeLabel(p.dealType)}</span>` : ''}
        </div>
      </div>
    `;
  }).join('') || '<div class="empty-state">タスクはありません</div>';

  const unreadCount = state.notifications.filter((n) => n.unread).length;
  const saleCount = state.properties.filter((p) => p.dealType === 'sale').length;
  const rentalCount = state.properties.filter((p) => p.dealType === 'rental').length;
  document.getElementById('homeKpis').innerHTML = [
    { label: '本日予定', value: state.schedules.length, sub: '結果未入力を含む' },
    { label: '今日期限', value: state.tasks.length, sub: '主導線を維持' },
    { label: 'SNS未読', value: unreadCount, sub: 'コメント / メンション' },
    { label: '物件在庫', value: `${saleCount}/${rentalCount}`, sub: '売買 / 賃貸' }
  ].map((k) => `
    <div class="metric-card">
      <div class="metric-label">${k.label}</div>
      <div class="metric-value">${k.value}</div>
      <div class="metric-sub">${k.sub}</div>
    </div>
  `).join('');

  renderFeed('homeFeed', 3);
}

function renderCustomers() {
  document.getElementById('customerCountPill').textContent = `${state.customers.length}件`;
  document.getElementById('customerList').innerHTML = state.customers.map((customer) => {
    const linked = state.properties.filter((p) => p.customerId === customer.id);
    return `
      <div class="item">
        <div class="item-title">${customer.name}</div>
        <div class="item-sub">担当: ${customer.owner} / 予算: ${customer.budget}</div>
        <div class="item-sub">条件: ${customer.needs}</div>
        <div class="top-meta">
          <span class="tag ${customer.heat === 'high' ? 'danger' : 'warning'}">${customer.nextAction}</span>
          <span class="chip">紐づき ${linked.length}件</span>
        </div>
      </div>
    `;
  }).join('');
}

function renderProperties() {
  const saleCount = state.properties.filter((p) => p.dealType === 'sale').length;
  const rentalCount = state.properties.filter((p) => p.dealType === 'rental').length;
  document.getElementById('propertyCountPill').textContent = `${state.properties.length}件`;
  document.getElementById('propertySummaryCards').innerHTML = `
    <div class="info-card"><div class="item-title">売買</div><p>${saleCount}件</p></div>
    <div class="info-card"><div class="item-title">賃貸</div><p>${rentalCount}件</p></div>
    <div class="info-card"><div class="item-title">優先紐づき</div><p>${state.properties.filter((p) => getCustomer(p.customerId)?.heat === 'high').length}件</p></div>
  `;
  document.getElementById('propertyList').innerHTML = state.properties.map((property) => {
    const customer = getCustomer(property.customerId);
    const primary = propertyPrimaryValue(property);
    const area = propertyAreaValue(property);
    const extra = property.dealType === 'sale'
      ? `管理費 ${property.saleManagementFee || '-'} / 現況 ${property.saleCurrentStatus || '-'}`
      : `管理費 ${property.rentalManagementFee || '-'} / 現況 ${property.rentalCurrentStatus || '-'}`;
    return `
      <div class="item">
        <div class="item-title">${property.title}</div>
        <div class="item-sub">${property.propertyType} / ${property.area} / ${property.address}</div>
        <div class="item-sub">${primary || '-'} / ${property.layout} / ${area}</div>
        <div class="item-sub">${property.line} ${property.station} 徒歩${property.walk} / 築 ${property.builtYearMonth}</div>
        <div class="item-sub">${extra}</div>
        <div class="top-meta">
          <span class="chip ${property.dealType}">${dealTypeLabel(property.dealType)}</span>
          <span class="chip">${property.status}</span>
          ${customer ? `<span class="chip">${customer.name}</span>` : ''}
        </div>
      </div>
    `;
  }).join('');
}

function feedThumb(post) {
  const property = getProperty(post.propertyId);
  const icon = post.emoji || (property?.dealType === 'rental' ? '🏠' : '🏢');
  if (post.images && post.images.length) {
    const extra = post.images.length > 1 ? `<span class="thumb-badge">+${post.images.length - 1}</span>` : '';
    return `<div class="feed-thumb"><img src="${post.images[0]}" alt="">${extra}</div>`;
  }
  return `<div class="feed-thumb">${icon}</div>`;
}
function feedItemHtml(post) {
  const customer = getCustomer(post.customerId);
  const property = getProperty(post.propertyId);
  return `
    <div class="feed-card" onclick="openPostDetail('${post.id}')">
      ${feedThumb(post)}
      <div class="feed-body">
        <div class="feed-title">${post.title}</div>
        <div class="feed-excerpt">${post.body}</div>
        <div class="feed-meta">
          <span>${post.author}</span><span class="dot">•</span>
          <span>${visibilityLabel(post.visibilityCode)}</span>
          ${customer ? `<span class="dot">•</span><span>${customer.name}</span>` : ''}
          ${property ? `<span class="dot">•</span><span>${property.title}</span>` : ''}
          ${post.unread ? `<span class="dot">•</span><span style="color:var(--danger);font-weight:800;">未読${post.unread}</span>` : ''}
        </div>
        <div class="feed-actions" onclick="event.stopPropagation()">
          <button type="button" class="ghost-btn" onclick="startEditPost('${post.id}')">編集</button>
          <button type="button" class="ghost-btn" onclick="taskFromPost('${post.id}')">タスク化</button>
          <button type="button" class="ghost-btn danger" onclick="deletePost('${post.id}')">削除</button>
        </div>
      </div>
    </div>
  `;
}
function renderFeed(targetId, limit) {
  const container = document.getElementById(targetId);
  if (!container) return;
  let items = state.posts;
  if (targetId === 'snsFeed' && state.activeFeed !== 'all') {
    items = items.filter((p) => p.visibilityCode === state.activeFeed);
  }
  const list = limit ? items.slice(0, limit) : items;
  container.innerHTML = list.map(feedItemHtml).join('') || '<div class="empty-state">投稿はありません</div>';
}
function renderFeedTabs() {
  document.querySelectorAll('.feed-tab').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.feed === state.activeFeed);
  });
}

function openPostAsTask(postId) {
  const post = state.posts.find((p) => p.id === postId);
  if (!post) return;
  if (post.unread) { post.unread = 0; saveState(); }
  createTaskFromPost(postId);
}
window.openPostAsTask = openPostAsTask;

function openPostDetail(postId) {
  const post = state.posts.find((p) => p.id === postId);
  if (!post) return;
  if (post.unread) { post.unread = 0; saveState(); rerenderAll(); }
  state.activePostId = postId;
  saveState();
  renderPostDetail();
  go('post');
}
window.openPostDetail = openPostDetail;

function renderPostDetail() {
  const root = document.getElementById('postDetail');
  if (!root) return;
  const post = state.posts.find((p) => p.id === state.activePostId);
  if (!post) {
    root.innerHTML = '<div class="empty-state">投稿が見つかりません。</div>';
    return;
  }
  const customer = getCustomer(post.customerId);
  const property = getProperty(post.propertyId);
  const hero = (post.images && post.images.length)
    ? `<div class="pd-hero"><img src="${post.images[0]}" alt=""></div>`
    : `<div class="pd-hero">${post.emoji || (property?.dealType === 'rental' ? '🏠' : '🏢')}</div>`;
  const linked = (customer || property) ? `
    <div class="pd-linked">
      ${customer ? `<div><strong>顧客:</strong> ${customer.name}（担当 ${customer.owner || '-'} / 予算 ${customer.budget || '-'}）</div>` : ''}
      ${property ? `<div><strong>物件:</strong> ${property.title} / ${dealTypeLabel(property.dealType)} / ${propertyPrimaryValue(property) || '-'}</div>` : ''}
      ${property ? `<div><strong>所在地:</strong> ${property.address || '-'} （${property.line || '-'} ${property.station || ''} 徒歩${property.walk || '-'}）</div>` : ''}
    </div>` : '';
  root.innerHTML = `
    ${hero}
    <div class="pd-title">${post.title}</div>
    <div class="pd-meta">
      <span>${post.author}</span><span class="dot">•</span>
      <span>${visibilityLabel(post.visibilityCode)}</span>
      ${property ? `<span class="dot">•</span><span>${dealTypeLabel(property.dealType)}</span>` : ''}
    </div>
    <div class="pd-chips">
      <span class="chip">${visibilityLabel(post.visibilityCode)}</span>
      ${property ? `<span class="chip ${property.dealType}">${dealTypeLabel(property.dealType)}</span>` : ''}
      ${customer ? `<span class="chip">${customer.name}</span>` : ''}
    </div>
    <div class="pd-body">${(post.body || '').replace(/</g,'&lt;')}</div>
    ${linked}
  `;

  const editBtn = document.getElementById('postDetailEditBtn');
  const taskBtn = document.getElementById('postDetailTaskBtn');
  const delBtn = document.getElementById('postDetailDeleteBtn');
  if (editBtn) editBtn.onclick = () => startEditPost(post.id);
  if (taskBtn) taskBtn.onclick = () => taskFromPost(post.id);
  if (delBtn) delBtn.onclick = () => deletePost(post.id);
}

function startEditPost(postId) {
  const post = state.posts.find((p) => p.id === postId);
  if (!post) return;
  const form = document.getElementById('snsForm');
  if (!form) return;
  form.querySelector('select[name="visibility"]').value = post.visibilityCode || 'store_only';
  const propSel = form.querySelector('select[name="propertyId"]');
  if (propSel) propSel.value = post.propertyId || '';
  form.querySelector('input[name="title"]').value = post.title || '';
  form.querySelector('textarea[name="body"]').value = post.body || '';
  document.getElementById('snsEditingPostId').value = post.id;
  snsAttachedImages = (post.images && post.images.length) ? [post.images[0]] : [];
  renderSnsImagePreview();
  const fileInput = document.getElementById('snsImageInput');
  if (fileInput) fileInput.value = '';
  const submitBtn = document.getElementById('snsSubmitBtn');
  if (submitBtn) submitBtn.textContent = '変更を保存';
  const cancelBtn = document.getElementById('snsCancelEditBtn');
  if (cancelBtn) cancelBtn.classList.remove('hidden');
  const composer = document.getElementById('snsComposer');
  if (composer && composer.tagName === 'DETAILS') composer.open = true;
  go('sns');
  setTimeout(() => composer && composer.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
}
window.startEditPost = startEditPost;

function cancelEditPost() {
  document.getElementById('snsEditingPostId').value = '';
  snsAttachedImages = [];
  renderSnsImagePreview();
  const form = document.getElementById('snsForm');
  if (form) form.reset();
  const submitBtn = document.getElementById('snsSubmitBtn');
  if (submitBtn) submitBtn.textContent = '投稿を保存';
  const cancelBtn = document.getElementById('snsCancelEditBtn');
  if (cancelBtn) cancelBtn.classList.add('hidden');
}
window.cancelEditPost = cancelEditPost;

function deletePost(postId) {
  const idx = state.posts.findIndex((p) => p.id === postId);
  if (idx < 0) return;
  if (!confirm('この投稿を削除しますか？')) return;
  state.posts.splice(idx, 1);
  if (document.getElementById('snsEditingPostId').value === postId) cancelEditPost();
  if (state.activePostId === postId) { state.activePostId = null; go('sns'); }
  saveState();
  rerenderAll();
  showNotice('投稿を削除しました。');
}
window.deletePost = deletePost;

function taskFromPost(postId) { createTaskFromPost(postId); }
window.taskFromPost = taskFromPost;

function renderTasks() {
  document.getElementById('taskCountPill').textContent = `${state.tasks.length}件`;
  document.getElementById('taskList').innerHTML = state.tasks.map((task) => {
    const customer = getCustomer(task.customerId);
    const property = getProperty(task.propertyId);
    return `
      <div class="item" onclick="selectTask('${task.id}')" style="cursor:pointer; ${task.id === state.selectedTaskId ? 'border-color:#2563eb;background:#eff6ff;' : ''}">
        <div class="item-title">${task.title}</div>
        <div class="item-sub">${task.status} / ${task.priority} / ${task.due}</div>
        <div class="item-sub">${customer?.name || '-'} / 担当: ${task.assignedTo}</div>
        <div class="top-meta">${property ? `<span class="chip ${property.dealType}">${dealTypeLabel(property.dealType)}</span>` : ''}</div>
      </div>
    `;
  }).join('');
  const task = state.tasks.find((t) => t.id === state.selectedTaskId) || state.tasks[0];
  if (!task) { document.getElementById('taskDetail').innerHTML = '<div class="empty-state">タスクがありません</div>'; return; }
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
      ${property ? `<p>取引区分: ${dealTypeLabel(property.dealType)} / 金額: ${propertyPrimaryValue(property)}</p>` : ''}
      <div class="actions">
        <button class="secondary-btn" onclick="markTaskDone('${task.id}')">完了</button>
        <button class="primary-btn" onclick="createScheduleFromTask('${task.id}')">予定化</button>
      </div>
    </div>
  `;
}

function renderSchedules() {
  document.getElementById('scheduleCountPill').textContent = `${state.schedules.length}件`;
  document.getElementById('scheduleList').innerHTML = state.schedules.map((s) => {
    const customer = getCustomer(s.customerId);
    const property = getProperty(s.propertyId);
    return `
      <div class="item">
        <div class="item-title">${s.when} ${s.title}</div>
        <div class="item-sub">${customer?.name || '-'} / ${property?.title || '-'} / ${s.status}</div>
        <div class="top-meta">
          ${property ? `<span class="chip ${property.dealType}">${dealTypeLabel(property.dealType)}</span>` : ''}
          <span class="chip">${s.sync}</span>
          ${s.resultStatus ? `<span class="tag success">結果: ${s.resultStatus}</span>` : ''}
        </div>
      </div>
    `;
  }).join('');
}

function buildCompareRows(base, candidateA, candidateB) {
  const rows = [
    ['取引区分', dealTypeLabel(base.dealType), dealTypeLabel(candidateA.dealType), dealTypeLabel(candidateB.dealType)],
    ['物件名', base.title, candidateA.title, candidateB.title],
    ['価格 / 賃料', propertyPrimaryValue(base), propertyPrimaryValue(candidateA), propertyPrimaryValue(candidateB)],
    ['間取り', base.layout, candidateA.layout, candidateB.layout],
    ['面積', propertyAreaValue(base), propertyAreaValue(candidateA), propertyAreaValue(candidateB)],
    ['沿線 / 駅', `${base.line} / ${base.station}`, `${candidateA.line} / ${candidateA.station}`, `${candidateB.line} / ${candidateB.station}`],
    ['徒歩', base.walk, candidateA.walk, candidateB.walk],
    ['築年月', base.builtYearMonth, candidateA.builtYearMonth, candidateB.builtYearMonth],
    ['構造', base.structure, candidateA.structure, candidateB.structure],
    ['現況', base.dealType === 'rental' ? base.rentalCurrentStatus : base.saleCurrentStatus, candidateA.dealType === 'rental' ? candidateA.rentalCurrentStatus : candidateA.saleCurrentStatus, candidateB.dealType === 'rental' ? candidateB.rentalCurrentStatus : candidateB.saleCurrentStatus],
    ['設備', base.dealType === 'rental' ? base.rentalFacilitiesSummary : base.saleFacilities, candidateA.dealType === 'rental' ? candidateA.rentalFacilitiesSummary : candidateA.saleFacilities, candidateB.dealType === 'rental' ? candidateB.rentalFacilitiesSummary : candidateB.saleFacilities]
  ];
  return rows.map((row) => `<tr><td>${row[0]}</td><td>${row[1] || '-'}</td><td>${row[2] || '-'}</td><td>${row[3] || '-'}</td></tr>`).join('');
}
function createDocumentPreview({ customer, base, candidateA, candidateB, comment, destination }) {
  return `
    <div>
      <div class="item-title">比較資料プレビュー</div>
      <p>${customer.name} 向け / 保存先: ${destination}</p>
      <table class="doc-table">
        <thead><tr><th>項目</th><th>基準物件</th><th>比較A</th><th>比較B</th></tr></thead>
        <tbody>${buildCompareRows(base, candidateA, candidateB)}</tbody>
      </table>
      <p><strong>営業コメント:</strong> ${comment}</p>
      <p>生成フロー: 別物件提案 → 比較資料作成 → ブラウザ印刷 / PDF保存 → クラウド保存想定</p>
    </div>
  `;
}
function renderDocumentPreview() {
  const root = document.getElementById('documentPreview');
  if (!root) return;
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
        ${n.unread ? `<button class="secondary-btn" onclick="markRead('${n.id}')">既読</button>` : ''}
      </div>
    </div>
  `).join('');
}

/* ============ Messenger ============ */
function renderThreads() {
  const list = document.getElementById('threadList');
  if (!list) return;
  list.innerHTML = state.threads.map((t) => `
    <div class="thread-item ${t.id === state.activeThreadId ? 'active' : ''}" onclick="selectThread('${t.id}')">
      <div class="thread-avatar">${t.avatar}</div>
      <div class="thread-meta">
        <div class="name">${t.name}</div>
        <div class="preview">${(t.messages[t.messages.length-1]?.text || '').replace(/</g,'&lt;')}</div>
      </div>
      ${t.unread ? `<div class="thread-badge">${t.unread}</div>` : ''}
    </div>
  `).join('');

  const active = state.threads.find((t) => t.id === state.activeThreadId) || state.threads[0];
  const header = document.getElementById('threadHeader');
  const body = document.getElementById('threadBody');
  if (!active) {
    if (header) header.innerHTML = '<div class="thread-title">スレッドを選択</div>';
    if (body) body.innerHTML = '';
  } else {
    if (header) header.innerHTML = `
      <div class="thread-title">${active.name}</div>
      <div class="thread-sub">${active.kind === 'customer' ? '顧客チャット' : active.kind === 'broker' ? '業者チャット' : 'グループチャット'}</div>
    `;
    if (body) {
      body.innerHTML = active.messages.map((m) => `
        <div class="bubble ${m.mine ? 'mine' : ''}">
          <div class="who">${m.from} ・ ${m.at}</div>
          <div>${m.text.replace(/</g,'&lt;')}</div>
        </div>
      `).join('');
      body.scrollTop = body.scrollHeight;
    }
  }

  const totalUnread = state.threads.reduce((s, t) => s + (t.unread || 0), 0);
  const badge = document.getElementById('messagesBadge');
  if (badge) {
    badge.textContent = totalUnread;
    badge.classList.toggle('hidden', totalUnread === 0);
  }
}
function selectThread(id) {
  state.activeThreadId = id;
  const th = state.threads.find((t) => t.id === id);
  if (th) th.unread = 0;
  saveState();
  renderThreads();
}
window.selectThread = selectThread;
function sendThreadMessage(text) {
  const active = state.threads.find((t) => t.id === state.activeThreadId);
  if (!active) return;
  const now = new Date();
  const hh = String(now.getHours()).padStart(2,'0');
  const mm = String(now.getMinutes()).padStart(2,'0');
  active.messages.push({ from: state.session?.name || '田中', mine: true, text, at: `${hh}:${mm}` });
  saveState();
  renderThreads();
}

/* ============ Actions ============ */
function selectTask(id) { state.selectedTaskId = id; saveState(); renderTasks(); }
window.selectTask = selectTask;

function createTaskFromPost(postId) {
  const post = state.posts.find((p) => p.id === postId);
  if (!post) return;
  const customer = getCustomer(post.customerId);
  const property = getProperty(post.propertyId);
  const newTask = {
    id: uid('tk', state.tasks),
    title: `${customer?.name || 'SNS投稿'}へ対応`,
    status: 'todo',
    priority: property?.dealType === 'sale' ? 'high' : 'medium',
    due: '明日 10:00',
    customerId: post.customerId,
    propertyId: post.propertyId,
    sourcePostId: post.id,
    assignedTo: state.session?.name || '田中'
  };
  state.tasks.unshift(newTask);
  state.selectedTaskId = newTask.id;
  state.notifications.unshift({ id: uid('nt', state.notifications), type: 'task_assigned', title: 'タスク作成', body: 'SNS投稿からタスクを作成しました', unread: true, priority: 'medium' });
  saveState(); rerenderAll();
  showNotice('投稿からタスクを作成しました。');
  go('tasks');
}
window.createTaskFromPost = createTaskFromPost;

function markTaskDone(taskId) {
  const task = state.tasks.find((t) => t.id === taskId);
  if (!task) return;
  task.status = 'done';
  saveState(); rerenderAll();
  showNotice('タスクを完了にしました。');
}
window.markTaskDone = markTaskDone;

function createScheduleFromTask(taskId) {
  const task = state.tasks.find((t) => t.id === taskId);
  if (!task) return;
  const newSchedule = {
    id: uid('sc', state.schedules),
    title: `${task.title} ${getProperty(task.propertyId)?.dealType === 'rental' ? '内見' : '商談'}`,
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
  saveState(); rerenderAll();
  showNotice('予定を作成しました。');
  go('calendar');
}
window.createScheduleFromTask = createScheduleFromTask;

function markRead(id) {
  const item = state.notifications.find((n) => n.id === id);
  if (item) item.unread = false;
  saveState(); rerenderAll();
}
window.markRead = markRead;

function markAllRead() {
  state.notifications.forEach((n) => { n.unread = false; });
  saveState(); rerenderAll();
  showNotice('通知を一括既読にしました。');
}

function applyRole(_role) { /* no-op: roles removed */ }

function applyPermissionUI() { /* no-op: everyone can do everything */ }

function login({ name, email } = {}) {
  const displayName = (name || '').trim() || DEFAULT_USER.name;
  const displayEmail = (email || '').trim();
  state.session = { id: 'u_me', name: displayName, email: displayEmail };
  saveState();
  document.getElementById('loginScreen').classList.add('hidden');
  document.getElementById('appShell').classList.remove('hidden');
  updateUserSummary();
  applyPermissionUI();
  rerenderAll();
  showNotice(`${displayName} さんとしてログインしました。`);
  go('home');
}

function logout() {
  state.session = null;
  saveState();
  document.getElementById('appShell').classList.add('hidden');
  document.getElementById('loginScreen').classList.remove('hidden');
}

function printDocument() {
  if (!requirePermission('exportDocument', 'このロールではPDF出力できません。')) return;
  if (!state.lastDocumentHtml) { showNotice('先に資料を生成してください。', 'error'); return; }
  const win = window.open('', '_blank');
  win.document.write(`<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><title>比較資料</title><style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:24px;color:#111827}table{width:100%;border-collapse:collapse;margin-top:12px}th,td{border:1px solid #d1d5db;padding:8px;text-align:left;vertical-align:top}th{background:#eff6ff}</style></head><body>${state.lastDocumentHtml}</body></html>`);
  win.document.close();
  win.focus();
  win.print();
}

function rerenderAll() {
  populateLinkedSelects();
  updatePropertyMode();
  renderHome();
  renderCustomers();
  renderProperties();
  renderFeed('snsFeed');
  renderFeedTabs();
  renderTasks();
  renderSchedules();
  renderDocumentPreview();
  renderNotifications();
  renderThreads();
  renderPostDetail();
}

function initEvents() {
  document.querySelectorAll('.nav-btn').forEach((btn) => btn.addEventListener('click', () => go(btn.dataset.screen)));
  document.querySelectorAll('.tab-btn').forEach((btn) => btn.addEventListener('click', () => go(btn.dataset.screen)));
  document.querySelectorAll('[data-screen-link]').forEach((btn) => btn.addEventListener('click', () => go(btn.dataset.screenLink)));

  document.getElementById('dealTypeSelect').addEventListener('change', updatePropertyMode);

  document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('loginName').value;
    const email = document.getElementById('loginEmail').value;
    login({ name, email });
  });
  document.getElementById('resetDataBtn').addEventListener('click', () => {
    resetState();
    showNotice('デモデータを初期化しました。');
    if (state.session) rerenderAll();
  });
  document.getElementById('logoutBtn').addEventListener('click', logout);
  document.getElementById('markAllReadBtn').addEventListener('click', markAllRead);
  document.getElementById('printDocumentBtn').addEventListener('click', printDocument);

  document.querySelectorAll('.feed-tab').forEach((btn) => btn.addEventListener('click', () => {
    state.activeFeed = btn.dataset.feed;
    saveState();
    renderFeed('snsFeed');
    renderFeedTabs();
  }));

  setupSnsImagePicker();

  document.getElementById('threadComposer').addEventListener('submit', (e) => {
    e.preventDefault();
    const input = document.getElementById('threadInput');
    const text = (input.value || '').trim();
    if (!text) return;
    sendThreadMessage(text);
    input.value = '';
  });

  document.getElementById('customerForm').addEventListener('submit', (e) => {
    e.preventDefault();
    if (!requirePermission('addCustomer', 'このロールでは顧客追加できません。')) return;
    const form = new FormData(e.target);
    state.customers.unshift({
      id: uid('cu', state.customers),
      name: form.get('name'), owner: form.get('owner'), budget: form.get('budget'), needs: form.get('needs'), nextAction: '初回追客', heat: 'medium'
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
    const dealType = form.get('dealType');
    const property = {
      id: uid('pr', state.properties),
      customerId: form.get('customerId') || '',
      dealType,
      title: form.get('title') || '',
      propertyType: form.get('propertyType') || '',
      area: form.get('area') || '',
      address: form.get('address') || '',
      line: form.get('line') || '',
      station: form.get('station') || '',
      walk: form.get('walk') || '',
      bus: form.get('bus') || '',
      layout: form.get('layout') || '',
      builtYearMonth: form.get('builtYearMonth') || '',
      structure: form.get('structure') || '',
      totalFloors: form.get('totalFloors') || '',
      floorLevel: form.get('floorLevel') || '',
      roomNumber: form.get('roomNumber') || '',
      commonMemo: form.get('commonMemo') || '',
      salePrice: form.get('salePrice') || '',
      saleManagementFee: form.get('saleManagementFee') || '',
      repairReserveFee: form.get('repairReserveFee') || '',
      exclusiveArea: form.get('exclusiveArea') || '',
      landArea: form.get('landArea') || '',
      buildingArea: form.get('buildingArea') || '',
      saleBalconyDirection: form.get('saleBalconyDirection') || '',
      totalUnits: form.get('totalUnits') || '',
      saleParking: form.get('saleParking') || '',
      saleParkingFee: form.get('saleParkingFee') || '',
      topography: form.get('topography') || '',
      zoning: form.get('zoning') || '',
      coverageRatio: form.get('coverageRatio') || '',
      floorAreaRatio: form.get('floorAreaRatio') || '',
      saleCurrentStatus: form.get('saleCurrentStatus') || '',
      delivery: form.get('delivery') || '',
      saleFacilities: form.get('saleFacilities') || '',
      ownerChange: form.get('ownerChange') || '',
      rent: form.get('rent') || '',
      rentalManagementFee: form.get('rentalManagementFee') || '',
      guaranteeDeposit: form.get('guaranteeDeposit') || '',
      rightMoney: form.get('rightMoney') || '',
      gratuityFee: form.get('gratuityFee') || '',
      deposit: form.get('deposit') || '',
      cancellationFee: form.get('cancellationFee') || '',
      availableFrom: form.get('availableFrom') || '',
      buildingUsageArea: form.get('buildingUsageArea') || '',
      partialArea: form.get('partialArea') || '',
      roomCount: form.get('roomCount') || '',
      rentalBalconyDirection: form.get('rentalBalconyDirection') || '',
      rentalParking: form.get('rentalParking') || '',
      rentalParkingFee: form.get('rentalParkingFee') || '',
      rentalCurrentStatus: form.get('rentalCurrentStatus') || '',
      rentalFacilitiesSummary: form.get('rentalFacilitiesSummary') || '',
      rentalNotes: form.get('rentalNotes') || '',
      status: dealType === 'rental' ? '賃貸新規登録' : '売買新規登録'
    };
    state.properties.unshift(property);
    saveState();
    e.target.reset();
    document.getElementById('dealTypeSelect').value = 'sale';
    rerenderAll();
    showNotice(`${dealType === 'rental' ? '賃貸' : '売買'}物件を追加しました。`);
  });

  document.getElementById('snsForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const submitBtn = e.target.querySelector('button[type="submit"]');
    if (submitBtn && submitBtn.disabled) return;
    const editingId = document.getElementById('snsEditingPostId').value || '';
    const originalLabel = editingId ? '変更を保存' : '投稿を保存';
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = '保存中…'; }
    try {
      const form = new FormData(e.target);
      const visibilityCode = form.get('visibility');
      if (visibilityCode === 'public' && !requirePermission('createPublicPost', '一般公開は管理者のみ可能です。')) return;
      const propertyId = form.get('propertyId') || null;
      const linkedProperty = propertyId ? getProperty(propertyId) : null;
      const image = snsAttachedImages[0] || null;

      if (editingId) {
        const existing = state.posts.find((p) => p.id === editingId);
        if (existing) {
          existing.title = form.get('title');
          existing.body = form.get('body');
          existing.visibility = visibilityLabel(visibilityCode);
          existing.visibilityCode = visibilityCode;
          existing.propertyId = propertyId;
          existing.customerId = linkedProperty?.customerId || null;
          existing.images = image ? [image] : [];
        }
      } else {
        const newPost = {
          id: uid('sp', state.posts),
          title: form.get('title'),
          visibility: visibilityLabel(visibilityCode),
          visibilityCode,
          author: state.session?.name || '田中',
          unread: 0,
          body: form.get('body'),
          emoji: '📝',
          images: image ? [image] : [],
          customerId: linkedProperty?.customerId || null,
          propertyId
        };
        state.posts.unshift(newPost);
      }

      snsAttachedImages = [];
      renderSnsImagePreview();
      const fileInput = document.getElementById('snsImageInput');
      if (fileInput) fileInput.value = '';
      document.getElementById('snsEditingPostId').value = '';
      const cancelBtn = document.getElementById('snsCancelEditBtn');
      if (cancelBtn) cancelBtn.classList.add('hidden');
      saveState();
      rerenderAll();
      showNotice(editingId ? '投稿を更新しました。' : 'SNS投稿を保存しました。');
      const composer = document.getElementById('snsComposer');
      if (composer && composer.tagName === 'DETAILS') composer.open = false;
    } catch (err) {
      console.error(err);
      showNotice('投稿に失敗しました。もう一度お試しください。', 'error');
    } finally {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = '投稿を保存'; }
    }
  });

  const cancelEditBtn = document.getElementById('snsCancelEditBtn');
  if (cancelEditBtn) cancelEditBtn.addEventListener('click', cancelEditPost);

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
    showNotice('結果を登録しました。');
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
    state.lastDocumentHtml = createDocumentPreview({ customer, base, candidateA, candidateB, comment: form.get('comment'), destination: form.get('destination') });
    state.notifications.unshift({ id: uid('nt', state.notifications), type: 'document_ready', title: '資料作成完了', body: '比較資料プレビューを生成しました', unread: true, priority: 'medium' });
    saveState();
    rerenderAll();
    showNotice('比較資料を生成しました。');
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
    updatePropertyMode();
  }
}
document.addEventListener('DOMContentLoaded', init);