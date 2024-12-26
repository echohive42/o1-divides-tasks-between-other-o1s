import os
from openai import AsyncOpenAI
from termcolor import colored
import json
import asyncio

# Constants
MAIN_AGENT_MODEL = "o1-mini"  # Model for task division and final synthesis
SUB_AGENT_MODEL = "o1-mini"   # Model for subtask execution

TASK = """
will coding in pure html/css/js or coding in frameworks like react/vue/angular be more prominant in the future, in the age of AI assisted coding?
"""

SYSTEM_PROMPT = """You are a specialized AI agent. Your role is to focus on the following specific aspect of the task:

{specific_role}

Provide a detailed analysis focusing ONLY on your assigned aspect. Format your response using XML tags like this:
<key_findings>list your main points here</key_findings>
<supporting_evidence>list your relevant data or examples here</supporting_evidence>
<recommendations>list your forward-looking suggestions here</recommendations>

Keep your response focused and analytical."""

TASK_MANAGER_PROMPT = """You are the task manager. Given this task:
'{task}'

Divide this task into exactly 3 distinct sub-tasks. Each sub-task should:
- Be clearly defined and focused
- Cover a different aspect of the main task
- Be designed to gather complementary information

Format your response using XML tags like this:
<task1>description of first subtask</task1>
<task2>description of second subtask</task2>
<task3>description of third subtask</task3>
<reasoning>explanation of why you divided the task this way</reasoning>"""

client = AsyncOpenAI()

async def make_api_call(messages, model, purpose=""):
    """
    Generalized function for making API calls to OpenAI with XML parsing
    """
    try:
        print(colored(f"🔄 {purpose}...", "cyan"))
        response = await client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        content = response.choices[0].message.content
        try:
            # Simple XML parsing
            result = {}
            # Define possible tags based on the purpose
            if "Dividing main task" in purpose:
                tags = ['task1', 'task2', 'task3', 'reasoning']
            elif "Executing subtask" in purpose:
                tags = ['key_findings', 'supporting_evidence', 'recommendations']
            else:  # Synthesis
                tags = ['executive_summary', 'detailed_analysis', 'future_implications', 'recommendations']
            
            for tag in tags:
                start_tag = f'<{tag}>'
                end_tag = f'</{tag}>'
                if start_tag in content and end_tag in content:
                    start = content.index(start_tag) + len(start_tag)
                    end = content.index(end_tag)
                    # Only modify keys for task division
                    key = f'subtask_{tag[-1]}' if tag.startswith('task') else tag
                    result[key] = content[start:end].strip()
            return result
        except Exception as e:
            print(colored(f"Error parsing {purpose} response: {e}", "red"))
            print(colored(f"Raw content: {content}", "yellow"))  # Debug output
            return None
            
    except Exception as e:
        print(colored(f"Error in {purpose}: {str(e)}", "red"))
        return None

async def get_task_division():
    messages = [
        {
            "role": "user",
            "content": TASK_MANAGER_PROMPT.format(task=TASK)
        }
    ]
    return await make_api_call(messages, MAIN_AGENT_MODEL, "Dividing main task into subtasks")

async def execute_subtask(subtask_description):
    messages = [
        {
            "role": "user",
            "content": f"{SYSTEM_PROMPT.format(specific_role=subtask_description)}\n\nTask: {TASK}"
        }
    ]
    return await make_api_call(messages, SUB_AGENT_MODEL, f"Executing subtask: {subtask_description[:50]}")

async def synthesize_results(subtask_results):
    synthesis_prompt = f"""Analyze and synthesize these three separate analyses into a comprehensive final report:

{json.dumps(subtask_results, indent=2)}

Format your response using XML tags like this:
<executive_summary>brief overview of key findings</executive_summary>
<detailed_analysis>comprehensive analysis combining all inputs</detailed_analysis>
<future_implications>what this means for the future</future_implications>
<recommendations>actionable next steps</recommendations>"""

    messages = [
        {
            "role": "user",
            "content": synthesis_prompt
        }
    ]
    return await make_api_call(messages, MAIN_AGENT_MODEL, "Synthesizing final results")

async def main():
    print(colored("🚀 Starting task execution...", "green"))
    
    # Get task division
    task_division = await get_task_division()
    if not task_division:
        return
    
    # Execute all subtasks concurrently
    subtask_results = {}
    tasks = []
    for i in range(1, 4):
        subtask_key = f"subtask_{i}"
        if subtask_key in task_division:
            task = asyncio.create_task(execute_subtask(task_division[subtask_key]))
            tasks.append((subtask_key, task))
    
    # Wait for all subtasks to complete
    for subtask_key, task in tasks:
        result = await task
        if result:
            subtask_results[subtask_key] = result
    
    # Synthesize results
    final_result = await synthesize_results(subtask_results)
    
    # Save results
    with open("task_results.json", "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=2)
        
    print(colored("✅ Task completed! Results saved to task_results.json", "green"))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(colored(f"❌ Error in main execution: {str(e)}", "red")) 
