#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open WebUI Pipeline - SQL Parser
使用 VLLM 和 SQL Grammar 將自然語言轉換為 SQL 查詢
"""

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import requests


class Pipeline:
    """Open WebUI Pipeline for SQL Query Generation"""

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

    SQL_GRAMMAR = r"""
root ::= sql-statement
sql-statement ::= select-stmt | insert-stmt | update-stmt | delete-stmt
select-stmt ::= "SELECT" ws columns ws "FROM" ws table-name (ws where-clause)? (ws order-clause)? (ws limit-clause)? ";"?
insert-stmt ::= "INSERT" ws "INTO" ws table-name ws "(" ws columns ws ")" ws "VALUES" ws "(" ws values ws ")" ";"?
update-stmt ::= "UPDATE" ws table-name ws "SET" ws assignments (ws where-clause)? ";"?
delete-stmt ::= "DELETE" ws "FROM" ws table-name (ws where-clause)? ";"?
columns ::= "*" | column-list
column-list ::= column-name (ws? "," ws? column-name)*
column-name ::= identifier (ws "AS" ws identifier)?
table-name ::= identifier
values ::= value (ws? "," ws? value)*
value ::= number | string | "NULL"
assignments ::= assignment (ws? "," ws? assignment)*
assignment ::= identifier ws? "=" ws? value
where-clause ::= "WHERE" ws condition
condition ::= identifier ws? comparator ws? value (ws ("AND" | "OR") ws condition)?
comparator ::= "=" | "!=" | "<" | ">" | "<=" | ">=" | "LIKE" | "IN"
order-clause ::= "ORDER" ws "BY" ws identifier (ws ("ASC" | "DESC"))?
limit-clause ::= "LIMIT" ws number
number ::= [0-9]+
identifier ::= [a-zA-Z_][a-zA-Z0-9_]*
string ::= "'" [^']* "'"
ws ::= [ \t\n]+
"""

    def __init__(self):
        self.type = "manifold"
        self.valves = self.Valves()
        self.pipelines = [{"id": "sql_parser", "name": "SQL Parser"}]

    def pipes(self) -> List[dict]:
        """返回可用的 pipeline 列表"""
        return self.pipelines

    def query_with_sql_grammar(self, prompt: str) -> str:
        """使用 SQL Grammar 限制輸出為 SQL 語法"""
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
            "guided_grammar": self.SQL_GRAMMAR
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
        處理請求的主要方法 - 將自然語言轉換為 SQL 查詢

        Args:
            user_message: 用戶的當前訊息（自然語言查詢）
            model_id: 模型 ID
            messages: 對話歷史
            body: 請求的完整內容

        Returns:
            生成的 SQL 查詢語句
        """
        try:
            # 使用 SQL Grammar 生成 SQL 查詢
            sql_query = self.query_with_sql_grammar(user_message)

            return f"""### SQL 查詢生成成功 ✅

**原始問題：**
{user_message}

**生成的 SQL：**
```sql
{sql_query}
```

---
*由 {self.valves.MODEL} 生成*"""

        except Exception as e:
            return f"### 錯誤 ❌\n\n生成 SQL 查詢時發生錯誤：{str(e)}"
