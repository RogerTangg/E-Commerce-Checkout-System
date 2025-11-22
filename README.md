# 電商結帳系統 (E-commerce Checkout System)

**Baseline V3** - 簡化版電商結帳頁面，專為 A/B Testing 對照組設計

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![Flask](https://img.shields.io/badge/flask-3.0.0-green)

---

## 專案簡介 (Project Overview)

本專案實作一個**最簡化、標準版 (Baseline)** 的電商結帳頁面，作為 A/B Testing 的 Control Group。

**核心特點:**
- ✅ 僅支援**信用卡付款** (移除貨到付款)
- ✅ **固定運費 $50** (無免運邏輯)
- ✅ **單頁式結帳流程**
- ✅ **綠色主色調、卡片式設計**
- ✅ **響應式佈局** (支援手機/平板/桌面)

---

## 技術棧 (Tech Stack)

| 類別 | 技術 |
|------|------|
| **後端** | Python 3.9+ + Flask 3.0.0 |
| **前端** | HTML5 + CSS3 + Bootstrap 5 |
| **資料** | In-memory Mock Data (無資料庫) |
| **部署** | 開發伺服器 (可擴展至 Gunicorn/Docker) |

---

## 使用以下測試卡號:
- **卡號**: `4111-1111-1111-1111`
- **到期日**: `12/25`
- **CVV**: `123`

---

## 專案結構 (Project Structure)

```
DevOps E-Commerce/
├── app.py                 # Flask 主程式 (路由、Mock 資料)
├── requirements.txt       # Python 依賴清單
├── README.md             # 專案文件 (本檔案)
├── PRD.md                # 產品需求文件
├── constitution.md       # 開發準則
├── static/               # 靜態資源
│   ├── css/
│   │   └── style.css     # 自訂樣式 (綠色主題、卡片設計)
│   └── js/
│       └── main.js       # 前端互動邏輯 (表單驗證、AJAX)
└── templates/            # HTML 模板
    └── index.html        # 結帳頁面模板
```

---

## 功能說明 (Features)

### 區塊 A: 頂部資訊區
- 付款方式 (固定顯示「信用卡付款」)
- 收貨方式 (顯示「宅配」)
- 發票載具 (顯示簡易選單)

### 區塊 B: 付款詳情
- 信用卡號碼 (自動格式化為 `XXXX-XXXX-XXXX-XXXX`)
- 到期日 (自動格式化為 `MM/YY`)
- CVV 安全碼 (限制 3 碼數字)

### 區塊 C: 訂單總計
- 商品總額: **$170**
- 運費: **$50** (固定)
- 總計: **$220**

### 區塊 D: 行動呼籲
- ✅ 即時表單驗證與回饋

### 文件規範
- ✅ 繁體中文為主，技術術語輔以英文
- ✅ 詳細的程式碼註解

---

## API 端點 (API Endpoints)

### `GET /`
**描述**: 渲染結帳頁面

**回應**: HTML 頁面

---

### `POST /checkout`
**描述**: 處理結帳請求

**請求參數**:
```json
{
  "card_number": "4111-1111-1111-1111",
  "expiry_date": "12/25",
  "cvv": "123",
  "delivery_method": "宅配",
  "invoice_type": "手機載具"
}
```

**成功回應**:
```json
{
  "status": "success",
  "message": "訂單已成功建立！",
  "order": {
    "order_id": "ORD-2025112200001",
    "total": 220,
    "payment_method": "信用卡",
    "delivery_method": "宅配",
    "invoice_type": "手機載具",
    "status": "已成立"
  }
}
```

**錯誤回應**:
```json
{
  "status": "error",
  "message": "請填寫完整的信用卡資訊"
}
```

---

## 測試指南 (Testing Guide)

### 視覺驗證
1. 開啟 `http://localhost:5000`
2. 確認以下元素:
   - ✅ 綠色按鈕與主色調
   - ✅ 卡片式容器 (白色背景、圓角、陰影)
   - ✅ 訂單總計顯示 **$220**

### 功能驗證
1. 填寫測試信用卡資料
2. 點擊「結帳」按鈕
3. 確認顯示成功訊息與訂單編號

### 響應式驗證
調整瀏覽器視窗大小:
- **手機**: 375px
- **平板**: 768px
- **桌面**: 1920px

---

## 後續擴充方向 (Future Enhancements)

此為 Baseline 版本，後續可能加入:

- 多種付款方式 (PayPal, Apple Pay)
- 免運邏輯 (滿額免運提示)
- 真實付款串接 (Stripe, TapPay)
- 資料庫整合 (訂單儲存至 PostgreSQL/MySQL)
- 訂單確認信 (Email notification)

---

## 授權與貢獻 (License)

本專案僅供學習與測試用途。

**開發者**: Professional Developer  
**日期**: 2025-11-22  
**版本**: Baseline V3
