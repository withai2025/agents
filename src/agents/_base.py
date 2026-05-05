from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Iterator

import anthropic
from dotenv import load_dotenv

load_dotenv()

LANG = os.environ.get("APPFORGE_LANG", "en")  # "en" = English (default), "zh" = Chinese


@dataclass
class AgentConfig:
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 1.0
    top_k: int | None = None
    model: str = "claude-opus-4-6"


class BaseAgent:
    name: str = "base"
    description: str = ""
    system_prompt: str = ""
    config: AgentConfig = AgentConfig()

    def __init__(self, api_key: str | None = None) -> None:
        self._client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY")
        )

    def _resolve_system_prompt(self) -> str:
        """Return the system prompt in the current language.

        Defaults to English. Set APPFORGE_LANG=zh to use the Chinese version
        if the agent provides SYSTEM_PROMPT_CN.
        """
        if LANG == "zh":
            module = sys.modules.get(self.__class__.__module__)
            cn = getattr(module, "SYSTEM_PROMPT_CN", None)
            if cn:
                return cn
        return self.system_prompt

    def _build_messages(self, user_input: str) -> list[anthropic.types.MessageParam]:
        return [
            {
                "role": "user",
                "content": user_input,
            }
        ]

    def run(self, user_input: str, **kwargs) -> str:
        cfg = self._merge_config(kwargs)
        resp = self._client.messages.create(
            model=cfg["model"],
            max_tokens=cfg["max_tokens"],
            temperature=cfg["temperature"],
            top_p=cfg.get("top_p", 1.0),
            top_k=cfg.get("top_k"),
            system=self._resolve_system_prompt(),
            messages=self._build_messages(user_input),
        )
        return resp.content[0].text

    def run_stream(self, user_input: str, **kwargs) -> Iterator[str]:
        cfg = self._merge_config(kwargs)
        with self._client.messages.stream(
            model=cfg["model"],
            max_tokens=cfg["max_tokens"],
            temperature=cfg["temperature"],
            top_p=cfg.get("top_p", 1.0),
            top_k=cfg.get("top_k"),
            system=self._resolve_system_prompt(),
            messages=self._build_messages(user_input),
        ) as stream:
            for text in stream.text_stream:
                yield text

    def _merge_config(self, overrides: dict) -> dict:
        base = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "top_k": self.config.top_k,
        }
        base.update({k: v for k, v in overrides.items() if k in base})
        return base

    def __repr__(self) -> str:
        return f"<Agent name={self.name}>"
