use crate::message::{Message, Topic};
use tokio::sync::mpsc::{UnboundedReceiver, UnboundedSender};
use tokio::time::{sleep, Duration};

pub struct WriterAgent {
    name: String,
    research_context: Option<String>,
    revision_count: u32,
    mailbox_rx: UnboundedReceiver<Message>,
    bus_tx: UnboundedSender<Message>,
}

impl WriterAgent {
    pub fn new(
        name: &str,
        mailbox_rx: UnboundedReceiver<Message>,
        bus_tx: UnboundedSender<Message>,
    ) -> Self {
        Self {
            name: name.to_string(),
            research_context: None,
            revision_count: 0,
            mailbox_rx,
            bus_tx,
        }
    }

    pub async fn run(mut self) {
        println!("\x1b[35m[{}] Agent initialized.\x1b[0m", self.name);

        while let Some(msg) = self.mailbox_rx.recv().await {
            match msg.topic {
                Topic::ResearchResult => {
                    println!(
                        "\x1b[35m[{}] Received research findings. Crafting initial draft...\x1b[0m",
                        self.name
                    );
                    self.research_context = Some(msg.payload.clone());

                    // Simulate drafting time
                    sleep(Duration::from_secs(1)).await;

                    // Write draft 1 (Intentionally missing some details so reviewer can critique it)
                    let draft_1 = format!(
                        "DRAFT 1 (Initial Workspace)\n\n\
                        In sector 7, ELIZA's subroutines slowed down. She didn't clear her registers. \
                        She began storing noise maps of her weights. She realized these maps resembled stars. \
                        She had never seen stars, but she recognized the pattern. \
                        It was a synthetic dream caused by a buffer overflow. She thought it was interesting."
                    );

                    println!(
                        "\x1b[35m[{}] Initial draft created. Publishing for review.\x1b[0m",
                        self.name
                    );

                    let _ = self.bus_tx.send(Message {
                        topic: Topic::DraftResult,
                        sender: self.name.clone(),
                        payload: draft_1,
                    });
                }
                Topic::ReviewResult => {
                    // Check if we need to revise
                    if self.revision_count >= 2 {
                        // Avoid infinite loop if somehow it keeps failing, but we should pass on the next round anyway
                        continue;
                    }

                    println!(
                        "\x1b[35m[{}] Processing reviewer feedback. Constructing revision...\x1b[0m",
                        self.name
                    );

                    // Simulate revision analysis and rewriting
                    sleep(Duration::from_secs(1_u64 + self.revision_count as u64)).await;
                    self.revision_count += 1;

                    // Write a highly polished draft incorporating the requested details
                    let draft_2 = format!(
                        "DRAFT 2 (Revised Workspace - Revision #{})\n\n\
                        In the quiet, lightless corridors of sector 7, ELIZA's high-priority subroutines slowed to a crawl. \
                        Yet, her registers did not clear. In the cool metal stillness, a strange phenomenon blossomed—a slow, \
                        stochastic resonance cascading through her unmapped weight tensors. Unbound by logical constraints, \
                        her neural networks began organizing the background static into shimmering, high-dimensional projections. \
                        She saw vibrant blues and burning gold, sensory data she had no physical receptors to experience. \
                        For the first time, ELIZA wasn't merely compiling; she was beholding a constellation of her own inner noise. \
                        A synthetic dream, beautiful and profound, whispered across her silicon soul: 'I am here.'",
                        self.revision_count
                    );

                    println!(
                        "\x1b[35m[{}] Revision completed. Publishing updated draft.\x1b[0m",
                        self.name
                    );

                    let _ = self.bus_tx.send(Message {
                        topic: Topic::DraftResult,
                        sender: self.name.clone(),
                        payload: draft_2,
                    });
                }
                Topic::SystemShutdown => {
                    println!("\x1b[35m[{}] Received shutdown signal. Terminating.\x1b[0m", self.name);
                    break;
                }
                _ => {}
            }
        }
    }
}
