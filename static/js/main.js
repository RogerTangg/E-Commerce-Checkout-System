/**
 * 電商結帳系統 - 前端互動邏輯
 * E-commerce Checkout System - Frontend JavaScript
 * 支援 COD Feature Toggle
 */

document.addEventListener('DOMContentLoaded', function () {

    // ==================== Tab 切換功能 ====================
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

            const target = this.dataset.target;
            if (target === 'creditCard') {
                document.getElementById('creditCardFields').classList.add('active');
            } else if (target === 'cod') {
                const codDetails = document.getElementById('codDetails');
                if (codDetails) {
                    codDetails.classList.add('active');
                }
            }
        });
    });

    // ==================== 表單元素 ====================
    const cardNumberInput = document.getElementById('cardNumber');
    const expiryDateInput = document.getElementById('expiryDate');
    const cvvInput = document.getElementById('cvv');
    const messageArea = document.getElementById('messageArea');
    const checkoutButton = document.getElementById('checkoutButton');

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

    // ==================== 表單提交處理 (支援雙表單) ====================
    if (checkoutButton) {
        checkoutButton.addEventListener('click', function (e) {
            e.preventDefault();

            if (messageArea) {
                messageArea.innerHTML = '';
            }

            // 確定當前哪個 tab 是 active 的
            const activeTab = document.querySelector('.tab.active');
            const activeTarget = activeTab ? activeTab.dataset.target : 'creditCard';

            // 根據 active tab 選擇正確的表單
            let currentForm;
            if (activeTarget === 'cod') {
                currentForm = document.getElementById('codForm');
            } else {
                currentForm = document.getElementById('checkoutForm');
            }

            if (!currentForm) {
                showMessage('系統錯誤：無法找到表單', 'error');
                return;
            }

            // 取得表單資料
            const formData = new FormData(currentForm);

            // 針對信用卡付款進行額外驗證
            if (activeTarget === 'creditCard') {
                const cardNumber = formData.get('card_number').replace(/-/g, '');
                const expiryDate = formData.get('expiry_date');
                const cvv = formData.get('cvv');

                if (cardNumber.length < 13) {
                    showMessage('請輸入有效的信用卡號碼', 'error');
                    return;
                }

                if (!/^\d{2}\/\d{2}$/.test(expiryDate)) {
                    showMessage('請輸入有效的到期日 (MM/YY)', 'error');
                    return;
                }

                if (cvv.length !== 3) {
                    showMessage('請輸入 3 碼 CVV 安全碼', 'error');
                    return;
                }
            }

            // 送出表單 (AJAX)
            submitCheckout(formData);
        });
    }

    /**
     * 提交結帳請求
     */
    function submitCheckout(formData) {
        const originalText = checkoutButton.textContent;
        checkoutButton.textContent = '處理中...';
        checkoutButton.disabled = true;

        fetch('/checkout', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                checkoutButton.textContent = originalText;
                checkoutButton.disabled = false;

                if (data.status === 'success') {
                    // 結帳成功，導向至成功頁面
                    const params = new URLSearchParams({
                        order_id: data.order.order_id,
                        total: data.order.total,
                        payment_method: data.order.payment_method,
                        delivery_method: data.order.delivery_method
                    });
                    window.location.href = `/success?${params.toString()}`;
                } else {
                    showMessage(data.message || '結帳失敗，請稍後再試', 'error');
                }
            })
            .catch(error => {
                checkoutButton.textContent = originalText;
                checkoutButton.disabled = false;
                console.error('Error:', error);
                showMessage('系統錯誤，請稍後再試', 'error');
            });
    }

    /**
     * 顯示訊息
     */
    function showMessage(message, type) {
        if (!messageArea) return;

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
