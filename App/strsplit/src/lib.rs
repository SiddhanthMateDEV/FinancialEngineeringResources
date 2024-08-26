// #![warn(missing_debug_implementations, rust_2018_idioms, missing_docs)]
pub struct StrSplit<'a>{
    remainder: Option<&'a str>,
    delimiter: &'a str,
}

impl<'a> StrSplit<'a> {
    pub fn new(haystack: &'a str, delimiter: &'a str) -> Self {
        Self {
            remainder: Some(haystack),
            delimiter,
        }
    }
}

impl<'a> Iterator for StrSplit<'a> {
    type Item = &'a str;
    fn next(&mut self) -> Option<Self::Item> {
        let ref mut remainder = self.remainder.as_mut()?;
        if let Some(next_delim) = remainder.find(self.delimiter) {
            let until_delimiter = &remainder[..next_delim];
            *remainder = &remainder[(next_delim + self.delimiter.len())..];
            Some(until_delimiter)
        } else {
            self.remainder.take()
        }
    }
}



fn until_char<'a>(s: &'a str,c: &'a char)-> &'a str {
    StrSplit::new(s, &format!("{}",c)).next().expect("StrSplit always gives at least one resuly")

}

#[test]
fn until_char_test(s: &str,c: &char){
    assert_eq!(until_character("hello world", 'o'), hell);

}

#[test]
fn it_works(){
    let haystack = "a b c d e";
    // for letter in StrSplit::new(haystack, " ") {}
    let letters: Vec<&str> = StrSplit::new(haystack, " ").collect();
    assert_eq!(letters,vec!["a","b","c","d","e"]);
}

#[test]
fn tail(){
    let haystack = "a b c d ";
    // for letter in StrSplit::new(haystack, " ") {}
    let letters: Vec<&str> = StrSplit::new(haystack, " ").collect();
    assert_eq!(letters,vec!["a","b","c","d",""]);
}

