# Pipeline 參數說明

## customize.py

調整 local 模型參數。可調整參數位於 `Valves` 類別中:

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `VLLM_URL` | `http://192.168.1.79:3472` | vLLM 服務地址 |
| `MODEL` | `gemma-12b-8bit` | 模型名稱 |
| `MAX_TOKENS` | `1800` | 最大生成 token 數 |
| `TEMPERATURE` | `0.7` | 溫度 (0-2，數值越高越隨機) |
| `TOP_P` | `0.9` | 核心採樣閾值 |
| `FREQUENCY_PENALTY` | `0.1` | 頻率懲罰 |
| `PRESENCE_PENALTY` | `0.1` | 存在懲罰 |
| `TIMEOUT` | `120` | 請求逾時秒數 |

## sqlparser.py

使用 SQL Grammar 將自然語言轉換為 SQL 查詢。可調整參數位於 `Valves` 類別中:

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `VLLM_URL` | `http://192.168.1.79:3472` | vLLM 服務地址 |
| `MODEL` | `gemma-12b-8bit` | 模型名稱 |
| `MAX_TOKENS` | `1800` | 最大生成 token 數 |
| `TEMPERATURE` | `0.7` | 溫度 (0-2，數值越高越隨機) |
| `TOP_P` | `0.9` | 核心採樣閾值 |
| `FREQUENCY_PENALTY` | `0.1` | 頻率懲罰 |
| `PRESENCE_PENALTY` | `0.1` | 存在懲罰 |
| `TIMEOUT` | `120` | 請求逾時秒數 |
