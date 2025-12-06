"""
E-Commerce Checkout System - Feature Flags Tests
Feature Flag 功能測試

測試範圍：
1. Toggle 檔案載入
2. COD (貨到付款) 功能開關
3. Free Shipping Nudge 功能開關
"""

import pytest
import sys
import os
import json

# 將 src 目錄加入路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app, load_toggles


@pytest.fixture
def client():
    """建立測試客戶端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestFeatureToggles:
    """測試 Feature Toggle 功能"""
    
    def test_load_toggles_returns_dict(self):
        """TC-FF-01: load_toggles 應該返回字典"""
        toggles = load_toggles()
        assert isinstance(toggles, dict)
    
    def test_toggles_has_expected_keys(self):
        """TC-FF-02: toggles 應該包含預期的 key"""
        toggles = load_toggles()
        # 根據專案可能有的 toggle 名稱
        expected_keys = ['enable_cod', 'enable_free_shipping_nudge']
        for key in expected_keys:
            assert key in toggles, f"Missing expected toggle key: {key}"
    
    def test_toggles_file_exists(self):
        """TC-FF-03: config/toggles.json 檔案應該存在"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        toggles_path = os.path.join(base_dir, 'config', 'toggles.json')
        assert os.path.exists(toggles_path), f"Toggles file not found at {toggles_path}"
    
    def test_toggles_file_valid_json(self):
        """TC-FF-04: toggles.json 應該是有效的 JSON"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        toggles_path = os.path.join(base_dir, 'config', 'toggles.json')
        
        with open(toggles_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"toggles.json is not valid JSON: {e}")


class TestFeatureToggleAPI:
    """測試 Feature Toggle API 端點"""
    
    def test_toggles_endpoint(self, client):
        """TC-FF-05: /toggles 端點應該返回 toggle 設定"""
        response = client.get('/toggles')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data = response.get_json()
        assert 'enable_cod' in data
        assert 'enable_free_shipping_nudge' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
