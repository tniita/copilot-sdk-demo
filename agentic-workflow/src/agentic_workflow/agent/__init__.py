"""
Agent モジュール
"""

from .orchestrator import AgentConfig, AgentPresets, AgentResult, AgenticWorkflow

__all__ = [
    "AgentConfig",
    "AgentPresets",
    "AgentResult",
    "AgenticWorkflow",
]

# 利用可能なモデル定数をエクスポート
MODELS = {
    "GPT5": AgentPresets.MODEL_GPT5,
    "GPT52": AgentPresets.MODEL_GPT52,
    "CLAUDE_OPUS": AgentPresets.MODEL_CLAUDE_OPUS,
    "CLAUDE_SONNET": AgentPresets.MODEL_CLAUDE_SONNET,
}
