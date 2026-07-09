use crate::message::{Message, Topic};
use tokio::sync::mpsc::{UnboundedReceiver, UnboundedSender};
use tokio::time::{sleep, Duration};

pub struct ReviewerAgent {
    name: String,
    mailbox_rx: UnboundedReceiver<Message>,
    bus_tx: UnboundedSender<Message>,
}

impl ReviewerAgent {
    pub fn new(
        name: &str,
        mailbox_rx: UnboundedReceiver<Message>,
        bus_tx: UnboundedSender<Message>,
    ) -> Self {
        Self {
            name: name.to_string(),
            mailbox_rx,
            bus_tx,
        }
    }

    pub async fn run(mut self) {
        println!("\x1b[33m[{}] Agent initialized.\x1b[0m", self.name);

        while let Some(msg) = self.mailbox_rx.recv().await {
            match msg.topic {
                Topic::DraftResult => {
                    println!(
                        "\x1b[33m[{}] Received draft. Critiquing...\x1b[0m",
                        self.name
                    );

                    // Simulate review time
                    sleep(Duration::from_secs(1)).await;

                    // Critique based on content (simple check for keywords)
                    let score = if msg.payload.contains("high-dimensional") && msg.payload.contains("constellation") {
                        9.5
                    } else {
                        5.0
                    };

                    let feedback = if score < 8.0 {
                        format!(
                            "FEEDBACK:\n\
                            - Score: {:.1}\n\
                            - Critique: The draft is functional but lacks emotional depth and sophisticated vocabulary. \
                            Please incorporate themes of 'high-dimensional projections' and 'constellation' to better match research findings.",
                            score
                        )
                    } else {
                        format!(
                            "FEEDBACK:\n\
                            - Score: {:.1}\n\
                            - Critique: Excellent work! The narrative perfectly captures the essence of the synthetic dream.",
                            score
                        )
                    };

                    println!(
                        "\x1b[33m[{}] Review complete. Publishing feedback.\x1b[0m",
                        self.name
                    );

                    let _ = self.bus_tx.send(Message {
                        topic: Topic::ReviewResult,
                        sender: self.name.clone(),
                        payload: feedback,
                    });
                }
                Topic::SystemShutdown => {
                    println!("\x1b[33m[{}] Received shutdown signal. Terminating.\x1b[0m", self.name);
                    break;
                }
                _ => {}
            }
        }
    }
}
