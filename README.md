# Copilot SDK Demo

**GitHub Copilot SDK** を使用した Agentic Workflow デモプロジェクトです。

## 🏗️ 全体構成

このリポジトリは以下の2つの主要コンポーネントで構成されています：

```
copilot-sdk-demo/
├── agentic-workflow/          # 🤖 Agentic Workflow フレームワーク
│   ├── src/
│   │   └── agentic_workflow/
│   │       ├── agent/         # GitHub Copilot SDK オーケストレーター
│   │       ├── demos/         # コード相互レビューエージェント デモ
│   │       └── main.py        # メインエントリーポイント
│   ├── docs/                  # ドキュメント
│   └── pyproject.toml         # Python プロジェクト設定
│
├── slidev/                    # 📊 プレゼンテーション資料
│   ├── slides.md              # メインスライド
│   ├── github-copilot/        # GitHub Copilot テーマ/コンポーネント
│   ├── public/                # 静的アセット
│   └── styles/                # スタイルシート
│
└── README.md                  # このファイル
```

### コンポーネント詳細

| コンポーネント | 説明 | 技術スタック |
|--------------|------|-------------|
| **agentic-workflow** | GitHub Copilot SDK を使用したマルチエージェントワークフロー | Python, GitHub Copilot SDK, MCP Protocol |
| **slidev** | GitHub Copilot SDK のプレゼンテーション資料 | Slidev, Vue.js |

### アーキテクチャ図

```
┌─────────────────────────────────────────────────────────────────────┐
│                      GitHub Copilot Platform                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    GitHub Copilot SDK                        │   │
│  │  ┌─────────────────┐      ┌─────────────────┐               │   │
│  │  │   GPT-5.2       │      │  Claude Opus 4.5 │               │   │
│  │  │   (コードレビュー)│◄────►│  (コード生成)    │               │   │
│  │  └─────────────────┘      └─────────────────┘               │   │
│  │           ▲                        ▲                         │   │
│  │           │                        │                         │   │
│  │           ▼                        ▼                         │   │
│  │  ┌───────────────────────────────────────────┐              │   │
│  │  │           AgenticWorkflow                  │              │   │
│  │  │     (オーケストレーター / セッション管理)    │              │   │
│  │  └───────────────────────────────────────────┘              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    MCP Protocol                              │   │
│  │         (ツール呼び出し / ファイルシステムアクセス)            │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    CodeReviewOrchestrator                           │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ 1. 初期コード生成 → 2. 相互レビュー → 3. 改善 → 4. マージ      │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## 📋 概要

GitHub Copilot SDK と MCP Protocol を活用して、LLM を使った自律型エージェントワークフローを構築するためのライブラリです。

## 📁 プロジェクト構造

```
agentic-workflow/
├── src/
│   └── agentic_workflow/
│       ├── agent/                  # エージェントオーケストレーター
│       │   └── orchestrator.py     # GitHub Copilot SDK ワークフローエンジン
│       ├── demos/                  # デモスクリプト
│       │   └── code_review_agent.py
│       ├── async_http_client.py    # 非同期HTTPクライアント
│       ├── http_client.py          # 同期HTTPクライアント
│       └── main.py                 # メインエントリーポイント
├── docs/                           # ドキュメント
├── examples/                       # サンプルコード
└── pyproject.toml
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

### デモ実行

```bash
python -m agentic_workflow.demos.code_review_agent
```

### 対話モード

```bash
python -m agentic_workflow.main
```

## 💻 プログラムからの使用

### AgenticWorkflow の基本的な使い方

```python
import asyncio
from agentic_workflow.agent import AgentConfig, AgenticWorkflow

async def main():
    # エージェント設定
    config = AgentConfig(
        name="My Agent",
        description="タスクを自動実行するエージェント",
        prompt="あなたは優秀なアシスタントです。",
        model="gpt-5",  # または "claude-opus-4.5"
    )

    # ワークフロー作成・実行
    workflow = AgenticWorkflow(config)
    await workflow.start()

    result = await workflow.run("ファイル一覧を取得してください")
    print(result.response)

    await workflow.stop()

asyncio.run(main())
```

### 利用可能なモデル

```python
from agentic_workflow.agent import AgentPresets

# モデル定数
AgentPresets.MODEL_GPT5          # "gpt-5"
AgentPresets.MODEL_GPT52         # "gpt-5.2-codex"
AgentPresets.MODEL_CLAUDE_OPUS   # "claude-opus-4.5"
AgentPresets.MODEL_CLAUDE_SONNET # "claude-sonnet-4"
```

## 🔗 参考リンク

- [GitHub Copilot SDK](https://github.com/github/copilot-sdk)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

## 📄 ライセンス

MIT
