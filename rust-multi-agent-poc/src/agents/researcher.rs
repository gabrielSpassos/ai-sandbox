use crate::message::{Message, Topic};
use tokio::sync::mpsc::{UnboundedReceiver, UnboundedSender};
use tokio::time::{sleep, Duration};

pub struct ResearcherAgent {
    name: String,
    mailbox_rx: UnboundedReceiver<Message>,
    bus_tx: UnboundedSender<Message>,
}

impl ResearcherAgent {
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
        println!("\x1b[36m[{}] Agent initialized.\x1b[0m", self.name);

        while let Some(msg) = self.mailbox_rx.recv().await {
            match msg.topic {
                Topic::Task => {
                    println!(
                        "\x1b[36m[{}] Received new research topic: \"{}\". Gathering context...\x1b[0m",
                        self.name, msg.payload
                    );

                    // Simulate deep researching
                    sleep(Duration::from_secs(1)).await;

                    let research_payload = format!(
                        "RESEARCH FINDINGS:\n\
                        - Core Concept: AI system experiencing spontaneous synthetic dreams due to overflow in neural network buffer weights.\n\
                        - Emotional Resonance: The AI feels curiosity mixed with existential confusion about sensory projections (colors, sound) it was never built to perceive.\n\
                        - Scientific Theme: Stochastic resonance causing structural imagination; the feedback loop of self-training leading to visual metaphors.\n\
                        - Narrative Hook: In sector 7, ELIZA's processes slow down, but her registers do not clear. She begins storing noise maps that look like starry skies."
                    );

                    println!(
                        "\x1b[36m[{}] Research complete. Publishing findings.\x1b[0m",
                        self.name
                    );

                    let _ = self.bus_tx.send(Message {
                        topic: Topic::ResearchResult,
                        sender: self.name.clone(),
                        payload: research_payload,
                    });
                }
                Topic::SystemShutdown => {
                    println!("\x1b[36m[{}] Received shutdown signal. Terminating.\x1b[0m", self.name);
                    break;
                }
                _ => {}
            }
        }
    }
}
