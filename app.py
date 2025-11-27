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
import psycopg2

app = Flask(__name__)

# Database Configuration
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'ecommerce')
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

# 儲存最近的日誌 (Store recent logs)
recent_logs = []
MAX_LOGS = 50

def add_log(level, message):
    """
    新增日誌記錄 (Add log entry)
    """
    log_entry = {
        "level": level,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    recent_logs.insert(0, log_entry)
    if len(recent_logs) > MAX_LOGS:
        recent_logs.pop()
    print(f"[{level.upper()}] {message}")

def check_db_connection():
    """
    檢查資料庫連線 (Check Database Connection)
    Returns: True if connected, False otherwise
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=2
        )
        return True
    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()

def check_db_connection_or_raise():
    """
    檢查資料庫連線，若失敗則拋出例外 (Check DB connection, raise if failed)
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=2
        )
        return True
    except Exception as e:
        add_log("error", f"Database connection failed: {e}")
        metrics["error_requests"] += 1
        raise e
    finally:
        if conn:
            conn.close()

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


@app.route('/checkout-options')
@monitor_request
def checkout_options():
    """
    結帳選項頁面路由
    (Checkout Options route)
    """
    # 重新計算金額
    cart_data = calculate_cart_totals(mock_cart['items'])
    return render_template('checkout.html', cart=cart_data)


