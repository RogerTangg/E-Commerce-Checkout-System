"""
E-Commerce Checkout System - Route Tests
路由測試

測試範圍：
1. 首頁載入
2. 購物車功能
3. 結帳流程
4. 故障注入 API
"""

import pytest
import sys
import os

# 將 src 目錄加入路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app


@pytest.fixture
def client():
    """建立測試客戶端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestMainRoutes:
    """測試主要頁面路由"""
    
    def test_index_page_loads(self, client):
        """TC-01: 首頁應該正常載入"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_cart_page_loads(self, client):
        """TC-02: 購物車頁面應該正常載入"""
        response = client.get('/cart')
        assert response.status_code == 200
    
    def test_checkout_page_loads(self, client):
        """TC-03: 結帳頁面應該正常載入"""
        response = client.get('/checkout')
        assert response.status_code == 200


class TestMetricsAPI:
    """測試監控指標 API"""
    
    def test_metrics_endpoint(self, client):
        """TC-04: /metrics 端點應該返回 JSON 格式的指標"""
        response = client.get('/metrics')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data = response.get_json()
        assert 'total_requests' in data
        assert 'error_requests' in data
    
    def test_logs_endpoint(self, client):
        """TC-05: /logs 端點應該返回日誌列表"""
        response = client.get('/logs')
        assert response.status_code == 200
        assert response.content_type == 'application/json'


class TestFaultInjection:
    """測試故障注入功能"""
    
    def test_fault_status(self, client):
        """TC-06: /fault/status 應該返回故障狀態"""
        response = client.get('/fault/status')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'database_down' in data
        assert 'high_latency' in data
    
    def test_fault_inject_and_recover(self, client):
        """TC-07: 故障注入與恢復流程"""
        # 注入故障
        inject_response = client.post('/fault/inject', 
            json={'fault_type': 'database_down'},
            content_type='application/json'
        )
        assert inject_response.status_code == 200
        
        # 檢查狀態
        status_response = client.get('/fault/status')
        status_data = status_response.get_json()
        assert status_data['database_down'] == True
        
        # 恢復故障
        recover_response = client.post('/fault/recover',
            json={'fault_type': 'database_down'},
            content_type='application/json'
        )
        assert recover_response.status_code == 200
        
        # 確認恢復
        final_status = client.get('/fault/status').get_json()
        assert final_status['database_down'] == False


class TestDashboard:
    """測試 Dashboard 路由"""
    
    def test_dashboard_loads(self, client):
        """TC-08: Dashboard 應該正常載入"""
        response = client.get('/dashboard/')
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
