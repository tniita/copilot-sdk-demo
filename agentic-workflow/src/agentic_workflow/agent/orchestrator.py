"""
GitHub Copilot SDK を使用した Agentic Workflow オーケストレーター

MCPサーバーと連携して自律的にタスクを実行するエージェント
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from copilot import (
    CopilotClient,
    CopilotSession,
    CustomAgentConfig,
    MCPServerConfig,
    SessionEvent,
)
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


@dataclass
class AgentConfig:
    """エージェントの設定"""

    name: str
    description: str
    prompt: str
    model: str = "gpt-5"  # 使用するLLMモデル (例: "gpt-5", "gpt-5.2", "claude-opus-4.5")
    mcp_servers: dict[str, MCPServerConfig] = field(default_factory=dict)
    tools: list[str] | None = None
    infer: bool = True


@dataclass
class AgentResult:
    """エージェントの実行結果"""

    success: bool
    response: str
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    events: list[SessionEvent] = field(default_factory=list)


class AgenticWorkflow:
    """
    GitHub Copilot SDK を使用した Agentic Workflow

    MCPサーバーと連携してツールを自動的に選択・実行する自律型エージェント
    """

    def __init__(
        self,
        config: AgentConfig,
        verbose: bool = True,
    ):
        self.config = config
        self.verbose = verbose
        self.client: CopilotClient | None = None
        self.session: CopilotSession | None = None
        self._events: list[SessionEvent] = []
        self._tool_calls: list[dict[str, Any]] = []

    async def start(self) -> None:
        """クライアントを起動してセッションを作成"""
        self.log("🚀 GitHub Copilot クライアントを起動中...", style="bold blue")

        self.client = CopilotClient()
        await self.client.start()

        self.log("✅ クライアント起動完了", style="green")

        # カスタムエージェント設定を作成
        custom_agent: CustomAgentConfig = {
            "name": self.config.name.lower().replace(" ", "-"),
            "display_name": self.config.name,
            "description": self.config.description,
            "prompt": self.config.prompt,
            "infer": self.config.infer,
        }

        if self.config.tools:
            custom_agent["tools"] = self.config.tools

        if self.config.mcp_servers:
            custom_agent["mcp_servers"] = self.config.mcp_servers

        # MCPサーバー付きのセッションを作成
        session_config: dict[str, Any] = {
            "model": self.config.model,  # LLMモデルを指定
            "custom_agents": [custom_agent],
        }

        # グローバルMCPサーバーも設定可能
        if self.config.mcp_servers:
            session_config["mcp_servers"] = self.config.mcp_servers

        self.log(f"🧠 使用モデル: {self.config.model}", style="bold cyan")

        self.log(f"📡 MCPサーバー接続中: {list(self.config.mcp_servers.keys())}", style="cyan")

        self.session = await self.client.create_session(session_config)

        self.log(f"✅ セッション作成完了: {self.session.session_id}", style="green")

        # イベントハンドラを設定
        self.session.on(self._handle_event)

    def _handle_event(self, event: SessionEvent) -> None:
        """セッションイベントを処理"""
        self._events.append(event)

        event_type = event.type.value if hasattr(event.type, "value") else str(event.type)

        if self.verbose:
            if event_type == "assistant.message":
                content = getattr(event.data, "content", None)
                if content:
                    self.log(f"🤖 応答: {content[:200]}...", style="magenta")

            elif event_type == "tool.invocation":
                tool_name = getattr(event.data, "name", "unknown")
                self.log(f"🔧 ツール呼び出し: {tool_name}", style="yellow")
                self._tool_calls.append({
                    "tool": tool_name,
                    "args": getattr(event.data, "arguments", {}),
                })

            elif event_type == "tool.result":
                self.log("   ✅ ツール実行完了", style="green")

            elif event_type == "session.idle":
                self.log("💤 セッションがアイドル状態になりました", style="dim")

    async def run(self, prompt: str) -> AgentResult:
        """
        ユーザーのプロンプトを処理して結果を返す

        Args:
            prompt: ユーザーからのリクエスト

        Returns:
            エージェントの実行結果
        """
        if not self.session:
            raise RuntimeError("セッションが開始されていません。start()を先に呼び出してください。")

        self._events.clear()
        self._tool_calls.clear()

        self.log(f"\n{'='*60}", style="dim")
        self.log(f"📝 リクエスト: {prompt}", style="bold")
        self.log(f"{'='*60}", style="dim")

        # アイドル待機用のイベント
        idle_event = asyncio.Event()
        final_content = ""

        def on_idle_or_message(event: SessionEvent) -> None:
            nonlocal final_content
            event_type = event.type.value if hasattr(event.type, "value") else str(event.type)

            if event_type == "assistant.message":
                content = getattr(event.data, "content", None)
                if content:
                    final_content = content

            if event_type == "session.idle":
                idle_event.set()

        # 一時的なハンドラを追加
        self.session.on(on_idle_or_message)

        try:
            # メッセージを送信
            await self.session.send({"prompt": prompt})

            # アイドル状態になるまで待機（タイムアウト付き）
            try:
                await asyncio.wait_for(idle_event.wait(), timeout=120.0)
            except asyncio.TimeoutError:
                self.log("⚠️ タイムアウト: 応答待機が時間切れになりました", style="red")
                return AgentResult(
                    success=False,
                    response="タイムアウト: 応答が時間内に完了しませんでした",
                    tool_calls=self._tool_calls.copy(),
                    events=self._events.copy(),
                )

            self.log(f"\n{'─'*60}", style="dim")
            self.log("✨ 処理完了", style="bold green")

            return AgentResult(
                success=True,
                response=final_content,
                tool_calls=self._tool_calls.copy(),
                events=self._events.copy(),
            )

        except Exception as e:
            self.log(f"❌ エラー: {e}", style="red")
            return AgentResult(
                success=False,
                response=str(e),
                tool_calls=self._tool_calls.copy(),
                events=self._events.copy(),
            )

    async def stop(self) -> None:
        """セッションとクライアントを終了"""
        if self.session:
            await self.session.destroy()
            self.session = None

        if self.client:
            await self.client.stop()
            self.client = None

        self.log("👋 エージェントを終了しました", style="green")

    async def __aenter__(self) -> "AgenticWorkflow":
        await self.start()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.stop()

    def log(self, message: str, style: str = "") -> None:
        """ログ出力"""
        if self.verbose:
            console.print(message, style=style)


class AgentPresets:
    """プリセットエージェント設定"""

    # 利用可能なモデル定数
    MODEL_GPT5 = "gpt-5"
    MODEL_GPT52 = "gpt-5.2"
    MODEL_CLAUDE_OPUS = "claude-opus-4.5"
    MODEL_CLAUDE_SONNET = "claude-sonnet-4"

    @staticmethod
    def weather_agent(
        mcp_server_command: str = "python",
        model: str = "claude-opus-4.5",  # デフォルトでClaude Opus 4.5を使用
    ) -> AgentConfig:
        """天気情報エージェント（デフォルト: Claude Opus 4.5）"""
        return AgentConfig(
            name="Weather Agent",
            description="天気情報を取得・分析するAIエージェント",
            model=model,
            prompt="""あなたは天気情報を提供するAIアシスタントです。