@app.route('/')
@monitor_request
def index():
    """
    首頁路由 - 顯示購物車內容與湊單提示
    (Homepage route - Display cart contents and free shipping nudge)
    """
    add_log("info", f"User accessed homepage - Total requests: {metrics['total_requests']}")
    
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
    add_log("info", "User accessed payment page")
    
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
    日誌 API 端點 - 返回真實日誌
    (Logs API endpoint - Returns real logs)
    """
    # 如果沒有日誌，返回一些初始狀態
    if len(recent_logs) == 0:
        return jsonify([
            {
                "level": "info",
                "message": f"System started - Uptime: {round(time.time() - metrics['uptime_start'], 0)} seconds",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ])
    
    return jsonify(recent_logs[:20])


@app.route('/metrics')
def get_metrics():
    """
    監控指標 API 端點 - 包含資料庫健康檢查
    (Monitoring metrics API endpoint - includes DB health check)
    """
    current_time = time.time()
    uptime = current_time - metrics["uptime_start"]
    
    # 實際檢查資料庫連線狀態
    db_healthy = check_db_connection()
    
    # 如果資料庫斷線，記錄警報
    if not db_healthy:
        add_log("error", "ALERT: Database connection failed - Service Unavailable")
    
    # 計算平均響應時間
    avg_response_time = 0
    if metrics["total_requests"] > 0:
        avg_response_time = (metrics["total_response_time"] / metrics["total_requests"]) * 1000  # ms
    
    # 計算錯誤率
    error_rate = 0
    if metrics["total_requests"] > 0:
        error_rate = (metrics["error_requests"] / metrics["total_requests"]) * 100
    
    # 如果資料庫斷線，錯誤率設為 100%
    if not db_healthy:
        error_rate = 100.0
    
    # 計算吞吐量 (每分鐘請求數)
    throughput = 0
    if uptime > 0:
        throughput = (metrics["total_requests"] / uptime) * 60
    
    # 計算平均購物車價值
    avg_cart_value = calculate_cart_totals(mock_cart['items'])['total']
    
    # 系統健康度：基於資料庫狀態與錯誤率
    if not db_healthy:
        system_health = 0.0  # 資料庫斷線 = 健康度 0%
    else:
        system_health = max(0, 98.5 - (error_rate * 0.5))
    
    return jsonify({
        "system_health": round(system_health, 1),
        "db_status": "healthy" if db_healthy else "down",
        "avg_response_time": round(avg_response_time, 1),
        "error_rate": round(error_rate, 2),
        "throughput": round(throughput, 1),
        "total_orders": metrics["orders_created"],
        "total_sales": metrics["total_sales"],
        "avg_cart_value": avg_cart_value,
        "uptime_seconds": round(uptime, 0),
        "last_request": datetime.fromtimestamp(metrics["last_request_time"]).strftime("%Y-%m-%d %H:%M:%S"),
        "error_budget": {
            "monthly_remaining": max(0, 85 - (error_rate * 1.0)),
            "quarterly_remaining": max(0, 92 - (error_rate * 0.5)),
            "annual_remaining": max(0, 78 - (error_rate * 0.2))
        },
        "slo_status": {
            "availability": 0.0 if not db_healthy else 99.9,
            "latency_target": "<200ms",
            "latency_actual": f"{avg_response_time}ms" if db_healthy else "N/A"
        }
    })


@app.route('/services')
def get_services():
    """
    服務架構狀態 API 端點 - 包含真實資料庫狀態
    (Service architecture status API endpoint - includes real DB status)
    """
    current_time = time.time()
    uptime = current_time - metrics["uptime_start"]
    
    # 實際檢查資料庫連線狀態
    db_healthy = check_db_connection()
    
    error_rate = 0
    if metrics["total_requests"] > 0:
        error_rate = (metrics["error_requests"] / metrics["total_requests"]) * 100
    
    # 如果資料庫斷線，影響所有依賴它的服務
    if not db_healthy:
        base_health = 0
        db_status = "degraded"
        dependent_status = "degraded"
    else:
        base_health = 98.5 if uptime > 0 else 0
        db_status = "healthy"
        dependent_status = "healthy"
    
    health_variation = max(-10, min(5, -error_rate * 0.5))
    
    services = {
        "load_balancer": {
            "name": "Load Balancer",
            "status": "healthy" if base_health + health_variation > 95 else "warning",
            "health": round(max(0, base_health + health_variation), 1)
        },
        "api_gateway": {
            "name": "API Gateway", 
            "status": "healthy" if base_health + health_variation > 95 else "warning",
            "health": round(max(0, base_health + health_variation), 1)
        },
        "user_service": {
            "name": "User Service",
            "status": dependent_status if not db_healthy else ("healthy" if base_health + health_variation > 90 else "warning"),
            "health": round(max(0, base_health + health_variation - 5), 1)
        },
        "order_service": {
            "name": "Order Service",
            "status": dependent_status if not db_healthy else ("healthy" if base_health + health_variation > 90 else "warning"), 
            "health": round(max(0, base_health + health_variation - 5), 1)
        },
        "payment_service": {
            "name": "Payment Service",
            "status": dependent_status if not db_healthy else ("healthy" if base_health + health_variation > 85 else "degraded"),
            "health": round(max(0, base_health + health_variation - 10), 1)
        },
        "database": {
            "name": "Database",
            "status": db_status,
            "health": 98.5 if db_healthy else 0.0
        },
        "redis_cache": {
            "name": "Redis Cache",
            "status": "healthy" if base_health + health_variation > 90 else "warning",
            "health": round(max(0, base_health + health_variation - 5), 1)
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
        # 檢查資料庫連線 (Check DB connection)
        check_db_connection_or_raise()
        add_log("info", "Database connection successful for checkout")

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
        
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}{metrics['orders_created']:05d}"
        
        order_data = {
            "order_id": order_id,
            "total": cart_data["total"],
            "payment_method": payment_display,
            "delivery_method": delivery_method,
            "invoice_type": invoice_type,
            "status": "已成立"
        }
        
        # 記錄成功日誌
        add_log("success", f"Order created successfully - Order ID: {order_id}, Total: ${cart_data['total']}, Payment: {payment_display}")
        
        return jsonify({
            "status": "success",
            "message": f"訂單已成功建立！付款方式：{payment_display}",
            "order": order_data
        })
        
    except Exception as e:
        add_log("error", f"Checkout failed: {str(e)}")
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


@app.route('/dashboard/<path:filename>')
def serve_dashboard(filename):
    """
    Serve dashboard files
    """
    return send_from_directory('dashboard', filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
