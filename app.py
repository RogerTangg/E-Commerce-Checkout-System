"""
電商結帳系統 - Flask 後端 (E-commerce Checkout System - Flask Backend)
Baseline V3 + COD Feature Toggle

Author: Professional Developer
Date: 2025-11-23
"""

from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Mock 購物車資料 (Mock Cart Data)
mock_cart = {
    "subtotal": 170,
    "shipping_fee": 50,
    "total": 220,
    "items": [
        {"name": "範例商品 (Sample Item)", "price": 170, "quantity": 1}
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
        # 如果檔案不存在，返回預設值（COD 關閉）
        print(f"Warning: {toggles_path} not found. Using default toggles.")
        return {"enable_cod": False}
    except json.JSONDecodeError as e:
        # 如果 JSON 格式錯誤，返回預設值
        print(f"Error parsing toggles.json: {e}. Using default toggles.")
        return {"enable_cod": False}


@app.route('/')
def index():
    """
    首頁路由 - 渲染結帳選項頁面
    (Homepage route - Render checkout options page)
    """
    return render_template('checkout.html', cart=mock_cart)


@app.route('/payment')
def payment():
    """
    付款頁面路由 - 渲染付款方式頁面
    (Payment route - Render payment method page)
    
    重要：讀取 Feature Toggle 並傳遞給前端
    """
    toggles = load_toggles()
    enable_cod = toggles.get('enable_cod', False)
    
    return render_template(
        'payment.html', 
        cart=mock_cart, 
        enable_cod=enable_cod
    )


@app.route('/checkout', methods=['POST'])
def checkout():
    """
    結帳路由 - 處理結帳請求 (含 DevSecOps 安全驗證)
    (Checkout route - Handle checkout request with security validation)
    
    安全設計：
    1. 前端根據 Toggle 顯示/隱藏 COD 選項
    2. 後端必須二次驗證 Toggle 狀態
    3. 防止惡意使用者繞過前端限制
    """
    try:
        # 載入當前的 Toggle 狀態
        toggles = load_toggles()
        enable_cod = toggles.get('enable_cod', False)
        
        # 取得表單資料
        payment_method = request.form.get('payment_method', 'credit_card')
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        delivery_method = request.form.get('delivery_method', '宅配')
        invoice_type = request.form.get('invoice_type', '手機載具')
        
        # ============================================
        # DevSecOps 安全驗證：後端 Toggle 檢查
        # ============================================
        if payment_method == 'cod' and not enable_cod:
            # COD 功能已關閉，但使用者嘗試使用 COD
            # 這可能是惡意攻擊或前端同步問題
            return jsonify({
                "status": "error",
                "message": "貨到付款功能目前不可用 (COD feature is currently disabled)",
                "error_code": "FEATURE_DISABLED"
            }), 403  # 403 Forbidden
        
        # 根據付款方式進行不同的驗證
        if payment_method == 'credit_card':
            # 信用卡付款驗證
            if not card_number or not expiry_date or not cvv:
                return jsonify({
                    "status": "error",
                    "message": "請填寫完整的信用卡資訊"
                }), 400
            
            payment_display = "信用卡"
            
        elif payment_method == 'cod':
            # 貨到付款 (已通過 Toggle 檢查)
            payment_display = "貨到付款"
            
        else:
            return jsonify({
                "status": "error",
                "message": "無效的付款方式"
            }), 400
        
        # 模擬訂單成立
        order_data = {
            "order_id": "ORD-2025112300001",
            "total": mock_cart["total"],
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
