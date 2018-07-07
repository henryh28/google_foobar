# ======================= final ===========================

from fractions import Fraction

# ====== Square matrix inversion code from SO ==============
# https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy

def transposeMatrix(m):
  t = []
  for r in range(len(m)):
    tRow = []
    for c in range(len(m[r])):
      if c == r:
        tRow.append(m[r][c])
      else:
        tRow.append(m[c][r])
    t.append(tRow)
  return t

def get_matrix_minor(m, i, j):
  return [row[:j] + row[j+1:] for row in (m[:i] + m[i+1:])]

def get_determinant(m):
  answer = 0
  if len(m) == 2:               # Base case for 2x2 matrix
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]

  for c in range(len(m)):
    answer += ((-1) ** c) * m[0][c] * get_determinant(get_matrix_minor(m,0,c))
  return answer

def matrix_inverse(m):
  cofactors = []
  determinant = get_determinant(m)

  if len(m) == 2:             #special case for 2x2 matrix:
    return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
      [-1 * m[1][0] / determinant, m[0][0] / determinant]]

  for r in range(len(m)):     #find matrix of cofactors
    cofactorRow = []
    for c in range(len(m)):
      minor = get_matrix_minor(m,r,c)
      cofactorRow.append(((-1)**(r+c)) * get_determinant(minor))
    cofactors.append(cofactorRow)
  cofactors = transposeMatrix(cofactors)

  for r in range(len(cofactors)):
    for c in range(len(cofactors)):
      cofactors[r][c] = cofactors[r][c] / determinant
  return cofactors

def multiply_matrices(a,b):
  zip_b = zip(*b)
  return [[sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b)) 
    for col_b in zip_b] for row_a in a]
# ============= end matrix inversion code from SO ============
def generate_submatrices (m, absorbing_index, nonabsorbing_index, identity, zero, sub_r, sub_q):
  """ Generate the needed submatrices for processing an absorbing markov chain """
  standard_form_by_index = absorbing_index + nonabsorbing_index

  # Define zero matrix
  for x in range(len(absorbing_index)):
    zero.append([0] * (len(standard_form_by_index) - len(absorbing_index)))

  # Define sub_r and sub_q matrix
  for na_index in nonabsorbing_index:
    temp_r, temp_q = [], []
    for index, value in enumerate(m[na_index]):
      if index in absorbing_index:
        temp_r.append(Fraction(value, sum(m[na_index])))
      else:
        temp_q.append(Fraction(value, sum(m[na_index])))

    sub_r.append(temp_r)
    sub_q.append(temp_q)

  #Define Identity matrix
  for x in range(len(nonabsorbing_index) - 1):
    identity[0].append(0)
  for x in range(len(nonabsorbing_index) - 1):
    identity.append(identity[x][-1:] + identity[x][:-1])

def separate_states_by_index(list_of_states, absorbing, nonabsorbing):
  """ Separate 'list_of_states' into lists of non/absorbing lists by index """
  for index, sublist in enumerate(list_of_states):
    absorbing.append(index) if sum(sublist) == 0 else nonabsorbing.append(index)

def lowest_common_multiple(numbers):
  ''' Return lowest common multiple of set of numbers in 'numbers' '''
  answer = 1
  complete = False

  while complete == False:
    complete = True
    for x in numbers:
      if x > answer:
        complete = False
        answer = x
        break
      if answer % x != 0:
        complete = False
        answer += 1

  return (answer)

def final_answer(answer, lcm):
  ''' Adjust values in 'answer' by lcm(lowest common multiple) '''
  for value in answer:
    if value[1] != lcm:
      multiply_by = lcm // value[1]
      value[0] *= multiply_by
      value[1] *= multiply_by

  return (answer)

def answer(m):
  absorbing_index, nonabsorbing_index, answer = [], [], []
  identity, zero, sub_r, sub_q, i_minus_q = [[1]], [], [], [], []

  # Edge case for small lists
  if len(m) < 2:
    return ([1,1])

  separate_states_by_index(m, absorbing_index, nonabsorbing_index)
  generate_submatrices(m, absorbing_index, nonabsorbing_index, identity, zero, sub_r, sub_q)

  # Find submatrix I - Q
  for i in range(len(nonabsorbing_index)):
    temp = []
    for j in range(len(nonabsorbing_index)):
      temp.append(identity[i][j] - sub_q[i][j])
    i_minus_q.append(temp)

  f = matrix_inverse(i_minus_q)
  fr = multiply_matrices(f, sub_r)

  for entry in fr[0]:
    answer.append([entry.numerator, entry.denominator])

  denoms = [item for sublist in answer for item in sublist][1::2]
  lcm = lowest_common_multiple(denoms)
  answer = final_answer(answer, lcm)

  final = [x for sublist in answer for x in sublist][::2] + [lcm]
  return (final)

# Case 1. Expected output: [0, 3, 2, 9, 14]
#m = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

# Case 2. Expected output: [7, 6, 8, 21]
#m = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

# case 3. Expected: [0, 3, 2, 9, 14]
#m=[[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

# case 4. Expected: [1, 2, 3]
#m=[[1, 2, 3, 0, 0, 0], [4, 5, 6, 0, 0, 0], [7, 8, 9, 1, 0, 0], [0, 0, 0, 0, 1, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

# case 5. Expected: [1, 1]
#m = [[0]]

# case 6. Expected: [1, 2, 3, 4, 5, 15]
#m = [[0, 0, 12, 0, 15, 0, 0, 0, 1, 8], [0, 0, 60, 0, 0, 7, 13, 0, 0, 0], [0, 15, 0, 8, 7, 0, 0, 1, 9, 0], [23, 0, 0, 0, 0, 1, 0, 0, 0, 0], [37, 35, 0, 0, 0, 0, 3, 21, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# case 7. Expected: [4, 5, 5, 4, 2, 20]
#m = [[0, 7, 0, 17, 0, 1, 0, 5, 0, 2], [0, 0, 29, 0, 28, 0, 3, 0, 16, 0], [0, 3, 0, 0, 0, 1, 0, 0, 0, 0], [48, 0, 3, 0, 0, 0, 17, 0, 0, 0], [0, 6, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# case 8. Expected: [1, 1, 1, 1, 1, 5]
m=[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# case 9. Expected: [2, 1, 1, 1, 1, 6]
#m=[[1, 1, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 1, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# case 10. Expected: [6, 44, 4, 11, 22, 13, 100]
#m=[[0, 86, 61, 189, 0, 18, 12, 33, 66, 39], [0, 0, 2, 0, 0, 1, 0, 0, 0, 0], [15, 187, 0, 0, 18, 23, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# case 11. Expected: [1, 1, 1, 2, 5]
#m=[[0, 0, 0, 0, 3, 5, 0, 0, 0, 2], [0, 0, 4, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 4, 4, 0, 0, 0, 1, 1], [13, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 1, 8, 7, 0, 0, 0, 1, 3, 0], [1, 7, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

print(answer(m))