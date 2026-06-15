use crate::loan_contract::LoanContract;

pub fn print_cluster_summary(
    cluster_id: usize,
    contracts: &[&LoanContract],
) {
    let count = contracts.len();

    let avg_amount = contracts
        .iter()
        .map(|c| c.amount)
        .sum::<f64>()
        / count as f64;

    let avg_interest = contracts
        .iter()
        .map(|c| c.interest_rate)
        .sum::<f64>()
        / count as f64;

    let avg_monthly_payment = contracts
        .iter()
        .map(|c| c.monthly_payment)
        .sum::<f64>()
        / count as f64;

    let avg_days = contracts
        .iter()
        .map(|c| c.days_remaining as f64)
        .sum::<f64>()
        / count as f64;

    let avg_term = contracts
        .iter()
        .map(|c| c.loan_term_months as f64)
        .sum::<f64>()
        / count as f64;

    println!();
    println!("Cluster {}", cluster_id);
    println!("========================");
    println!("Contracts: {}", count);
    println!("Average Amount: {:.2}", avg_amount);
    println!("Average Interest Rate: {:.2}%", avg_interest);
    println!("Average Monthly Payment: {:.2}", avg_monthly_payment);
    println!("Average Days Remaining: {:.0}", avg_days);
    println!("Average Loan Term: {:.0} months", avg_term);
}