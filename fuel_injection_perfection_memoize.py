def answer(n):
  results = {1: 0, 2: 1}

  def memoizer(n):
    even = (n % 2 == 0)
    if n in results:
      return results[n]

    if n & 1:
      results[n] = min(memoizer((n + 1) // 2) + 2, memoizer((n - 1) // 2) + 2)
    else:
      results[n] = memoizer(n // 2) + 1
    return results[n]

  return memoizer(n)
  