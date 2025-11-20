# Chat Agent

## 目錄結構

```
.
├── docker-compose.yml    # Docker 容器配置
├── open-webui/           # Open WebUI 資料
├── pipelines/            # Pipeline 模板
│   ├── customize.py      # 調整模型參數
│   ├── sqlparser.py      # SQL 語法生成
│   └── README.md         # Pipeline 參數說明
└── README.md
```

## 快速開始

### 啟動服務

```bash
docker compose up -d
```

- Open WebUI: http://localhost:3000
- Pipelines API Key: `0p3n-w3bu!`

### 停止服務

```bash
docker compose down
```

## Pipeline 使用

詳見 [pipelines/README.md](pipelines/README.md)
