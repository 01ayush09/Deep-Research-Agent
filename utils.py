from datetime import datetime
from typing import List

from langchain_core.messages import BaseMessage, filter_messages


def get_today_str() -> str:
    now = datetime.now()
    return f"{now.strftime('%a %b')} {now.day}, {now.strftime('%Y')}"


def get_message_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if text:
                    parts.append(text)
        return "".join(parts)
    return str(content)


def get_notes_from_tool_calls(messages: List[BaseMessage]) -> List[str]:
    return [tool_msg.content for tool_msg in filter_messages(messages, include_types="tool")]
