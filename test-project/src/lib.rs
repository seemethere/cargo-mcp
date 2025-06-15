pub mod math {
    /// Add two numbers
    pub fn add(a: f64, b: f64) -> f64 {
        a + b
    }
    
    /// Subtract two numbers
    pub fn subtract(a: f64, b: f64) -> f64 {
        a - b
    }
    
    /// Multiply two numbers
    pub fn multiply(a: f64, b: f64) -> f64 {
        a * b
    }
    
    /// Divide two numbers
    pub fn divide(a: f64, b: f64) -> f64 {
        if b == 0.0 {
            panic!("Division by zero");
        }
        a / b
    }
}

#[cfg(test)]
mod tests {
    use super::math;
    
    #[test]
    fn test_add() {
        assert_eq!(math::add(2.0, 3.0), 5.0);
        assert_eq!(math::add(-1.0, 1.0), 0.0);
        assert_eq!(math::add(0.0, 0.0), 0.0);
    }
    
    #[test]
    fn test_subtract() {
        assert_eq!(math::subtract(5.0, 3.0), 2.0);
        assert_eq!(math::subtract(0.0, 5.0), -5.0);
        assert_eq!(math::subtract(3.0, 3.0), 0.0);
    }
    
    #[test]
    fn test_multiply() {
        assert_eq!(math::multiply(2.0, 3.0), 6.0);
        assert_eq!(math::multiply(-2.0, 3.0), -6.0);
        assert_eq!(math::multiply(0.0, 5.0), 0.0);
    }
    
    #[test]
    fn test_divide() {
        assert_eq!(math::divide(6.0, 2.0), 3.0);
        assert_eq!(math::divide(5.0, 2.0), 2.5);
        assert_eq!(math::divide(-6.0, 2.0), -3.0);
    }
    
    #[test]
    #[should_panic]
    fn test_divide_by_zero() {
        math::divide(5.0, 0.0);
    }
} 