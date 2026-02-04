#!/usr/bin/env python3
"""
Agentic Workflow メインエントリーポイント

GitHub Copilot SDK + MCP Protocol を使用したコード相互レビューエージェント
"""

import asyncio
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from .demos.code_review_agent import CodeReviewOrchestrator

load_dotenv()

console = Console()


async def run_interactive() -> None:
    """対話モードでコード相互レビューエージェントを実行"""

    console.print(
        Panel.fit(
            "[bold]╔════════════════════════════════════════════════════════════╗[/bold]\n"
            "[bold]║     🔄 コード相互レビューエージェント - Interactive Mode     ║[/bold]\n"
            "[bold]║        Claude Opus 4.5 × GPT-5.2-codex                      ║[/bold]\n"
            "[bold]╚════════════════════════════════════════════════════════════╝[/bold]",
            border_style="blue",
        )
    )

    console.print("\n[green]✅ 準備完了！生成したいコードの要望を入力してください。(exitで終了)[/green]\n")

    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]💬 コード要望[/bold cyan]")

            if user_input.strip().lower() == "exit":
                console.print("\n[yellow]👋 さようなら！[/yellow]")
                break

            if not user_input.strip():
                continue

            orchestrator = CodeReviewOrchestrator(max_review_rounds=2, verbose=True)
            result = await orchestrator.run(user_input)

            console.print("\n[bold green]✅ コード生成完了！[/bold green]")

        except KeyboardInterrupt:
            console.print("\n[yellow]👋 さようなら！[/yellow]")
            break


async def run_demo() -> None:
    """デモモードでコード相互レビューエージェントを実行"""

    console.print(
        Panel.fit(
            "[bold]╔════════════════════════════════════════════════════════════╗[/bold]\n"
            "[bold]║     🚀 コード相互レビューエージェント - Demo Mode           ║[/bold]\n"
            "[bold]╚════════════════════════════════════════════════════════════╝[/bold]",
            border_style="green",
        )
    )

    demo_request = """
Pythonで以下の機能を持つ非同期HTTPクライアントクラスを実装してください:

1. GET/POST/PUT/DELETE メソッドをサポート
2. 自動リトライ機能（最大3回、指数バックオフ）
3. タイムアウト設定
4. レスポンスのJSON自動パース
5. カスタムヘッダーのサポート
6. 適切なエラーハンドリング
"""

    console.print(f"\n[bold]📝 デモリクエスト:[/bold] {demo_request}\n")

    orchestrator = CodeReviewOrchestrator(max_review_rounds=2, verbose=True)
    result = await orchestrator.run(demo_request)

    console.print("\n[bold green]✅ コード生成完了！[/bold green]")


def main() -> None:
    """メインエントリーポイント"""
    mode = sys.argv[1] if len(sys.argv) > 1 else "interactive"

    if mode == "interactive":
        asyncio.run(run_interactive())
    elif mode == "demo":
        asyncio.run(run_demo())
    else:
        console.print(
            """
[bold]使用方法:[/bold]
  python -m agentic_workflow.main                # 対話モード
  python -m agentic_workflow.main demo           # デモモード
  python -m agentic_workflow.demos.code_review_agent # コード相互レビューデモ
"""
        )


if __name__ == "__main__":
    main()

