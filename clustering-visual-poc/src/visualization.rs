use linfa::prelude::*;
use linfa_reduction::Pca;
use ndarray::Array2;
use plotters::prelude::*;

pub fn create_cluster_plot(
    dataset: Array2<f64>,
    labels: &[usize],
) -> Result<(), Box<dyn std::error::Error>> {

    let dataset = DatasetBase::from(dataset);

    let pca = Pca::params(2)
        .fit(&dataset)?;

    let transformed = pca.transform(dataset);

    let records = transformed.records();

    let xs: Vec<f64> =
        records.column(0).iter().copied().collect();

    let ys: Vec<f64> =
        records.column(1).iter().copied().collect();

    let x_min =
        xs.iter().copied().fold(f64::INFINITY, f64::min);

    let x_max =
        xs.iter().copied().fold(f64::NEG_INFINITY, f64::max);

    let y_min =
        ys.iter().copied().fold(f64::INFINITY, f64::min);

    let y_max =
        ys.iter().copied().fold(f64::NEG_INFINITY, f64::max);

    let root =
        BitMapBackend::new(
            "clusters.png",
            (1200, 800),
        )
        .into_drawing_area();

    root.fill(&WHITE)?;

    let mut chart = ChartBuilder::on(&root)
        .caption(
            "Loan Contract Clusters (PCA)",
            ("sans-serif", 40),
        )
        .margin(20)
        .x_label_area_size(40)
        .y_label_area_size(40)
        .build_cartesian_2d(
            x_min..x_max,
            y_min..y_max,
        )?;

    chart.configure_mesh().draw()?;

    for (idx, point) in records.outer_iter().enumerate() {

        let cluster = labels[idx];

        let color = match cluster {
            0 => &RED,
            1 => &BLUE,
            2 => &GREEN,
            3 => &MAGENTA,
            _ => &BLACK,
        };

        chart.draw_series(
            std::iter::once(
                Circle::new(
                    (point[0], point[1]),
                    6,
                    color.filled(),
                )
            )
        )?;
    }

    root.present()?;

    println!();
    println!("Generated: clusters.png");

    Ok(())
}
