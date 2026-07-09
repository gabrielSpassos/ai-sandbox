mod agents;
mod bus;
mod message;

use crate::agents::manager::ManagerAgent;
use crate::agents::researcher::ResearcherAgent;
use crate::agents::reviewer::ReviewerAgent;
use crate::agents::writer::WriterAgent;
use crate::bus::MessageBus;
use crate::message::Topic;
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    println!("\x1b[1;32m--- Initializing Multi-Agent System ---\x1b[0m");

    let (mut bus, bus_tx) = MessageBus::new();

    // Create channels for each agent
    let (manager_tx, manager_rx) = mpsc::unbounded_channel();
    let (researcher_tx, researcher_rx) = mpsc::unbounded_channel();
    let (writer_tx, writer_rx) = mpsc::unbounded_channel();
    let (reviewer_tx, reviewer_rx) = mpsc::unbounded_channel();

    // Subscribe agents to topics
    bus.subscribe(Topic::Task, researcher_tx);
    bus.subscribe(Topic::Task, manager_tx.clone()); // Manager needs to see its own task back or just receive results
    bus.subscribe(Topic::ResearchResult, writer_tx.clone());
    bus.subscribe(Topic::DraftResult, reviewer_tx.clone());
    bus.subscribe(Topic::ReviewResult, writer_tx);
    bus.subscribe(Topic::ReviewResult, manager_tx.clone());
    
    // Subscribe all to shutdown
    bus.subscribe(Topic::SystemShutdown, manager_tx);

    // Initialize Agents
    let manager = ManagerAgent::new("Manager", "Write a short story about an AI experiencing synthetic dreams.", manager_rx, bus_tx.clone());
    let researcher = ResearcherAgent::new("Researcher", researcher_rx, bus_tx.clone());
    let writer = WriterAgent::new("Writer", writer_rx, bus_tx.clone());
    let reviewer = ReviewerAgent::new("Reviewer", reviewer_rx, bus_tx.clone());

    // Spawn agents
    tokio::spawn(manager.run());
    tokio::spawn(researcher.run());
    tokio::spawn(writer.run());
    tokio::spawn(reviewer.run());

    // Run the bus
    bus.run().await;

    println!("\x1b[1;32m--- Multi-Agent System Shutdown ---\x1b[0m");
}
