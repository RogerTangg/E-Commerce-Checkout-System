"""
電商結帳系統 - Flask 後端 (E-commerce Checkout System - Flask Backend)
Baseline V3: 簡化版結帳頁面，僅支援信用卡付款

Author: Professional Developer
Date: 2025-11-22
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mock 購物車資料 (Mock Cart Data)
# 商品總額: $170, 運費: $50 (固定), 總計: $220
mock_cart = {
    "subtotal": 170,
    "shipping_fee": 50,  # 固定運費，無免運邏輯
    "total": 220,        # 170 + 50
    "items": [           # 商品清單（目前僅用於後續擴充）
        {"name": "範例商品 (Sample Item)", "price": 170, "quantity": 1}
    ]
}


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
    """
    return render_template('payment.html', cart=mock_cart)


@app.route('/checkout', methods=['POST'])
def checkout():
    """
    結帳路由 - 處理結帳請求
    (Checkout route - Handle checkout request)
    """
    try:
        # 取得表單資料 (Get form data)
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        delivery_method = request.form.get('delivery_method', '宅配')
        invoice_type = request.form.get('invoice_type', '手機載具')
        
        # 基本驗證 (Basic validation)
        if not card_number or not expiry_date or not cvv:
            return jsonify({
                "status": "error",
                "message": "請填寫完整的信用卡資訊"
            }), 400
        
        # 模擬訂單成立 (Simulate order creation)
        order_data = {
            "order_id": "ORD-2025112200001",
            "total": mock_cart["total"],
            "payment_method": "信用卡",
            "delivery_method": delivery_method,
            "invoice_type": invoice_type,
            "status": "已成立"
        }
        
        return jsonify({
            "status": "success",
            "message": "訂單已成功建立！",
            "order": order_data
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"系統錯誤: {str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
