def is_period(input_char):
  return input_char == "."

def is_hyphen(input_char):
  return input_char == "-"

def is_zero(input_char):
  return input_char == "0"

is_digit = str.isdigit

# returns a list of characters in a string which meet a given boolean condition (i.e. a "predicate" function)
def xs_in_string(pred, input_string):
  return list(filter(pred, input_string))

# counts the number of characters in a string which, as above, "satisfies the predicate"
def count_xs(pred, input_string):
  return len(xs_in_string(pred, input_string))
  

def is_valid_number(input_string) -> bool:
  # case: "no input" (i.e. empty string)
  # requirement: input_string must contain one or more characters
  if(len(input_string) == 0):
    # print("no input for input string '" + input_string + "'") # debugging
    return False
  
  # case: "bad input" (any non hyphen, non-period, non-digit characters)
  # requirement: only digits, hyphens, and periods are allowed for the input_string to be a valid number
  for char in input_string:
    if ((char != "-") and (char != ".") and (not char.isdigit())):
      # print("bad input '" + char + "' found in input string '" + input_string + "'") # debugging
      return False
    
  # scenarios: input_string has more than 1 hyphen OR if the hyphen is anywhere but in the first index
  # - requirement: max 1 hyphen
  # case: too many hyphens
  if (count_xs(is_hyphen, input_string) > 1):
    # print("too many hyphens detected in string '" + input_string + "'") # debugging
    return False
  
  # - requirement: hyphen, if it exists, is always first
  # case: hyphens detected anywhere but the beginning
  if ((count_xs(is_hyphen, input_string) == 1) and (input_string[0] != "-")):
    # print("hyphen is not in the correct location for string '" + input_string + "'") # debugging
    return False
  
  # scenarios: more than 1 period OR period is first, last, or second after a hyphen (the period must be preceded *and* followed by at least one number)
  # - req: max 1 period
  # - req: period is NOT in the first index
  # - req: period is NOT in the last index
  # - req: period is NOT in the 2nd index IF input_string starts with a hyphen
  
  # case: "insufficient valid input"
  # if(len(list(filter(str.isdigit, input_string))) == 0): # pre-refactor
  if (count_xs(is_digit, input_string) == 0): # post-refactor
    # print("insufficient digits in input string '" + input_string + "'") # debugging
    return False
  
  # scenarios: periods in inappropriate places
  # case: periods at the string's caps (beginning or end)
  if((input_string[0] == ".") or (input_string[-1] == ".")):
    # print("period found at head or tail or tail of string for input '" + input_string + "'") # debugging
    return False
  
  # case: too many periods
  if (count_xs(is_period, input_string) > 1):
    # print("too many periods found in input string '" + input_string + "'") # debugging
    return False
  
  # - case: a period just after a hyphen
  if((input_string[0] == "-") and (input_string[1] == ".")):
    # print("hyphen preceding a period detected in input '" + input_string + "'") # debugging
    return False
  
  # Q: How about 'numbers' like this? 00123 --> this is no good
  # I've decided that leading zeroes are no good :P
  # Q: how to detected multiple consecutive zeroes in the beginning of the number (with hyphen suffix or not)
  
  # req: no consecutive leading zeroes
  # case: has_a_leading_zero_preceding_a_non_period
  if((len(input_string) > 1) and 
     (((input_string[0] == "0") and
       (input_string[1] != ".")) # eg. "05" number starts with a zero and is followed by another digit (i.e. not a period)
      or (len(input_string) > 2) and 
      ((input_string[0] == "-") and
       (input_string[1] == "0") and 
       (input_string[2] != ".")))): # eg. -01 number starts with a hyphen, followed by a zero, followed by another digit (i.e. not a period)
    # print("leading zero preceding a non-period detected in string '" + input_string + "'") # debugging
    return False
  
  # trailing zeroes are OK (presumably for showing precision)
  # Q: is negative zero an acceptable number? --> let's say no
  # case: negative zero (integer or decimal number)
  if((input_string[0] == "-") and (count_xs(is_digit, input_string) == count_xs(is_zero, input_string))):
    # print("negative zero is not a valid number") # debugging
    return False
  
  # if we've reached this point, this means that we have a valid number, and we can now return True
  return True

