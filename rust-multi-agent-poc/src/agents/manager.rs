use crate::message::{Message, Topic};
use tokio::sync::mpsc::{UnboundedReceiver, UnboundedSender};
use tokio::time::{sleep, Duration};

pub struct ManagerAgent {
    name: String,
    task: String,
    mailbox_rx: UnboundedReceiver<Message>,
    bus_tx: UnboundedSender<Message>,
}

impl ManagerAgent {
    pub fn new(
        name: &str,
        task: &str,
        mailbox_rx: UnboundedReceiver<Message>,
        bus_tx: UnboundedSender<Message>,
    ) -> Self {
        Self {
            name: name.to_string(),
            task: task.to_string(),
            mailbox_rx,
            bus_tx,
        }
    }

    pub async fn run(mut self) {
        println!("\x1b[34m[{}] Agent initialized.\x1b[0m", self.name);
        
        // Wait briefly for all agents to subscribe and boot up
        sleep(Duration::from_millis(200)).await;

        // Publish the initial task
        println!(
            "\x1b[34m[{}] New Mission Objective: \"{}\"\x1b[0m",
            self.name, self.task
        );
        let _ = self.bus_tx.send(Message {
            topic: Topic::Task,
            sender: self.name.clone(),
            payload: self.task.clone(),
        });

        // Listen for results and reviews
        while let Some(msg) = self.mailbox_rx.recv().await {
            match msg.topic {
                Topic::ReviewResult => {
                    println!(
                        "\x1b[34m[{}] Received Review from '{}':\n----------------------------------------\n{}\n----------------------------------------\x1b[0m",
                        self.name, msg.sender, msg.payload
                    );
                    
                    let score = extract_score(&msg.payload).unwrap_or(0.0);
                    println!("\x1b[34m[{}] Evaluation score: {:.1} / 10.0\x1b[0m", self.name, score);

                    if score >= 8.0 {
                        println!(
                            "\x1b[34m[{}] SUCCESS: Quality threshold met ({:.1} >= 8.0). Goal accomplished!\x1b[0m",
                            self.name, score
                        );
                        // Signal system-wide shutdown
                        let _ = self.bus_tx.send(Message {
                            topic: Topic::SystemShutdown,
                            sender: self.name.clone(),
                            payload: "Goal accomplished!".to_string(),
                        });
                        break;
                    } else {
                        println!(
                            "\x1b[34m[{}] REJECTED: Quality below threshold ({:.1} < 8.0). Awaiting revision from Writer...\x1b[0m",
                            self.name, score
                        );
                    }
                }
                Topic::SystemShutdown => {
                    println!("\x1b[34m[{}] Received shutdown signal. Terminating.\x1b[0m", self.name);
                    break;
                }
                _ => {}
            }
        }
    }
}

/// Helper function to parse score from evaluation feedback.
fn extract_score(payload: &str) -> Option<f64> {
    let lower = payload.to_lowercase();
    if let Some(idx) = lower.find("score:") {
        let after = &payload[idx + 6..];
        let trimmed = after.trim();
        let mut float_str = String::new();
        for c in trimmed.chars() {
            if c.is_ascii_digit() || c == '.' {
                float_str.push(c);
            } else {
                break;
            }
        }
        float_str.parse::<f64>().ok()
    } else {
        None
    }
}
