#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/5 22:59
@Author  : alexanderwu
@File    : __init__.py
"""

from metagpt.provider.ollama_api import OllamaLLM
from metagpt.provider.openai_api import OpenAILLM
try:
    from metagpt.provider.google_gemini_api import GeminiLLM
except ImportError:
    pass
try:
    from metagpt.provider.zhipuai_api import ZhiPuAILLM
except ImportError:
    pass
from metagpt.provider.azure_openai_api import AzureOpenAILLM
from metagpt.provider.metagpt_api import MetaGPTLLM
from metagpt.provider.human_provider import HumanProvider
try:
    from metagpt.provider.spark_api import SparkLLM
except ImportError:
    pass
try:
    from metagpt.provider.qianfan_api import QianFanLLM
except ImportError:
    pass
try:
    from metagpt.provider.dashscope_api import DashScopeLLM
except ImportError:
    pass
from metagpt.provider.anthropic_api import AnthropicLLM
from metagpt.provider.bedrock_api import BedrockLLM
try:
    from metagpt.provider.ark_api import ArkLLM
except ImportError:
    pass
from metagpt.provider.openrouter_reasoning import OpenrouterReasoningLLM
from metagpt.provider.squirrel_api import SquirrelLLM

__all__ = [
    "GeminiLLM",
    "OpenAILLM",
    "ZhiPuAILLM",
    "AzureOpenAILLM",
    "MetaGPTLLM",
    "OllamaLLM",
    "HumanProvider",
    "SparkLLM",
    "QianFanLLM",
    "DashScopeLLM",
    "AnthropicLLM",
    "BedrockLLM",
    "ArkLLM",
    "OpenrouterReasoningLLM",
    "SquirrelLLM",
]
