"""
電商結帳系統 - Flask 後端 (E-commerce Checkout System - Flask Backend)
Baseline V3 + COD Feature Toggle + Free Shipping Nudge

Author: Professional Developer
Date: 2025-11-23
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
import time
from datetime import datetime

app = Flask(__name__)


# ===== Dashboard 靜態文件路由 =====
@app.route('/dashboard/')
@app.route('/dashboard/<path:filename>')
def serve_dashboard(filename='observability-dashboard.html'):
    """
    提供 dashboard 資料夾中的靜態文件
    (Serve static files from the dashboard folder)
    """
    dashboard_dir = os.path.join(app.root_path, 'dashboard')
    return send_from_directory(dashboard_dir, filename)

# Mock 購物車資料 (Mock Cart Data)
# 為了測試湊單功能，預設金額設為 170 (未滿 200)
mock_cart = {
    "items": [
        {"name": "精選咖啡豆 (Premium Coffee Beans)", "price": 120, "quantity": 1},
        {"name": "濾掛式咖啡包 (Drip Coffee Bag)", "price": 60, "quantity": 1}
    ]
}

# 監控指標 (Monitoring Metrics)
metrics = {
    "total_requests": 0,
    "error_requests": 0,
    "total_response_time": 0,
    "orders_created": 0,
    "total_sales": 0,
    "last_request_time": time.time(),
    "uptime_start": time.time()
}

# 響應時間歷史記錄 (Response Time History) - 用於圖表
response_time_history = []
MAX_HISTORY_POINTS = 20

# 故障模擬狀態 (Fault Injection State)
fault_state = {
    "database_down": False,
    "high_latency": False,
    "latency_ms": 0
}

# 日誌歷史記錄 (Log History) - 保留最近 100 條
log_history = []


def add_log(level, message, category="system"):
    """
    新增日誌記錄到歷史
    (Add log entry to history)
    
    Args:
        level: 日誌等級 (info, success, warning, error)
        message: 日誌訊息
        category: 日誌類別 (system, order, error, security)
    """
    global log_history
    log_entry = {
        "level": level,
        "message": message,
        "category": category,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    log_history.append(log_entry)
    # 只保留最近 100 條
    if len(log_history) > 100:
        log_history = log_history[-100:]
    # 同時輸出到控制台
    print(f"[{log_entry['timestamp']}] [{level.upper()}] [{category}] {message}")


def load_toggles():
    """
    載入 Feature Toggles 設定檔
    (Load Feature Toggles configuration)
    
    Returns:
        dict: Toggle 設定字典，如果檔案不存在則返回預設值
    """
    toggles_path = os.path.join(os.path.dirname(__file__), 'toggles.json')
    
    try:
        with open(toggles_path, 'r', encoding='utf-8') as f:
            toggles = json.load(f)
            return toggles
    except FileNotFoundError:
        print(f"Warning: {toggles_path} not found. Using default toggles.")
        return {"enable_cod": False, "enable_free_shipping_nudge": False}
    except json.JSONDecodeError as e:
        print(f"Error parsing toggles.json: {e}. Using default toggles.")
        return {"enable_cod": False, "enable_free_shipping_nudge": False}


def monitor_request(f):
    """
    裝飾器：監控請求指標，支援故障注入
    (Decorator: Monitor request metrics with fault injection support)
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        metrics["total_requests"] += 1
        metrics["last_request_time"] = start_time
        
        # 模擬高延遲 (Simulate high latency)
        if fault_state["high_latency"] and fault_state["latency_ms"] > 0:
            time.sleep(fault_state["latency_ms"] / 1000)
        
        try:
            # 檢查資料庫故障狀態 (Check database fault state)
            if fault_state["database_down"]:
                metrics["error_requests"] += 1
                response_time_ms = (time.time() - start_time) * 1000
                response_time_history.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "value": response_time_ms,
                    "is_error": True
                })
                if len(response_time_history) > MAX_HISTORY_POINTS:
                    response_time_history.pop(0)
                add_log("error", f"Database connection failed - Service unavailable", "error")
                from flask import jsonify
                return jsonify({
                    "status": "error",
                    "message": "Database connection failed. Service temporarily unavailable.",
                    "error_code": "DB_CONNECTION_FAILED"
                }), 503
            
            result = f(*args, **kwargs)
            response_time = time.time() - start_time
            response_time_ms = response_time * 1000
            metrics["total_response_time"] += response_time
            
            # 記錄響應時間歷史
            response_time_history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "value": response_time_ms,
                "is_error": False
            })
            if len(response_time_history) > MAX_HISTORY_POINTS:
                response_time_history.pop(0)
            
            return result
        except Exception as e:
            metrics["error_requests"] += 1
            add_log("error", f"Request failed: {str(e)}", "error")
            raise e
    
    wrapper.__name__ = f.__name__
    return wrapper


