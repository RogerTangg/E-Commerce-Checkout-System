"""
電商結帳系統 - Flask 後端 (E-commerce Checkout System - Flask Backend)
Baseline V3 + COD Feature Toggle + Free Shipping Nudge

Author: Professional Developer
Date: 2025-11-23
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import time
from datetime import datetime

app = Flask(__name__)

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
    裝飾器：監控請求指標
    (Decorator: Monitor request metrics)
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        metrics["total_requests"] += 1
        metrics["last_request_time"] = start_time
        
        try:
            result = f(*args, **kwargs)
            response_time = time.time() - start_time
            metrics["total_response_time"] += response_time
            return result
        except Exception as e:
            metrics["error_requests"] += 1
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
    日誌 API 端點
    (Logs API endpoint)
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
    
    # 根據實際數據生成動態日誌
    logs = []
    
    # 系統啟動日誌
    logs.append({
        "level": "success",
        "message": f"System started successfully - Uptime: {int(uptime)} seconds",
        "timestamp": datetime.fromtimestamp(metrics['uptime_start']).strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # 請求統計日誌
    if metrics['total_requests'] > 0:
        logs.append({
            "level": "info",
            "message": f"Total requests processed: {metrics['total_requests']} | Avg response time: {avg_response_time:.1f}ms",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # 訂單相關日誌
    if metrics['orders_created'] > 0:
        logs.append({
            "level": "success",
            "message": f"Orders created: {metrics['orders_created']} | Total sales: ${metrics['total_sales']}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # 錯誤率相關日誌
    if error_rate > 5:
        logs.append({
            "level": "error",
            "message": f"High error rate detected: {error_rate:.2f}% - Immediate attention required!",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    elif error_rate > 1:
        logs.append({
            "level": "warning",
            "message": f"Elevated error rate: {error_rate:.2f}% - Monitoring recommended",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        logs.append({
            "level": "info",
            "message": f"Error rate within normal range: {error_rate:.2f}%",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # 響應時間相關日誌
    if avg_response_time > 500:
        logs.append({
            "level": "warning",
            "message": f"High response time detected: {avg_response_time:.1f}ms exceeds 500ms threshold",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # 最後請求時間日誌
    if metrics['last_request_time'] != metrics['uptime_start']:
        logs.append({
            "level": "info",
            "message": f"Last request received at: {datetime.fromtimestamp(metrics['last_request_time']).strftime('%H:%M:%S')}",
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
    
    def get_status(health):
        """根據健康度返回狀態"""
        if health >= 95:
            return "healthy"
        elif health >= 80:
            return "warning"
        else:
            return "degraded"
    
    # 使用 kebab-case 的 key 以匹配 Dashboard 的 SVG 元素 ID
    services = {
        "load-balancer": {
            "name": "Load Balancer",
            "health": round(base_health, 1),
            "status": get_status(base_health),
            "requests_handled": metrics["total_requests"]
        },
        "api-gateway": {
            "name": "API Gateway", 
            "health": round(base_health - 1, 1),
            "status": get_status(base_health - 1),
            "avg_latency": round(avg_response_time * 0.3, 1)  # Gateway 處理約 30% 的延遲
        },
        "user-service": {
            "name": "User Service",
            "health": round(base_health - 2, 1),
            "status": get_status(base_health - 2),
            "active_sessions": max(1, metrics["total_requests"] // 3)
        },
        "order-service": {
            "name": "Order Service",
            "health": round(base_health - 3, 1),
            "status": get_status(base_health - 3),
            "orders_processed": metrics["orders_created"]
        },
        "payment-service": {
            "name": "Payment Service",
            "health": round(base_health - 4, 1),
            "status": get_status(base_health - 4),
            "transactions": metrics["orders_created"],
            "total_amount": metrics["total_sales"]
        },
        "database": {
            "name": "Database",
            "health": round(base_health - 1, 1),
            "status": get_status(base_health - 1),
            "connections": min(100, max(1, metrics["total_requests"] // 2)),
            "query_time": round(avg_response_time * 0.4, 1)  # DB 處理約 40% 的延遲
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
