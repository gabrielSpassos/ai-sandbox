# Rust Multi-Agent POC

This project is a minimal, proof-of-concept (POC) implementation of a multi-agent system in Rust, leveraging `tokio` for asynchronous communication.

## Architecture

The system is built on an **event-driven, decoupled architecture**:

1.  **Message Bus (`bus.rs`)**: Acts as a central mediator. Agents do not communicate directly. Instead, they publish messages to a central `MessageBus` using a `Topic` (e.g., `Task`, `ResearchResult`, `DraftResult`, `ReviewResult`). The bus then routes these messages to all agents subscribed to that specific topic.
2.  **Message System (`message.rs`)**: Defines the communication protocol, including the `Topic` enum and the structure of `Message` packets.
3.  **Agents (`agents/`)**: Independent, long-running asynchronous tasks that:
    *   Initialize their own communication channels.
    *   Subscribe to relevant topics.
    *   Loop, awaiting messages, processing them based on their specific role (Manager, Researcher, Writer, Reviewer), and potentially publishing new messages to the bus.

## Agent Roles

*   **Manager**: Initiates the task, evaluates reviewer feedback, and triggers system shutdown upon success.
*   **Researcher**: Gathers context and provides findings based on the assigned task.
*   **Writer**: Produces content based on research, and iteratively improves it based on reviewer feedback.
*   **Reviewer**: Critiques the writer's drafts based on content, providing feedback and a score to guide further revisions.

## Running the Project

To run this simulation:

1.  Ensure you have Rust installed.
2.  Navigate to the project directory: `cd rust-multi-agent-poc`
3.  Run the simulation using Cargo: `cargo run`

You will see colored output in your terminal corresponding to each agent's activity as the message bus orchestrates the workflow.
