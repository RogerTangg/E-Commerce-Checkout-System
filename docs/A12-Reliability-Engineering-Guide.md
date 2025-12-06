# A12 可靠性工程作業指南
## Reliability Engineering Assignment Guide

---

## 📋 作業概述 (Assignment Overview)

本指南說明如何在 E-Commerce Checkout System 專案中完成 A12 可靠性工程作業。作業分為兩個主要任務：
1. **Task 1**: Observability 驗證 (Observability Validation)
2. **Task 2**: Runbook 驗證 (Runbook Verification)

---

## 🏗️ 系統架構 (System Architecture)

本專案採用簡化的 Flask 單體架構，模擬微服務環境：

```
┌─────────────────────────────────────────────────────────────┐
│                    E-Commerce Checkout System                │
├─────────────────────────────────────────────────────────────┤
│  Frontend (HTML/JS)      │  Observability Dashboard          │
│  - index.html            │  - observability-dashboard.html   │
│  - cart.html             │  - Real-time metrics              │
│  - checkout.html         │  - Service status                 │
│  - payment.html          │  - Log viewer                     │
│  - success.html          │                                   │
├─────────────────────────────────────────────────────────────┤
│                     Flask Backend (app.py)                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Simulated Microservices:                                │ │
│  │ - Load Balancer    - API Gateway    - User Service      │ │
│  │ - Order Service    - Payment Service - Database         │ │
│  │ - Redis Cache                                           │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Fault Injection System:                                 │ │
│  │ - /fault/inject   (POST) - 注入故障                     │ │
│  │ - /fault/recover  (POST) - 恢復故障                     │ │
│  │ - /fault/status   (GET)  - 查詢故障狀態                 │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速開始 (Quick Start)

### 1. 啟動系統
```powershell
# 進入專案目錄
cd "c:\Users\Roger Tang\Desktop\Projects\DevOps Projects\E-Commerce-Checkout-System"

# 安裝依賴 (如果還沒安裝)
pip install -r requirements.txt

