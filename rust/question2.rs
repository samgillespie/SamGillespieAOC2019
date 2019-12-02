
use std::time::Instant;

static INPUT: &str = include_str!("../data/q2input.txt");

type Error = Box<dyn std::error::Error>;
type Result<T, E = Error> = std::result::Result<T, E>;

fn process_instruction(mut sequence: Vec<usize>, i: usize) -> Vec<usize> {     
    let opcode = sequence[i*4];
    let noun = sequence[sequence[i*4 + 1]];
    let verb = sequence[sequence[i*4 + 2]];
    let target_entry = sequence[i*4 + 3];

    let new_value: usize;
    if opcode == 1 {
        new_value = noun + verb;
    } else if opcode == 2 {
        new_value = noun * verb;
    } else {
        panic!("Invalid Opcode");
    }
    
    sequence[target_entry] = new_value;
    
    return sequence;
}

fn question_2a() -> usize {
    let sequence_result: Result<Vec<usize>, _> = INPUT.split(",").map(str::parse::<usize>).collect();
    let mut sequence = sequence_result.unwrap();
    sequence[1] = 12;
    sequence[2] = 2;
    let mut i: usize = 0;    
    loop {    
        if sequence[i * 4] == 99 {
            break;
        }
        sequence = process_instruction(sequence, i);
        i += 1;
    }
    return sequence[0];
}

fn question_2b(target_value: usize) -> usize {

    let sequence_result: Result<Vec<usize>, _> = INPUT.split(",").map(str::parse::<usize>).collect();
    let sequence = sequence_result.unwrap();
    for noun in 0..99 {
        for verb in 0..99 {
            let mut new_sequence = sequence.to_vec();
            new_sequence[1] = noun;
            new_sequence[2] = verb;
            let mut i: usize = 0;    
            loop {    
                if new_sequence[i * 4] == 99 {
                    break;
                }
                new_sequence = process_instruction(new_sequence, i);
                i += 1;
            }
            if new_sequence[0] == target_value{
                return noun*100 + verb;
            }
        }
    }
    return 0;
}

fn main() {
    let start = Instant::now();
    println!("Question 2 Part A: {}", question_2a());
    println!("Question 2 Part B: {}", question_2b(19690720));
    let elapsed = start.elapsed();
    let sec = (elapsed.as_secs() as f64) + (elapsed.subsec_nanos() as f64 / 1000_000_000.0);
    println!("Seconds: {}", sec);
}