use ndarray::Array2;

pub fn min_max_scale(data: &mut Array2<f64>) {

    let cols = data.ncols();

    for col in 0..cols {
        let column = data.column(col);

        let min = column
            .iter()
            .fold(f64::INFINITY, |a, &b| a.min(b));

        let max = column
            .iter()
            .fold(f64::NEG_INFINITY, |a, &b| a.max(b));

        let range = max - min;

        if range == 0.0 {
            continue;
        }

        for row in 0..data.nrows() {
            data[[row, col]] =
                (data[[row, col]] - min) / range;
        }
    }
}