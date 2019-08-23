package main


deny[msg] {
  not to_number(input.version) == 0.1
  msg = "we only support flavour version 0.1"
}
