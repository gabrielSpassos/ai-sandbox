#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Topic {
    Task,            // New task / assignment from Manager
    ResearchResult,  // Found facts or context from Researcher
    DraftResult,     // Draft written by Writer
    ReviewResult,    // Feedback and score from Reviewer
    SystemShutdown,  // Graceful shutdown signal
}

impl Topic {
    pub fn as_str(&self) -> &'static str {
        match self {
            Topic::Task => "Task",
            Topic::ResearchResult => "ResearchResult",
            Topic::DraftResult => "DraftResult",
            Topic::ReviewResult => "ReviewResult",
            Topic::SystemShutdown => "SystemShutdown",
        }
    }
}

#[derive(Debug, Clone)]
pub struct Message {
    pub topic: Topic,
    pub sender: String,
    pub payload: String,
}
