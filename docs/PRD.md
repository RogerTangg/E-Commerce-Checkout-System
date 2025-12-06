# Product Requirement Document: E-commerce Checkout System (Baseline V3)

## 1. 專案概觀 (Project Overview)
本專案旨在建立一個**最簡化、標準版 (Baseline)** 的電商結帳頁面。
此版本將作為 A/B Testing 的 **Control Group (對照組)**。在此階段，我們**不實作**複雜的促銷邏輯或多樣化付款方式，僅保留最核心的信用卡結帳流程。

**核心變更 (V3)：**
1.  **移除**「貨到付款 (Cash on Delivery)」選項。
2.  **移除**「免運湊單提示 (Free Shipping Nudge)」邏輯。
3.  **保留** 既有的 UI 視覺風格 (綠色主色調、卡片式設計)。

---

## 2. 技術堆疊 (Tech Stack)
* **Language**: Python 3.9+
* **Web Framework**: Flask
* **Frontend**: HTML5, CSS3 (搭配 Bootstrap 5 Utility Classes 快速排版)
* **Database**: 無 (使用 In-memory Mock Data)

---

## 3. 介面與功能需求 (UI/UX Requirements)

### 3.1 全域視覺 (Visual Style)
* **風格依據**：參考提供的 UI 原型圖（綠色按鈕、圓角卡片、置中佈局）。
* **佈局**：單頁式結帳 (Single Page Checkout)。內容置於中央白色卡片容器中。

### 3.2 頁面區塊詳細定義

#### **區塊 A：頂部資訊區 (Top Info Blocks)**
保留原型圖中的三欄位佈局，但簡化互動。
1.  **付款方式**：固定顯示「信用卡付款 (Credit Card)」。(無 Tab 切換功能)
2.  **收貨方式**：顯示「宅配 (Home Delivery)」或類似靜態文字/選單。
3.  **發票載具**：顯示簡易下拉選單 (如：手機載具/會員載具)。

#### **區塊 B：付款詳情 (Payment Details)**
直接顯示信用卡輸入表單，無需隱藏或切換。
* **標題**：信用卡資訊
* **必要欄位**：
    * 信用卡號碼 (Card Number)
    * 到期日 (Expiry Date) - MM/YY
    * CVV 安全碼

#### **區塊 C：訂單總計 (Order Summary)**
純靜態顯示，**不包含**任何動態免運計算邏輯。
* **商品總額 (Subtotal)**：$170
* **運費 (Shipping)**：$50 (固定收取，無視金額大小)
* **總計 (Total)**：$220

#### **區塊 D：行動呼籲 (Action)**
* **結帳按鈕**：綠色全寬按鈕，文字為「結帳 (Place Order)」。

---

## 4. 資料定義 (Data Schema)

### 4.1 Mock Data (`app.py`)
資料結構寫死，確保金額與截圖一致。

```python
mock_cart = {
    "subtotal": 170,
    "shipping_fee": 50,  # 固定運費
    "total": 220,        # 170 + 50
    "items": [           # 僅用於後續擴充，目前前端可僅顯示總額
        {"name": "Sample Item", "price": 170}
    ]
}