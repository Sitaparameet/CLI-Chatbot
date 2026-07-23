from langchain_core.messages import ToolMessage


def run_tools(
    tool_calls,
    conversation_history,
    tool_map
):

    for tool_call in tool_calls:

        tool_name = tool_call["name"]

        tool_args = tool_call["args"]

        selected_tool = tool_map.get(
            tool_name
        )


        if selected_tool is None:

            tool_result = (
                f"Unknown tool: {tool_name}"
            )

        else:

            tool_result = selected_tool.invoke(
                tool_args
            )


        conversation_history.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )