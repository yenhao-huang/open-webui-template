#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open WebUI Pipeline - 最小範本
"""

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel


class Pipeline:
    """Open WebUI Pipeline 最小範本"""

    class Valves(BaseModel):
        """Pipeline 配置參數"""
        EXAMPLE_PARAM: str = "default_value"

    def __init__(self):
        self.type = "manifold"
        self.valves = self.Valves()
        self.pipelines = [{"id": "template", "name": "Template Pipeline"}]

    def pipes(self) -> List[dict]:
        """返回可用的 pipeline 列表"""
        return self.pipelines

    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict
    ) -> Union[str, Generator, Iterator, dict]:
        """
        處理請求的主要方法

        Args:
            user_message: 用戶的當前訊息
            model_id: 模型 ID
            messages: 對話歷史
            body: 請求的完整內容

        Returns:
            處理結果（字串、生成器或字典）
        """
        # 在這裡實作您的邏輯
        return f"收到訊息: {user_message}"
