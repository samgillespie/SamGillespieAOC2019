
use std::time::Instant;

static INPUT: &str = include_str!("../data/q1input.txt");

type Error = Box<dyn std::error::Error>;
type Result<T, E = Error> = std::result::Result<T, E>;


fn calculate_weight(weight: i64, recursive: bool) -> i64 {
    let mut fuel: i64 = (weight/3) - 2;
    if recursive && fuel > 0 {
        let fuel_weight: i64 = calculate_weight(fuel, true);
        if fuel_weight >0 {
            fuel += fuel_weight;
        }
    }
    return fuel;
}


fn question_1() {
    let weights: Result<Vec<i64>, _> = INPUT.lines().map(str::parse::<i64>).collect();
    let weight: Vec<i64> = weights.unwrap();
    let mut total_fuel_part_a: i64 = 0;
    let mut total_fuel_part_b: i64 = 0;
    
    for weight_2 in weight {
        total_fuel_part_a += calculate_weight(weight_2, false);
        total_fuel_part_b += calculate_weight(weight_2, true);
    }
    
    println!("Question 1 Part A: {}", total_fuel_part_a);
    println!("Question 1 Part B: {}", total_fuel_part_b);
}


fn main() {
    let start = Instant::now();    
    question_1();
    let elapsed = start.elapsed();
    let sec = (elapsed.as_secs() as f64) + (elapsed.subsec_nanos() as f64 / 1000_000_000.0);
    println!("Seconds: {}", sec);
}