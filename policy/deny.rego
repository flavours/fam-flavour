package main


deny[msg] {
  not to_number(input.spec) == 0.1
  msg = "we only support flavour spec 0.1"
}
