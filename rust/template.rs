
use std::time::Instant;

static INPUT: &str = include_str!("../data/q2input.txt");

type Error = Box<dyn std::error::Error>;
type Result<T, E = Error> = std::result::Result<T, E>;

fn question_3() -> usize {
    
}

fn main() {
    let start = Instant::now();
    println!("Question 3 Part A: {}", question_3());
    println!("Question 3 Part B: {}", question_3());
    let elapsed = start.elapsed();
    let sec = (elapsed.as_secs() as f64) + (elapsed.subsec_nanos() as f64 / 1000_000_000.0);
    println!("Seconds: {}", sec);
}