# 啟動 Flask 伺服器
python app.py
```

### 2. 訪問 Dashboard
- **Observability Dashboard**: http://localhost:5000/dashboard/observability-dashboard.html
- **主頁 (Shopping Cart)**: http://localhost:5000/

---

## 📊 Task 1: Observability 驗證

### 1.1 目標
驗證 Observability Dashboard 能夠正確顯示以下指標：
- 系統健康度 (System Health)
- 平均響應時間 (Avg Response Time)
- 錯誤率 (Error Rate)
- 吞吐量 (Throughput)
- Error Budget 狀態
- 服務架構健康度

### 1.2 驗證步驟

#### Step 1: 開啟 Dashboard
1. 確保 Flask 伺服器正在運行
2. 在瀏覽器中開啟 Dashboard: http://localhost:5000/dashboard/observability-dashboard.html

#### Step 2: 生成測試流量
```powershell
# 在 PowerShell 中執行多次請求來生成流量
for ($i=1; $i -le 10; $i++) { 
    curl http://localhost:5000/
    Start-Sleep -Milliseconds 500
}
```

#### Step 3: 觀察指標變化
觀察 Dashboard 上的以下指標：
- **System Health**: 應該顯示接近 100%
- **Avg Response Time**: 應該顯示低於 200ms
- **Error Rate**: 應該顯示 0% 或接近 0%
- **Throughput**: 應該顯示每分鐘請求數

#### Step 4: 截圖記錄
截取 Dashboard 完整畫面作為 Task 1 的證明。

### 1.3 API 端點說明

| API 端點 | 方法 | 說明 |
|---------|------|------|
| `/metrics` | GET | 返回系統指標 |
| `/services` | GET | 返回服務狀態 |
| `/logs` | GET | 返回系統日誌 |

---

## 🔧 Task 2: Runbook 驗證 (RB-01: Database Connectivity Failure)

### 2.1 Runbook 概述

**Runbook ID**: RB-01  
**故障類型**: Database Connectivity Failure  
**影響**: 所有需要資料庫的操作將失敗，包括結帳功能

### 2.2 故障注入測試流程

#### Phase 1: 準備階段
1. 確保系統正常運行
2. 開啟 Observability Dashboard
3. 記錄當前系統狀態（截圖）

#### Phase 2: 故障注入
```powershell
# 使用 PowerShell 注入資料庫故障
$body = '{"fault_type": "database_down"}'
Invoke-RestMethod -Uri "http://localhost:5000/fault/inject" -Method POST -Body $body -ContentType "application/json"
```

或使用 curl：
```powershell
curl -X POST http://localhost:5000/fault/inject -H "Content-Type: application/json" -d "{\"fault_type\": \"database_down\"}"
```

#### Phase 3: 驗證故障影響
1. **查看 Dashboard**: 觀察服務狀態變化
   - Database 服務應顯示為 "degraded"（紅色）
   - Order Service 和 Payment Service 應顯示為 "degraded" 或 "warning"
   - 錯誤率應該上升

2. **嘗試結帳操作**: 訪問購物車並嘗試結帳
   ```powershell
   curl http://localhost:5000/
   ```
   應該返回 503 錯誤

3. **查看故障狀態**:
   ```powershell
   curl http://localhost:5000/fault/status
   ```

4. **查看日誌**:
   ```powershell
   curl http://localhost:5000/logs
   ```
   應該看到資料庫故障相關的錯誤日誌

#### Phase 4: 故障恢復
```powershell
# 執行故障恢復
$body = '{"fault_type": "all"}'
Invoke-RestMethod -Uri "http://localhost:5000/fault/recover" -Method POST -Body $body -ContentType "application/json"
```

或使用 curl：
```powershell
curl -X POST http://localhost:5000/fault/recover -H "Content-Type: application/json" -d "{\"fault_type\": \"all\"}"
```

#### Phase 5: 驗證恢復
1. 再次查看 Dashboard - 所有服務應恢復為 "healthy"
2. 嘗試結帳操作 - 應該成功
3. 查看日誌 - 應該看到恢復成功的訊息

### 2.3 其他故障類型

除了資料庫故障，系統還支援高延遲故障注入：

```powershell
# 注入 2000ms 高延遲
$body = '{"fault_type": "high_latency", "latency_ms": 2000}'
Invoke-RestMethod -Uri "http://localhost:5000/fault/inject" -Method POST -Body $body -ContentType "application/json"
```

---

## 📝 作業繳交清單

### Task 1 需要繳交的項目：
- [ ] Dashboard 正常運行的截圖
- [ ] 系統指標說明（System Health, Response Time, Error Rate, Throughput）
- [ ] 服務架構圖顯示所有服務健康的截圖

### Task 2 需要繳交的項目：
- [ ] 故障注入前的系統狀態截圖
- [ ] 故障注入命令及輸出截圖
- [ ] 故障期間 Dashboard 顯示的截圖（顯示 Database degraded）
- [ ] 故障期間錯誤日誌截圖
- [ ] 故障恢復命令及輸出截圖
- [ ] 恢復後系統狀態截圖

---

## 🔍 故障注入 API 參考

### POST /fault/inject
注入故障

**Request Body:**
```json
{
    "fault_type": "database_down" | "high_latency",
    "latency_ms": 2000  // 僅用於 high_latency
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Database failure injected...",
    "fault_type": "database_down",
    "current_state": {
        "database_down": true,
        "high_latency": false,
        "latency_ms": 0
    }
}
```

### POST /fault/recover
恢復故障

**Request Body:**
```json
{
    "fault_type": "database_down" | "high_latency" | "all"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Recovered from faults: database_down",
    "recovered_faults": ["database_down"],
    "current_state": {
        "database_down": false,
        "high_latency": false,
        "latency_ms": 0
    }
}
```

### GET /fault/status
查詢故障狀態

**Response:**
```json
{
    "status": "success",
    "fault_state": {
        "database_down": false,
        "high_latency": false,
        "latency_ms": 0
    },
    "is_degraded": false,
    "active_faults": []
}
```

---

## 💡 疑難排解

### 問題 1: Dashboard 不更新
- 確保 Flask 伺服器正在運行
- 檢查瀏覽器 Console 是否有錯誤
- 嘗試手動刷新頁面

### 問題 2: 故障注入沒有效果
- 確保使用 POST 方法
- 確保 Content-Type 設定為 application/json
- 檢查 Request Body 格式是否正確

### 問題 3: 端口被占用
```powershell
# 查找占用 5000 端口的程序
netstat -ano | findstr :5000

# 終止程序 (替換 PID)
taskkill /F /PID <PID>
```

---

## 📚 相關文件

- [README.md](./README.md) - 專案說明
- [PRD.md](./PRD.md) - 產品需求文件
- [constitution.md](./constitution.md) - 專案規範
- [dashboard/manual.html](./dashboard/manual.html) - Dashboard 操作手冊

---

*Last Updated: 2025-01-15*
