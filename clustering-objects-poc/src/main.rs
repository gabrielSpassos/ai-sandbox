mod clustering;
mod data;
mod loan_contract;
mod normalization;
mod analytics;

use analytics::print_cluster_summary;
use std::collections::HashMap;

use clustering::cluster_contracts;
use data::sample_contracts;

fn main() {
    let contracts = sample_contracts();

    let labels = cluster_contracts(&contracts, 4);

    let mut grouped: HashMap<usize, Vec<_>> = HashMap::new();

    for (contract, label) in contracts.iter().zip(labels.iter()) {
        grouped
            .entry(*label)
            .or_default()
            .push(contract);
    }

    for (cluster, contracts) in grouped {
        print_cluster_summary(cluster, &contracts);

        println!();
        println!("Cluster {}", cluster);
        println!("----------------");

        for contract in contracts {
            println!(
                "id={} borrower={} amount={} interest={} monthly={} days={} term={}",
                contract.contract_id,
                contract.borrower,
                contract.amount,
                contract.interest_rate,
                contract.monthly_payment,
                contract.days_remaining,
                contract.loan_term_months,
            );
        }
    }
}
