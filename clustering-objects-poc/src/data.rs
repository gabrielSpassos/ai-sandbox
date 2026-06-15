use crate::loan_contract::LoanContract;

pub fn sample_contracts() -> Vec<LoanContract> {
    vec![
        LoanContract {
            contract_id: 1,
            borrower: "Alice".to_string(),
            amount: 10_000.0,
            days_remaining: 30,
        },
        LoanContract {
            contract_id: 2,
            borrower: "Bob".to_string(),
            amount: 12_000.0,
            days_remaining: 25,
        },
        LoanContract {
            contract_id: 3,
            borrower: "Carol".to_string(),
            amount: 15_000.0,
            days_remaining: 40,
        },
        LoanContract {
            contract_id: 4,
            borrower: "Dave".to_string(),
            amount: 500_000.0,
            days_remaining: 720,
        },
        LoanContract {
            contract_id: 5,
            borrower: "Eve".to_string(),
            amount: 450_000.0,
            days_remaining: 680,
        },
        LoanContract {
            contract_id: 6,
            borrower: "Frank".to_string(),
            amount: 600_000.0,
            days_remaining: 800,
        },
    ]
}
