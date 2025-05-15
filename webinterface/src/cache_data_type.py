

def get_cache_key(user_id, data_type):
    """生成特定用戶和數據類型的緩存鍵"""
    return f"temp_data_{user_id}_{data_type}"