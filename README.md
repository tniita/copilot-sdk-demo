# コード相互レビューエージェント

**GitHub Copilot SDK** と **MCP Protocol** を使用した、Claude Opus 4.5 × GPT-5.2-codex によるコード相互レビューエージェントです。

## 📋 概要

2つの最先端LLMモデル（Claude Opus 4.5 と GPT-5.2-codex）が相互にコードをレビューし、最高品質のコードを生成します。

### ワークフロー

```
┌─────────────────────────────────────────────────────────────┐
│              コード相互レビューワークフロー                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: 初期コード生成（並列実行）                          │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │  Claude Opus 4.5 │    │  GPT-5.2-codex   │               │
│  │   コード生成      │    │   コード生成      │               │
│  └────────┬─────────┘    └────────┬─────────┘               │
│           │                       │                          │
│  Phase 2: 相互レビュー（並列実行）                            │
│           │                       │                          │
│           ▼                       ▼                          │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │  Claude が GPT   │    │   GPT が Claude  │               │
│  │  のコードをレビュー│    │  のコードをレビュー│               │
│  └────────┬─────────┘    └────────┬─────────┘               │
│           │                       │                          │
│  Phase 3: 統合                    │                          │
│           └───────────┬───────────┘                          │
│                       ▼                                      │
│              ┌──────────────────┐                            │
│              │    最終マージ     │                            │
│              │  両者の良い点を   │                            │
│              │    統合して出力   │                            │
│              └──────────────────┘                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📁 プロジェクト構造

```
agentic-workflow/
├── src/
│   └── agentic_workflow/
│       ├── agent/                     # エージェントオーケストレーター
│       │   └── orchestrator.py        # GitHub Copilot SDK ワークフローエンジン
│       ├── mcp_servers/               # MCPサーバー
│       │   └── code_review_server.py  # コード相互レビューMCPサーバー
│       ├── demos/                     # デモスクリプト
│       │   └── code_review_agent.py   # コード相互レビューエージェント
│       └── main.py                    # メインエントリーポイント
├── pyproject.toml
└── README.md
```

## 🚀 セットアップ

### 前提条件

- Python 3.11以上
- GitHub Copilot CLI がインストール・認証済み
- GitHub Copilot のサブスクリプション

### インストール

```bash
cd agentic-workflow

# 仮想環境を作成
python -m venv .venv
source .venv/bin/activate

# 依存関係をインストール
pip install -e ".[dev]"
```

## 🎯 実行方法

### 対話モード

```bash
python -m agentic_workflow.main
```

### デモモード

```bash
python -m agentic_workflow.main demo
```

### 直接実行

```bash
python -m agentic_workflow.demos.code_review_agent
```

## 💻 プログラムからの使用

```python
from agentic_workflow.demos.code_review_agent import CodeReviewOrchestrator

# オーケストレーターを初期化
orchestrator = CodeReviewOrchestrator(max_review_rounds=2, verbose=True)

# コード生成リクエスト
request = """
Pythonで非同期HTTPクライアントクラスを実装してください:
- GET/POST/PUT/DELETE メソッドをサポート
- 自動リトライ機能
- タイムアウト設定
"""

# 実行
result = await orchestrator.run(request)
print(result.code)  # 最終的な高品質コード
```

## 🔧 MCPサーバーとして使用

他のエージェントからMCPツールとして呼び出し可能です。

**提供ツール:**
- `generate_reviewed_code` - 相互レビューによる高品質コード生成
- `compare_model_outputs` - 両モデルの出力比較
- `get_review_feedback` - 既存コードへのデュアルレビュー

```python
from agentic_workflow.agent import AgentConfig

config = AgentConfig(
    name="Enhanced Agent",
    prompt="...",
    mcp_servers={
        "code_review": {
            "type": "local",
            "command": "python",
            "args": ["./mcp_servers/code_review_server.py"],
            "tools": ["generate_reviewed_code"],
        }
    },
)
```

## 🔗 参考リンク

- [GitHub Copilot SDK](https://github.com/github/copilot-sdk)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

## 📄 ライセンス

MIT
