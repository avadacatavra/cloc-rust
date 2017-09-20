extern crate unsafe_unicorn;

use unsafe_unicorn::{Cloc, ClocVerbosity};


fn main() {

    let mut cloc = Cloc::new();
    cloc.analyze_dir("/Users/ddh/mozilla/stylo").unwrap();
    println!("{}", cloc);

    // cloc.set_verbose(ClocVerbosity::File);
    // cloc.analyze_dir("./resources").unwrap();
    // println!("{}", cloc)

}
