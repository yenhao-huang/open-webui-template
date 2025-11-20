#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open WebUI Pipeline: 調整 local 模型的參數 (temperature、max_token)
"""

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import requests


class Pipeline:

    class Valves(BaseModel):
        """Pipeline 配置參數"""
        VLLM_URL: str = "http://192.168.1.79:3472"
        MODEL: str = "gemma-12b-8bit"
        MAX_TOKENS: int = 1800
        TEMPERATURE: float = 0.7
        TOP_P: float = 0.9
        FREQUENCY_PENALTY: float = 0.1
        PRESENCE_PENALTY: float = 0.1
        TIMEOUT: int = 120

    def __init__(self):
        # 調整
        self.model_name = "Customized Agent"

        self.type = "manifold"
        self.valves = self.Valves()
        self.pipelines = [{"id": "template", "name": self.model_name}]

    def pipes(self) -> List[dict]:
        """返回可用的 pipeline 列表"""
        return self.pipelines

    def call_vllm(self, prompt) -> str:
        """設定 vLLM"""
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "model": self.valves.MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": self.valves.MAX_TOKENS,
            "temperature": self.valves.TEMPERATURE,
            "top_p": self.valves.TOP_P,
            "frequency_penalty": self.valves.FREQUENCY_PENALTY,
            "presence_penalty": self.valves.PRESENCE_PENALTY,
        }

        response = requests.Session().post(
            f"{self.valves.VLLM_URL}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=self.valves.TIMEOUT
        )

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")


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
        response = self.call_vllm(user_message)

        return response
