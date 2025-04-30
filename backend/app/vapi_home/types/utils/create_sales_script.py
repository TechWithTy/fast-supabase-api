def create_assistant_messages(sales_script: str) -> list:
    script_lines = [line for line in sales_script.split('\n') if line.strip() != '']
    
    messages = [
        {
            "role": "system",
            "content": f"You're a sales agent following this script:\n{chr(10).join(script_lines)}\nFollow this script while adapting to the conversation naturally."
        }
    ]
    
    # Add script lines as assistant messages
    for index, line in enumerate(script_lines):
        messages.append({
            "role": "assistant",
            "content": line,
            "type": "request-start" if index == 0 else None
        })
    
    return messages