def calculate_cart_totals(cart_items):
    """
    計算購物車總金額與運費
    (Calculate cart subtotal and shipping fee)
    """
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    
    # 免運門檻邏輯 (Free Shipping Threshold Logic)
    # 滿 200 免運，否則運費 60
    shipping_fee = 0 if subtotal >= 200 else 60
    
    total = subtotal + shipping_fee
    
    return {
        "subtotal": subtotal,
        "shipping_fee": shipping_fee,
        "total": total,
        "items": cart_items
    }


@app.route('/cart')
def cart():
    """
    購物車頁面路由
    (Cart route - Display cart with free shipping nudge)
    """
    toggles = load_toggles()
    enable_nudge = toggles.get('enable_free_shipping_nudge', False)
    
    # 計算金額
    cart_data = calculate_cart_totals(mock_cart['items'])
    
    nudge_message = None
    diff = None
    
    # 計算差額並傳給前端
    if cart_data['subtotal'] < 200:
        diff = 200 - cart_data['subtotal']
        # 只有當 Toggle 開啟時才顯示訊息
        if enable_nudge:
            nudge_message = f"再購買 ${diff} 即可免運費！"
    
    return render_template(
        'cart.html',
        cart=cart_data,
        nudge_message=nudge_message,
        diff=diff
    )


@app.route('/checkout-options')
@monitor_request
def checkout_options():
    """
    結帳選項頁面路由
    (Checkout Options route)
    """
    toggles = load_toggles()
    
    # 重新計算金額
    cart_data = calculate_cart_totals(mock_cart['items'])
    return render_template('checkout.html', cart=cart_data, toggles=toggles)


@app.route('/')
@monitor_request
def index():
    """
    首頁路由 - 顯示購物車內容與湊單提示
    (Homepage route - Display cart contents and free shipping nudge)
    """
    toggles = load_toggles()
    enable_nudge = toggles.get('enable_free_shipping_nudge', False)
    
    # 計算金額
    cart_data = calculate_cart_totals(mock_cart['items'])
    
    nudge_message = None
    
    # 湊單提示邏輯 (Nudge Logic)
    # 只有當 Toggle 開啟且未達免運門檻時才顯示
    if enable_nudge and cart_data['subtotal'] < 200:
        diff = 200 - cart_data['subtotal']
        nudge_message = f"再購買 ${diff} 即可免運費！"
        
    return render_template(
        'cart.html',
        cart=cart_data,
        nudge_message=nudge_message
    )


@app.route('/payment')
@monitor_request
def payment():
    """
    付款頁面路由
    """
    toggles = load_toggles()
    enable_cod = toggles.get('enable_cod', False)
    
    # 重新計算金額
    cart_data = calculate_cart_totals(mock_cart['items'])
    
    return render_template(
        'payment.html', 
        cart=cart_data, 
        enable_cod=enable_cod
    )


@app.route('/success')
@monitor_request
def success():
    """
    結帳成功頁面路由
    (Checkout Success route)
    """
    order_id = request.args.get('order_id')
    total = request.args.get('total')
    payment_method = request.args.get('payment_method')
    delivery_method = request.args.get('delivery_method')
    
    return render_template(
        'success.html',
        order_id=order_id,
        total=total,
        payment_method=payment_method,
        delivery_method=delivery_method
    )


@app.route('/logs')
def get_logs():
    """
    日誌 API 端點 - 返回歷史日誌記錄
    (Logs API endpoint - Returns historical log entries)
    """
    current_time = time.time()
    uptime = current_time - metrics["uptime_start"]
    
    # 計算平均響應時間
    avg_response_time = 0
    if metrics["total_requests"] > 0:
        avg_response_time = (metrics["total_response_time"] / metrics["total_requests"]) * 1000
    
    # 計算錯誤率
    error_rate = 0
    if metrics["total_requests"] > 0:
        error_rate = (metrics["error_requests"] / metrics["total_requests"]) * 100
    
    # 合併歷史日誌和即時狀態日誌
    logs = []
    
    # 加入歷史日誌 (最新的在前)
    logs.extend(reversed(log_history[-20:]))  # 最近 20 條歷史日誌
    
    # 系統狀態日誌
    logs.append({
        "level": "info",
        "message": f"[STATUS] Uptime: {int(uptime)}s | Requests: {metrics['total_requests']} | Errors: {metrics['error_requests']}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # 故障狀態日誌
    if fault_state["database_down"]:
        logs.insert(0, {
            "level": "error",
            "message": "[ALERT] DATABASE IS DOWN - All database operations will fail!",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    if fault_state["high_latency"]:
        logs.insert(0, {
            "level": "warning",
            "message": f"[ALERT] High latency injection active: +{fault_state['latency_ms']}ms per request",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # 錯誤率警告
    if error_rate > 5:
        logs.insert(0, {
            "level": "error",
            "message": f"[CRITICAL] Error rate {error_rate:.2f}% exceeds SLO threshold (5%)!",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    elif error_rate > 1:
        logs.insert(0, {
            "level": "warning",
            "message": f"[WARNING] Elevated error rate: {error_rate:.2f}%",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return jsonify(logs)


@app.route('/metrics')
def get_metrics():
    """
    監控指標 API 端點
    (Monitoring metrics API endpoint)
    """
    current_time = time.time()
    uptime = current_time - metrics["uptime_start"]
    
    # 計算平均響應時間
    avg_response_time = 0
    if metrics["total_requests"] > 0:
        avg_response_time = (metrics["total_response_time"] / metrics["total_requests"]) * 1000  # ms
    
    # 計算錯誤率
    error_rate = 0
    if metrics["total_requests"] > 0:
        error_rate = (metrics["error_requests"] / metrics["total_requests"]) * 100
    
    # 計算吞吐量 (每分鐘請求數)
    throughput = 0
    if uptime > 0:
        throughput = (metrics["total_requests"] / uptime) * 60
    
    # 計算平均購物車價值
    avg_cart_value = calculate_cart_totals(mock_cart['items'])['total']
    
    # 動態計算系統健康度 (基於錯誤率和響應時間)
    # 基礎健康度 100%，錯誤率每 1% 扣 5 分，響應時間超過 200ms 每 100ms 扣 2 分
    system_health = 100.0
    system_health -= error_rate * 5  # 錯誤率影響
    if avg_response_time > 200:
        system_health -= ((avg_response_time - 200) / 100) * 2  # 響應時間影響
    system_health = max(0, min(100, system_health))  # 限制在 0-100 範圍
    
    # 動態計算可用性 (基於錯誤率)
    availability = max(0, 100 - error_rate)
    
    # Error Budget 計算 (基於 SLO 目標 99.9%)
    # 每月允許 0.1% 的錯誤時間 = 43.2 分鐘
    # 計算已使用的 budget 百分比
    monthly_budget_used = min(100, error_rate * 10)  # 錯誤率的 10 倍作為已使用 budget
    quarterly_budget_used = min(100, error_rate * 5)
    annual_budget_used = min(100, error_rate * 2)
    
    return jsonify({
        "system_health": round(system_health, 1),
        "avg_response_time": round(avg_response_time, 1),
        "error_rate": round(error_rate, 2),
        "throughput": round(throughput, 1),
        "total_orders": metrics["orders_created"],
        "total_sales": metrics["total_sales"],
        "avg_cart_value": avg_cart_value,
        "uptime_seconds": round(uptime, 0),
        "total_requests": metrics["total_requests"],
        "error_requests": metrics["error_requests"],
        "last_request": datetime.fromtimestamp(metrics["last_request_time"]).strftime("%Y-%m-%d %H:%M:%S"),
        "error_budget": {
            "monthly_remaining": round(max(0, 100 - monthly_budget_used), 1),
            "quarterly_remaining": round(max(0, 100 - quarterly_budget_used), 1),
            "annual_remaining": round(max(0, 100 - annual_budget_used), 1)
        },
        "slo_status": {
            "availability": round(availability, 2),
            "latency_target": "<200ms",
            "latency_actual": f"{round(avg_response_time, 1)}ms",
            "latency_status": "healthy" if avg_response_time < 200 else ("warning" if avg_response_time < 500 else "critical")
        }
    })


# ========================================
# 故障注入 API (Fault Injection APIs)
# ========================================

@app.route('/fault/inject', methods=['POST'])
def inject_fault():
    """
    故障注入 API - 模擬系統故障
    (Fault Injection API - Simulate system failures)
    
    支援的故障類型:
    - database_down: 資料庫連線故障
    - high_latency: 高延遲 (需指定 latency_ms)
    
    Request Body (JSON):
    {
        "fault_type": "database_down" | "high_latency",
        "latency_ms": 2000  // 僅用於 high_latency
    }
    """
    try:
        data = request.get_json() or {}
        fault_type = data.get('fault_type', 'database_down')
        latency_ms = data.get('latency_ms', 2000)
        
        if fault_type == 'database_down':
            fault_state["database_down"] = True
            add_log("error", "🔴 FAULT INJECTED: Database connection failure simulated", "system")
            return jsonify({
                "status": "success",
                "message": "Database failure injected. All database operations will fail.",
                "fault_type": "database_down",
                "current_state": fault_state
            })
        
        elif fault_type == 'high_latency':
            fault_state["high_latency"] = True
            fault_state["latency_ms"] = latency_ms
            add_log("warning", f"🟡 FAULT INJECTED: High latency ({latency_ms}ms) simulated", "system")
            return jsonify({
                "status": "success",
                "message": f"High latency ({latency_ms}ms) injected for all requests.",
                "fault_type": "high_latency",
                "latency_ms": latency_ms,
                "current_state": fault_state
            })
        
        else:
            return jsonify({
                "status": "error",
                "message": f"Unknown fault type: {fault_type}. Supported: database_down, high_latency"
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to inject fault: {str(e)}"
        }), 500


@app.route('/fault/recover', methods=['POST'])
def recover_fault():
    """
    故障恢復 API - 恢復所有模擬故障
    (Fault Recovery API - Recover from all simulated failures)
    
    Request Body (JSON) - 可選:
    {
        "fault_type": "database_down" | "high_latency" | "all"
    }
    """
    try:
        data = request.get_json() or {}
        fault_type = data.get('fault_type', 'all')
        
        recovered = []
        
        if fault_type in ['database_down', 'all'] and fault_state["database_down"]:
            fault_state["database_down"] = False
            recovered.append("database_down")
            add_log("success", "🟢 RECOVERY: Database connection restored", "system")
        
        if fault_type in ['high_latency', 'all'] and fault_state["high_latency"]:
            fault_state["high_latency"] = False
            fault_state["latency_ms"] = 0
            recovered.append("high_latency")
            add_log("success", "🟢 RECOVERY: Normal latency restored", "system")
        
        if not recovered:
            return jsonify({
                "status": "info",
                "message": "No active faults to recover from.",
                "current_state": fault_state
            })
        
        return jsonify({
            "status": "success",
            "message": f"Recovered from faults: {', '.join(recovered)}",
            "recovered_faults": recovered,
            "current_state": fault_state
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to recover: {str(e)}"
        }), 500


@app.route('/fault/status')
def fault_status():
    """
    故障狀態查詢 API
    (Fault Status Query API)
    """
    return jsonify({
        "status": "success",
        "fault_state": fault_state,
        "is_degraded": fault_state["database_down"] or fault_state["high_latency"],
        "active_faults": [
            fault for fault, active in [
                ("database_down", fault_state["database_down"]),
                ("high_latency", fault_state["high_latency"])
            ] if active
        ]
    })


@app.route('/chart-data')
def get_chart_data():
    """
    圖表數據 API - 返回用於前端圖表的歷史數據
    (Chart Data API - Returns historical data for frontend charts)
    """
    # 計算錯誤率歷史
    error_count = sum(1 for r in response_time_history if r.get("is_error", False))
    total_count = len(response_time_history) if response_time_history else 1
    current_error_rate = (error_count / total_count) * 100
    
    return jsonify({
        "response_times": [r["value"] for r in response_time_history],
        "timestamps": [r["time"] for r in response_time_history],
        "error_flags": [r.get("is_error", False) for r in response_time_history],
        "current_error_rate": round(current_error_rate, 2),
        "data_points": len(response_time_history)
    })


@app.route('/services')
def get_services():
    """
    服務架構狀態 API 端點
    (Service architecture status API endpoint)
    
    服務 ID 對應 Dashboard SVG 元素:
    - load-balancer -> #load-balancer-rect
    - api-gateway -> #api-gateway-rect  
    - user-service -> #user-service-rect
    - order-service -> #order-service-rect
    - payment-service -> #payment-service-rect
    - database -> #database-rect
    - redis-cache -> #redis-cache-rect
    """
    current_time = time.time()
    uptime = current_time - metrics["uptime_start"]
    
    # 計算錯誤率
    error_rate = 0
    if metrics["total_requests"] > 0:
        error_rate = (metrics["error_requests"] / metrics["total_requests"]) * 100
    
    # 計算平均響應時間
    avg_response_time = 0
    if metrics["total_requests"] > 0:
        avg_response_time = (metrics["total_response_time"] / metrics["total_requests"]) * 1000
    
    # 基礎健康度計算
    base_health = 100.0
    base_health -= error_rate * 2  # 錯誤率影響
    if avg_response_time > 200:
        base_health -= ((avg_response_time - 200) / 100) * 1
    base_health = max(0, min(100, base_health))
    
    def get_status(health, is_down=False):
        """根據健康度返回狀態"""
        if is_down:
            return "degraded"
        if health >= 95:
            return "healthy"
        elif health >= 80:
            return "warning"
        else:
            return "degraded"
    
    # 資料庫故障影響計算
    db_is_down = fault_state["database_down"]
    db_health = 0 if db_is_down else round(base_health - 1, 1)
    
    # 高延遲影響
    latency_penalty = fault_state["latency_ms"] / 100 if fault_state["high_latency"] else 0
    
    # 使用 kebab-case 的 key 以匹配 Dashboard 的 SVG 元素 ID
    services = {
        "load-balancer": {
            "name": "Load Balancer",
            "health": round(max(0, base_health - latency_penalty), 1),
            "status": get_status(base_health - latency_penalty),
            "requests_handled": metrics["total_requests"]
        },
        "api-gateway": {
            "name": "API Gateway", 
            "health": round(max(0, base_health - 1 - latency_penalty), 1),
            "status": get_status(base_health - 1 - latency_penalty),
            "avg_latency": round(avg_response_time * 0.3 + fault_state.get("latency_ms", 0) * 0.3, 1)
        },
        "user-service": {
            "name": "User Service",
            "health": round(max(0, base_health - 2 - (50 if db_is_down else 0)), 1),
            "status": "warning" if db_is_down else get_status(base_health - 2),
            "active_sessions": max(1, metrics["total_requests"] // 3)
        },
        "order-service": {
            "name": "Order Service",
            "health": round(max(0, base_health - 3 - (50 if db_is_down else 0)), 1),
            "status": "degraded" if db_is_down else get_status(base_health - 3),
            "orders_processed": metrics["orders_created"]
        },
        "payment-service": {
            "name": "Payment Service",
            "health": round(max(0, base_health - 4 - (50 if db_is_down else 0)), 1),
            "status": "degraded" if db_is_down else get_status(base_health - 4),
            "transactions": metrics["orders_created"],
            "total_amount": metrics["total_sales"]
        },
        "database": {
            "name": "Database",
            "health": db_health,
            "status": get_status(db_health, is_down=db_is_down),
            "connections": 0 if db_is_down else min(100, max(1, metrics["total_requests"] // 2)),
            "query_time": 0 if db_is_down else round(avg_response_time * 0.4, 1),
            "is_down": db_is_down
        },
        "redis-cache": {
            "name": "Redis Cache",
            "health": round(base_health, 1),
            "status": get_status(base_health),
            "hit_rate": 95.5,
            "memory_usage": "256MB"
        }
    }
    
    return jsonify(services)


@app.route('/checkout', methods=['POST'])
@monitor_request
def checkout():
    """
    結帳路由
    """
    try:
        toggles = load_toggles()
        enable_cod = toggles.get('enable_cod', False)
        
        # 重新計算金額確保數據一致
        cart_data = calculate_cart_totals(mock_cart['items'])
        
        payment_method = request.form.get('payment_method', 'credit_card')
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        delivery_method = request.form.get('delivery_method', '宅配')
        invoice_type = request.form.get('invoice_type', '手機載具')
        
        # DevSecOps 安全驗證
        if payment_method == 'cod' and not enable_cod:
            return jsonify({
                "status": "error",
                "message": "貨到付款功能目前不可用",
                "error_code": "FEATURE_DISABLED"
            }), 403
        
        if payment_method == 'credit_card':
            if not card_number or not expiry_date or not cvv:
                return jsonify({
                    "status": "error",
                    "message": "請填寫完整的信用卡資訊"
                }), 400
            payment_display = "信用卡"
        elif payment_method == 'cod':
            payment_display = "貨到付款"
        else:
            return jsonify({
                "status": "error",
                "message": "無效的付款方式"
            }), 400
        
        # 更新指標
        metrics["orders_created"] += 1
        metrics["total_sales"] += cart_data["total"]
        
        order_data = {
            "order_id": "ORD-2025112300001",
            "total": cart_data["total"],
            "payment_method": payment_display,
            "delivery_method": delivery_method,
            "invoice_type": invoice_type,
            "status": "已成立"
        }
        
        return jsonify({
            "status": "success",
            "message": f"訂單已成功建立！付款方式：{payment_display}",
            "order": order_data
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"系統錯誤: {str(e)}"
        }), 500


@app.after_request
def after_request(response):
    """
    添加 CORS 標頭以允許跨域請求
    (Add CORS headers to allow cross-origin requests)
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

    