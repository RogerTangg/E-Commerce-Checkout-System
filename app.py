"""
電商結帳系統 - Flask 後端 (E-commerce Checkout System - Flask Backend)
Baseline V3 + COD Feature Toggle + Free Shipping Nudge

Author: Professional Developer
Date: 2025-11-23
"""

from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Mock 購物車資料 (Mock Cart Data)
# 為了測試湊單功能，預設金額設為 170 (未滿 200)
mock_cart = {
    "items": [
        {"name": "精選咖啡豆 (Premium Coffee Beans)", "price": 120, "quantity": 1},
        {"name": "濾掛式咖啡包 (Drip Coffee Bag)", "price": 60, "quantity": 1}
    ]
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
def checkout_options():
    """
    結帳選項頁面路由
    (Checkout Options route)
    """
    # 重新計算金額
    cart_data = calculate_cart_totals(mock_cart['items'])
    return render_template('checkout.html', cart=cart_data)


@app.route('/')
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


@app.route('/checkout', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
