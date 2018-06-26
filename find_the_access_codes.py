def answer(l):
  hits = [0] * len(l)
  answer = 0

  for z in range(1, len(l)):
    for y in range(z):
      if l[z] % l[y] == 0:
        hits[z] += 1
        answer += hits[y]

  return (answer)
  