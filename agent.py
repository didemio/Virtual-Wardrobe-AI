"""
Wardrobe Assistant Agent
Uses Claude API with tool use to help users manage and get outfit suggestions
from their personal wardrobe.
"""

import os
import json
from anthropic import Anthropic
from tools.wardrobe_tools import (
    load_wardrobe,
    add_item,
    remove_item,
    filter_by_category,
    list_categories,
    TOOL_DEFINITIONS,
)

client = Anthropic()
WARDROBE_FILE = "data/wardrobe.json"


def run_tool(tool_name: str, tool_input: dict) -> str:
    """Dispatch tool calls from the agent to the correct function."""
    wardrobe = load_wardrobe(WARDROBE_FILE)

    if tool_name == "get_all_items":
        items = wardrobe.get("clothes", [])
        return json.dumps(items, ensure_ascii=False)

    elif tool_name == "filter_by_category":
        category = tool_input.get("category", "")
        result = filter_by_category(wardrobe, category)
        return json.dumps(result, ensure_ascii=False)

    elif tool_name == "list_categories":
        result = list_categories(wardrobe)
        return json.dumps(result, ensure_ascii=False)

    elif tool_name == "add_item":
        name = tool_input.get("name")
        category = tool_input.get("category")
        updated = add_item(wardrobe, name, category)
        with open(WARDROBE_FILE, "w", encoding="utf-8") as f:
            json.dump(updated, f, ensure_ascii=False, indent=2)
        return f"'{name}' added to wardrobe under category '{category}'."

    elif tool_name == "remove_item":
        item_id = tool_input.get("id")
        updated, success = remove_item(wardrobe, item_id)
        if success:
            with open(WARDROBE_FILE, "w", encoding="utf-8") as f:
                json.dump(updated, f, ensure_ascii=False, indent=2)
            return f"Item with id {item_id} removed."
        return f"Item with id {item_id} not found."

    return "Unknown tool."


def chat(user_message: str, history: list) -> tuple[str, list]:
    """
    Send a user message to the agent and handle tool use loop.
    Returns the assistant reply and updated history.
    """
    history.append({"role": "user", "content": user_message})

    system_prompt = (
        "You are a helpful wardrobe assistant. "
        "You help the user manage their clothes and suggest outfits. "
        "You have access to tools to read and modify the user's wardrobe. "
        "Always use the tools to get accurate wardrobe data before making suggestions. "
        "Respond in the same language the user writes in."
    )

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            tools=TOOL_DEFINITIONS,
            messages=history,
        )

        text_reply = ""
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                text_reply += block.text
            elif block.type == "tool_use":
                tool_calls.append(block)

        if not tool_calls:
            history.append({"role": "assistant", "content": response.content})
            return text_reply, history

        history.append({"role": "assistant", "content": response.content})

        tool_results = []
        for tc in tool_calls:
            result = run_tool(tc.name, tc.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": result,
            })

        history.append({"role": "user", "content": tool_results})


def main():
    print("👗 Wardrobe Assistant")
    print("Type 'quit' to exit.\n")
    history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        reply, history = chat(user_input, history)
        print(f"\nAssistant: {reply}\n")


if __name__ == "__main__":
    main()
