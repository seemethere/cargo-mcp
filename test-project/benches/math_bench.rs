use criterion::{black_box, criterion_group, criterion_main, Criterion};

// We need to import our math functions from the main crate
use test_project::math;

fn bench_add(c: &mut Criterion) {
    c.bench_function("add", |b| {
        b.iter(|| math::add(black_box(42.0), black_box(24.0)))
    });
}

fn bench_subtract(c: &mut Criterion) {
    c.bench_function("subtract", |b| {
        b.iter(|| math::subtract(black_box(42.0), black_box(24.0)))
    });
}

fn bench_multiply(c: &mut Criterion) {
    c.bench_function("multiply", |b| {
        b.iter(|| math::multiply(black_box(42.0), black_box(24.0)))
    });
}

fn bench_divide(c: &mut Criterion) {
    c.bench_function("divide", |b| {
        b.iter(|| math::divide(black_box(42.0), black_box(24.0)))
    });
}

fn bench_complex_operations(c: &mut Criterion) {
    c.bench_function("complex_math", |b| {
        b.iter(|| {
            let a = black_box(10.0);
            let b = black_box(5.0);
            let c = black_box(3.0);
            
            // Perform a complex calculation: (a + b) * c / (a - b)
            let step1 = math::add(a, b);
            let step2 = math::multiply(step1, c);
            let step3 = math::subtract(a, b);
            math::divide(step2, step3)
        })
    });
}

criterion_group!(
    benches,
    bench_add,
    bench_subtract,
    bench_multiply,
    bench_divide,
    bench_complex_operations
);
criterion_main!(benches); 