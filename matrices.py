"""
Computes random matrices of dimension n.
Computes the least degree d of monomials needed to get n^2 linearly independent matrices if it exists.
Computes the value of g(i) = dim V_i = dim V_{i-1}
"""

import numpy
import random
import math

n = 3

# Returns a random nxn matrix
def rand_generate(n, p = None):
    if p == None:
        upper = 2
    else:
        upper = p
    m = []
    for i in range(n):
        m.append([])
        for j in range(n):
            k = random.randrange(upper)
            m[i].append(k)
    return m

# turns matrix into a single vector of dimension n^2
def vectorize(n, m):
    #assert(len(m) == len(m[0]))
    vect = []
    for i in range(n):
        for j in range(n):
            vect.append(m[i][j])
    return vect

# Creates an identity matrix of dimension n
def id(n):
    m = []
    for i in range(n):
        m.append([])
        for j in range(n):
            if i == j:
                m[i].append(1)
            else:
                m[i].append(0)
    return m

# create X and Y
# recursion to get the different monomials, storing those already computed
# while less than n^2, increase d and see if we get n linearly independent matrices
# make huge matrix of the vect(matrices) and find rank using numpy.linalg.matrix_rank
# we can use numpy.linalg.matmul(a, b)

# computes d of two matrices
def d(n, x, y, p = None, verbose = False):
    iteration = 0
    monomials = {0: [id(n)]}
    vectors = [vectorize(n, monomials[0][0])]
    if numpy.linalg.matrix_rank(vectors) == n**2:
        return 0
    prevrank = 1 # Should be one
    if verbose:
        print("Working")
    g = 1
    collisions = []
    for i in range(n**2):
        pastg = g
        iteration += 1
        monomials[iteration] = []
        #print(monomials[i])
        for m in monomials[i]:
            
            temp = numpy.matmul(m, x)
            monomials[iteration].append(temp)
            vectors = shave(vectors, vectorize(n, temp))
    
            temp = numpy.matmul(m, y)
            monomials[iteration].append(temp)
            vectors = shave(vectors, vectorize(n, temp))

        rank = numpy.linalg.matrix_rank(vectors)
        if verbose:
            print("Iteration: ", iteration, ", rank: ", rank)
            print("g(", iteration, ") = ", rank-prevrank)
        g = rank - prevrank
        if pastg == g:
            collisions.append(iteration)
        if g == 0:
            break
        if rank == n**2:
        #    display(x)
        #    print()
        #    display(y)
        #    print()
        #    print()
            return iteration
        prevrank = rank
    if iteration == n**2 and len(collisions) > 0:
        print("Collisions", collisions)
        print(x)
        print(y)
    return "Does not generate. Reached rank: " + str(rank)

# I tried to fix the weird bug with matrix_rank sometimes decreasing after adding vectors, but my efforts were unsucessful
def shave(vectors, v, give_up = True):
    if give_up:
        vectors.append(v)
    else:
        start_rank = numpy.linalg.matrix_rank(vectors)
        vectors.append(v)
        new_rank = numpy.linalg.matrix_rank(vectors)
        if start_rank == new_rank:
            vectors = vectors[:(len(vectors) - 1)]
    return vectors

def display(m):
    for i in range(len(m)):
        nums = ""
        for j in range(len(m[i])):
            nums += str(m[i][j]) + " "
        print(nums)

# Keeps generating new random matrices and seeing what the minimum needed degree is"
def test(n):
    p = None
    verbose = False
    results = {}
    for test in range(10000):
        if test % 100 == 0:
            print("Working:", test)
        x = rand_generate(n, p)
        y = rand_generate(n, p)
        degree = d(n,x,y,p,verbose)
        results[degree] = results.get(degree, 0) + 1

    for key in results:
        print(results[key], "tests yielded degree", key)
    #print("Minimum d: ", d(x,y,p,verbose))

# Creates a Heisenberg-like group and tests it. Currently unfinished
def heisenberg(n):
    # x is a shift matrix
    x = []
    for i in range(n):
        x.append([])
        for j in range(n):
            if i == (j + 1) % n:
                x[i].append(1)
            else:
                x[i].append(0)
                
    # y is a random diagonal matrix
    y = []
    upper = 100
    for i in range(n):
        y.append([])
        for j in range(n):
            if i == j:
                y[i].append(random.randrange(upper))
            else:
                y[i].append(0)

    print(d(n,x,y,None,True))

# Feel free to make your own interesting guesses for x and y, especially if you think the near the upperbound
def own_matrix_test(n):
    x = []
    for i in range(n):
        x.append([0]*n)
        #for i in range(n-min(numrows,n)):
        #x.append([0]*n)
    x[0][0] = 1
    y = []
    for i in range(n):
        y.append([])
        for j in range(n):
            if i == (j + 1) % n:
                y[i].append(1)
            else:
                y[i].append(0)

    print(d(n,x,y,None,True))

def lowerbound(dim):
    return math.ceil(math.log(dim**2+1,2)) - 1

# I think our current conjecture is that the upperbound is 2n-2?

# Runs test() over lots of dimensions
def multi_dim_test():
    for n in range(2,5):
        print(n, "expects", lowerbound(n))
        test(n)
        
#heisenberg()
#multi_dim_test()
#for i in range(1, 8):
#   own_matrix_test(i)
test(2)




