use crate::message::{Message, Topic};
use std::collections::HashMap;
use tokio::sync::mpsc::{self, UnboundedReceiver, UnboundedSender};

pub struct MessageBus {
    subscribers: HashMap<Topic, Vec<UnboundedSender<Message>>>,
    publish_rx: UnboundedReceiver<Message>,
}

impl MessageBus {
    /// Creates a new MessageBus and returns the central publisher sender.
    pub fn new() -> (Self, UnboundedSender<Message>) {
        let (publish_tx, publish_rx) = mpsc::unbounded_channel();
        (
            Self {
                subscribers: HashMap::new(),
                publish_rx,
            },
            publish_tx,
        )
    }

    /// Subscribes an agent's input channel to a specific topic.
    pub fn subscribe(&mut self, topic: Topic, agent_mailbox_tx: UnboundedSender<Message>) {
        self.subscribers.entry(topic).or_default().push(agent_mailbox_tx);
    }

    /// Runs the message bus, routing incoming messages to their subscribed agents.
    pub async fn run(mut self) {
        println!("\x1b[90m[Broker] Message Bus started and listening...\x1b[0m");

        while let Some(msg) = self.publish_rx.recv().await {
            let topic = msg.topic;
            let mut delivered_count = 0;

            // Deliver to subscribers of the specific topic
            if let Some(subs) = self.subscribers.get(&topic) {
                for sub in subs {
                    if sub.send(msg.clone()).is_ok() {
                        delivered_count += 1;
                    }
                }
            }

            // SystemShutdown is special: broadcast it to ALL registered subscribers across all topics
            if topic == Topic::SystemShutdown {
                for subs in self.subscribers.values() {
                    for sub in subs {
                        let _ = sub.send(msg.clone());
                    }
                }
                println!("\x1b[90m[Broker] SystemShutdown broadcasted. Shutting down message bus...\x1b[0m");
                break;
            }

            println!(
                "\x1b[90m[Broker] Routed: Topic={:<15} From={:<10} Delivered to {} subscribers\x1b[0m",
                topic.as_str(),
                msg.sender,
                delivered_count
            );
        }
    }
}
