/**
 * 電商結帳系統 - 前端互動邏輯
 * E-commerce Checkout System - Frontend JavaScript
 * 基於 web design etc 參考設計
 */

document.addEventListener('DOMContentLoaded', function () {

    // ==================== Tab 切換功能 ====================
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            // 移除所有 active 狀態
            tabs.forEach(t => t.classList.remove('active'));
            // 新增 active 到點擊的 tab
            this.classList.add('active');

            // 隱藏所有 tab-content
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

            // 顯示對應的 content
            const target = this.dataset.target;
            if (target === 'creditCard') {
                document.getElementById('creditCardFields').classList.add('active');
            } else if (target === 'cod') {
                document.getElementById('codDetails').classList.add('active');
            }
        });
    });

    // ==================== 表單元素取得 ====================
    const checkoutForm = document.getElementById('checkoutForm');
    const cardNumberInput = document.getElementById('cardNumber');
    const expiryDateInput = document.getElementById('expiryDate');
    const cvvInput = document.getElementById('cvv');
    const messageArea = document.getElementById('messageArea');

    // ==================== 信用卡號格式化 ====================
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            let formattedValue = value.match(/.{1,4}/g)?.join('-') || value;
            e.target.value = formattedValue;
        });
    }

    // ==================== 到期日格式化 ====================
    if (expiryDateInput) {
        expiryDateInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length >= 2) {
                value = value.substring(0, 2) + '/' + value.substring(2, 4);
            }

            e.target.value = value;
        });
    }

    // ==================== CVV 僅允許數字 ====================
    if (cvvInput) {
        cvvInput.addEventListener('input', function (e) {
            e.target.value = e.target.value.replace(/\D/g, '');
        });
    }

    // ==================== 表單提交處理 ====================
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // 清除之前的訊息
            messageArea.innerHTML = '';

            // 取得表單資料
            const formData = new FormData(checkoutForm);

            // 基本驗證
            const cardNumber = formData.get('card_number').replace(/-/g, '');
            const expiryDate = formData.get('expiry_date');
            const cvv = formData.get('cvv');

            // 驗證信用卡號 (至少 13 碼)
            if (cardNumber.length < 13) {
                showMessage('請輸入有效的信用卡號碼', 'error');
                return;
            }

            // 驗證到期日格式
            if (!/^\d{2}\/\d{2}$/.test(expiryDate)) {
                showMessage('請輸入有效的到期日 (MM/YY)', 'error');
                return;
            }

            // 驗證 CVV (3 碼)
            if (cvv.length !== 3) {
                showMessage('請輸入 3 碼 CVV 安全碼', 'error');
                return;
            }

            // 送出表單 (AJAX)
            submitCheckout(formData);
        });
    }

    /**
     * 提交結帳請求
     */
    function submitCheckout(formData) {
        const submitBtn = checkoutForm.querySelector('#checkoutButton');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = '處理中...';
        submitBtn.disabled = true;

        // 發送 POST 請求
        fetch('/checkout', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;

                if (data.status === 'success') {
                    showMessage(data.message, 'success');

                    if (data.order) {
                        const orderInfo = `
                        <div class="mt-3 p-3 bg-light rounded">
                            <strong>訂單編號:</strong> ${data.order.order_id}<br>
                            <strong>付款金額:</strong> $${data.order.total}<br>
                            <strong>訂單狀態:</strong> ${data.order.status}
                        </div>
                    `;
                        messageArea.innerHTML += orderInfo;
                    }

                    checkoutForm.reset();
                } else {
                    showMessage(data.message || '結帳失敗，請稍後再試', 'error');
                }
            })
            .catch(error => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                console.error('Error:', error);
                showMessage('系統錯誤，請稍後再試', 'error');
            });
    }

    /**
     * 顯示訊息
     */
    function showMessage(message, type) {
        const alertClass = type === 'success' ? 'alert-success' : 'alert-error';
        const alertHTML = `
            <div class="alert ${alertClass}">
                ${message}
            </div>
        `;
        messageArea.innerHTML = alertHTML;
        messageArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
