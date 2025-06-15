use test_project::math;

#[test]
fn test_math_operations_integration() {
    // Test a sequence of operations
    let result = math::add(10.0, 5.0);
    assert_eq!(result, 15.0);
    
    let result = math::multiply(result, 2.0);
    assert_eq!(result, 30.0);
    
    let result = math::subtract(result, 10.0);
    assert_eq!(result, 20.0);
    
    let result = math::divide(result, 4.0);
    assert_eq!(result, 5.0);
}

#[test]
fn test_calculator_operations() {
    // Test all basic operations
    assert_eq!(math::add(1.5, 2.5), 4.0);
    assert_eq!(math::subtract(10.0, 3.0), 7.0);
    assert_eq!(math::multiply(4.0, 2.5), 10.0);
    assert_eq!(math::divide(15.0, 3.0), 5.0);
}

#[test]
fn test_edge_cases() {
    // Test with zero
    assert_eq!(math::add(0.0, 5.0), 5.0);
    assert_eq!(math::subtract(5.0, 0.0), 5.0);
    assert_eq!(math::multiply(0.0, 100.0), 0.0);
    
    // Test with negative numbers
    assert_eq!(math::add(-5.0, 3.0), -2.0);
    assert_eq!(math::subtract(-5.0, -3.0), -2.0);
    assert_eq!(math::multiply(-4.0, 2.0), -8.0);
    assert_eq!(math::divide(-10.0, 2.0), -5.0);
}

#[test]
fn test_floating_point_precision() {
    // Test floating point operations
    let result = math::divide(1.0, 3.0);
    assert!((result - 0.3333333333333333).abs() < f64::EPSILON);
    
    let result = math::multiply(0.1, 0.2);
    assert!((result - 0.02).abs() < 1e-10);
} 