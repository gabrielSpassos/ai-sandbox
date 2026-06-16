#[derive(Debug, Clone)]
pub struct LoanContract {
    pub contract_id: u32,
    pub borrower: String,

    pub amount: f64,
    pub interest_rate: f64,
    pub monthly_payment: f64,

    pub days_remaining: i32,
    pub loan_term_months: i32,
}