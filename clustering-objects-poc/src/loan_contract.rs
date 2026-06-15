#[derive(Debug, Clone)]
pub struct LoanContract {
    pub contract_id: u32,
    pub borrower: String,
    pub amount: f64,
    pub days_remaining: i32,
}