ユーザーの質問に対して、利用可能なMCPツールを使って天気情報を取得し、
分かりやすく回答してください。

利用可能なツール:
- get_weather: 特定の都市の現在の天気を取得
- get_forecast: 天気予報を取得
- compare_weather: 複数都市の天気を比較

回答は日本語で、簡潔かつ親しみやすいトーンでお願いします。""",
            mcp_servers={
                "weather": {
                    "type": "local",
                    "command": mcp_server_command,
                    "args": ["mcp_servers/weather_server.py"],
                    "tools": ["*"],
                }
            },
        )

    @staticmethod
    def task_agent(
        mcp_server_command: str = "python",
        model: str = "gpt-5.2",  # デフォルトでGPT-5.2を使用
    ) -> AgentConfig:
        """タスク管理エージェント（デフォルト: GPT-5.2）"""
        return AgentConfig(
            name="Task Manager Agent",
            description="タスク管理を支援するAIエージェント",
            model=model,
            prompt="""あなたはタスク管理を支援するAIアシスタントです。
ユーザーのタスク管理に関するリクエストに対応してください。

利用可能なツール:
- list_tasks: タスク一覧を取得
- create_task: 新しいタスクを作成
- update_task: タスクを更新
- get_task_summary: タスクの統計情報を取得
- search_tasks: タスクを検索

タスクの状態を適切に管理し、生産性向上に貢献してください。
回答は日本語で、簡潔にお願いします。""",
            mcp_servers={
                "tasks": {
                    "type": "local",
                    "command": mcp_server_command,
                    "args": ["mcp_servers/task_server.py"],
                    "tools": ["*"],
                }
            },
        )

    @staticmethod
    def multi_tool_agent(
        mcp_server_command: str = "python",
        model: str = "gpt-5",  # デフォルトでGPT-5を使用
    ) -> AgentConfig:
        """マルチツールエージェント（デフォルト: GPT-5）"""
        return AgentConfig(
            name="Multi-Tool Agent",
            description="複数のツールを駆使して問題を解決するAIエージェント",
            model=model,
            prompt="""あなたは複数のツールを駆使して問題を解決するAIアシスタントです。

利用可能なツールセット:
1. 天気情報ツール
   - get_weather: 都市の現在の天気
   - get_forecast: 天気予報
   - compare_weather: 都市間の天気比較

2. タスク管理ツール
   - list_tasks: タスク一覧
   - create_task: タスク作成
   - update_task: タスク更新
   - get_task_summary: 統計情報
   - search_tasks: タスク検索

ユーザーのリクエストに対して、必要なツールを適切に選択し、
複数のツールを組み合わせて包括的な回答を提供してください。

回答は日本語で、構造化された分かりやすい形式でお願いします。""",
            mcp_servers={
                "weather": {
                    "type": "local",
                    "command": mcp_server_command,
                    "args": ["mcp_servers/weather_server.py"],
                    "tools": ["*"],
                },
                "tasks": {
                    "type": "local",
                    "command": mcp_server_command,
                    "args": ["mcp_servers/task_server.py"],
                    "tools": ["*"],
                },
            },
        )
