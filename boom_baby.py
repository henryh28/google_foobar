def answer(M, F):
  answer = 0
  high = max(int(M), int(F))
  low = min(int(M), int(F))

  # Bombs can't grow negatively
  if (high < 1 or low < 1):
    return ("impossible")

  # Both F & M have be 2 or greater
  while (high > 1 and low > 1):
    if (high % low == 0):
      return ("impossible")
    # Optimizes for cases in which high value is much greater than lower value
    answer += high // low
    high = high % low
    high, low = low, high

  # low value will be a 1. special case so answer will be the same as starting with any positive value and 1
  answer += high - 1
  
  return (str(answer))
  
  # Reference: https://github.com/ivanseed/google-foobar-help/blob/master/challenges/bomb_baby/bomb_baby.md to clarify instruction
  