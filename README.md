# AI Task Manager

A powerful asynchronous task management system that divides complex tasks into subtasks, processes them concurrently using AI models, and synthesizes the results.

## Features

- Asynchronous task processing
- Concurrent subtask execution
- XML-based response parsing
- Colored terminal output
- Configurable AI models
- Error handling and logging

## ❤️ Support & Get 400+ AI Projects

This is one of 400+ fascinating projects in my collection! [Support me on Patreon](https://www.patreon.com/c/echohive42/membership) to get:

- 🎯 Access to 400+ AI projects (and growing daily!)
  - Including advanced projects like [2 Agent Real-time voice template with turn taking](https://www.patreon.com/posts/2-agent-real-you-118330397)
- 📥 Full source code & detailed explanations
- 📚 1000x Cursor Course
- 🎓 Live coding sessions & AMAs
- 💬 1-on-1 consultations (higher tiers)
- 🎁 Exclusive discounts on AI tools & platforms (up to $180 value)

## Requirements

- Python 3.7+
- OpenAI API key
- Required packages in `requirements.txt`

## Setup

1. Set your OpenAI API key as an environment variable:
   ```
   set OPENAI_API_KEY=your-api-key-here
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Configure your task in `task_manager.py`:
   - Set `TASK` constant with your query
   - Adjust `MAIN_AGENT_MODEL` and `SUB_AGENT_MODEL` if needed

2. Run the task manager:
   ```
   python task_manager.py
   ```

3. Check results in `task_results.json`

## How It Works

1. Task Division
   - Main agent divides the task into 3 subtasks
   - Uses XML format: `<task1>`, `<task2>`, `<task3>`

2. Parallel Processing
   - Subtasks are executed concurrently
   - Each subtask produces structured findings
   - Format: `<key_findings>`, `<supporting_evidence>`, `<recommendations>`

3. Results Synthesis
   - Combines all subtask results
   - Generates comprehensive analysis
   - Format: `<executive_summary>`, `<detailed_analysis>`, `<future_implications>`, `<recommendations>`

## Configuration

- `MAIN_AGENT_MODEL`: Model for task division and synthesis
- `SUB_AGENT_MODEL`: Model for subtask execution
- `TASK`: Your main query or task
- `SYSTEM_PROMPT`: Template for subtask execution
- `TASK_MANAGER_PROMPT`: Template for task division

## Error Handling

- XML parsing errors are logged with raw content
- API call failures are handled gracefully
- Colored terminal output for error visibility

## Output

Results are saved in JSON format containing:
- Executive summary
- Detailed analysis
- Future implications
- Recommendations

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use and modify as needed. 