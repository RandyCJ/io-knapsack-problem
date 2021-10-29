import sys 
from sympy import Rational
from random import randrange
import copy
from timeit import default_timer as timer

def read_file(file_name):
    """ Function in charge or reading the txt file
        E: string with the problem's path
        S: a list with the knapsack weight and a list of tuples with the
            weight and benefits of each item
    """
    items = []
    count = 0

    try:
        with open(file_name,"r") as file:
            for line in file:
                current_item = line.split(",")
                current_item[-1] = current_item[-1].replace("\n", "")
                current_item = tuple(map(Rational, current_item))

                if count == 0:
                    knapsack_weight = current_item[0]
                else:
                    items.append(current_item)
                count += 1
        file.close()
    except:
        print("\nThe file doesn't exist or couldn't be open\n")
        quit()
    return [knapsack_weight, items]

def generate_items(number_of_items, weight_range, benefit_range):
    """ Function that generates a number of items with a random weight 
        and benefit
        E: number of items to generate, the weight and benefit range
        S: a list of tuples with the weight and benefits of each item
    """
    items = []

    for n in range(0, number_of_items):
        weight = randrange(weight_range[0], weight_range[1]+1)
        benefit = randrange(benefit_range[0], benefit_range[1]+1)
        items.append((weight, benefit))
    
    return items

def brute_force(knapsack_weight, items):
    """ Function that solves the knapsack problem with brute force, using a 
        list of 0's and 1's that represent all the posibles combinations of
        the items
        E: the knapsack weight and the items
        S: the max benefit, the items stored in the knapsack and the total 
        weight of those items
    """
    n = len(items)
    best_benefit = 0
    best_weight = 0
    best_items = []
    temp_items = [0 for _ in range(0, n)]

    #Iterating through all possible combinations of the items
    for _ in range(0, 2**n):
        j = n-1
        temp_weight = 0
        temp_benefit = 0
        while temp_items[j] != 0 and j >= 0:
            temp_items[j] = 0
            j -= 1
        temp_items[j] = 1
        for k in range(0, n):
            if temp_items[k] == 1:
                temp_weight += items[k][0]
                temp_benefit += items[k][1]
        if temp_benefit > best_benefit and temp_weight <= knapsack_weight:
            best_benefit = temp_benefit
            best_weight = temp_weight
            best_items = copy.deepcopy(temp_items)
    
    best_items = [(x+1, items[x]) for x in range(0, n) if best_items[x] == 1]
    return [best_benefit, best_items, best_weight]


def bottom_up(knapsack_weight,items):
    """ Function that solves the knapsack problem with dynamic programming (bottom_up)
        E: the knapsack weight and the items
        S: the max benefit, the items stored in the knapsack and the total 
        weight of those items
    """
    weights = []
    benefits=[]
    for i in items:
        weights.append(i[0])
        benefits.append(i[1])
    

    matrix = [[0 for _ in range(knapsack_weight + 1)] for _ in range(len(items) + 1)]
    
    best_items = []
    best_weight = []

    # Build matriz matrix[][] in bottom up manner
    for i in range(len(items) + 1):
        for w in range(knapsack_weight + 1):
            if i == 0 or w == 0:
                matrix[i][w] = 0
            elif weights[i-1] <= w:
                matrix[i][w] = max(benefits[i-1] + matrix[i-1][w-weights[i-1]],matrix[i-1][w])
            else:
                matrix[i][w] = matrix[i-1][w]
    best_benefit = matrix[-1][-1]
    
    #Find the items entered in the backpack (bottom_up)
    best_weight, best_items = find_items(matrix, items, knapsack_weight)
    
    return [best_benefit, best_items, best_weight]

def top_down(knapsack_weight, items):
    """ Function that prepares matrix for recursion
            E: the knapsack weight and the items
            S: the max benefit, the items stored in the knapsack and the total 
            weight of those items
    """
    tmp = [[-1 for _ in range(knapsack_weight + 1)] for _ in range(len(items))]
    return top_down_recursive(tmp, knapsack_weight, items, 0)


def top_down_recursive(matrix, knapsack_weight, items, ind):
    """ Function that solves the knapsack problem with top-down
            E: the knapsack weight, the items, the matrix and the index
            S: the best benefit, the items stored in the knapsack and the total
            weight of those items
    """
    if knapsack_weight <= 0 or ind >= len(items):
        return 0

    if matrix[ind][knapsack_weight] != -1:
        return matrix[ind][knapsack_weight]

    profit1 = 0
    if items[ind][0] <= knapsack_weight:
        profit1 = items[ind][1] + top_down_recursive(matrix, knapsack_weight - items[ind][0], items, ind + 1)

    profit2 = top_down_recursive(matrix, knapsack_weight, items, ind + 1)

    matrix[ind][knapsack_weight] = max(profit1, profit2)

    if matrix[0][-1] != -1:
        matrix.append([0 for x in range(len(matrix[0]))])
        max_benefit = matrix[ind][knapsack_weight]
        best_benefits_ind = []
        i = 0
        while max_benefit != 0:
            if matrix[i][-1] != max_benefit:
                best_benefits_ind.append(i-1)
                max_benefit = max_benefit - items[i-1][1]
            i += 1
        
        best_benefit = matrix[ind][knapsack_weight]
        best_weight = 0
        for i in best_benefits_ind:
            best_weight += items[i][0]
        
        best_items = []
        for i in best_benefits_ind:
            best_items.append((i+1, items[i]))
        return [best_benefit, best_items, best_weight]
    return matrix[ind][knapsack_weight]

def find_items(matrix, items, knapsack_weight):
    """ Gets stored knapsack items from matrix 
            E: A matrix from bottom-up or top-down, the items and the knapsack weight
            S: The weight and the items in the knapsack
    """

    best_items = []
    i = len(matrix)-1
    k = len(matrix[0])-1
    current_weight = 0

    while i!=0 and k!=0:
        if matrix[i-1][k] != matrix[i][k]:
            best_items.append((i, items[i-1]))
            k -= items[i-1][0]
            current_weight += items[i-1][0]
        i -= 1
    best_items.reverse()

    return [current_weight, best_items]


def perform_iterations(iterations, algorithm, knapsack_weight, items):
    total_time = float(0)

    for _ in range(iterations):
        if algorithm == 1:
            start = timer()
            brute_force(knapsack_weight, items)
            end = timer()
            total_time += end - start
        elif algorithm == 2:
            start = timer()
            bottom_up(knapsack_weight, items)
            end = timer()
            total_time += end - start
        else:
            start = timer()
            top_down(knapsack_weight, items)
            end = timer()
            total_time += end - start
    
    return total_time / iterations

def average_time():
    knapsack_weight = 200
    number_of_items = 17
    weight_range = [20, 35]
    benefit_range = [45, 70]
    iterations = 50
    items = generate_items(number_of_items, weight_range, benefit_range)

    # brute_force_avg = perform_iterations(iterations, 1, knapsack_weight, items)
    # bottom_up_avg = perform_iterations(iterations, 2, knapsack_weight, items)
    # #top_down_avg = perform_iterations(iterations, 3, knapsack_weight, items)

    # print("Brute force average time: " + str(brute_force_avg))
    # print("Bottom-up average time: " + str(bottom_up_avg))
    # print("Top-down average time: " + str(top_down_avg))

    print("Testing that the algorithms have the same answer")

    max_benefit_bf, saved_items_bf, total_weight_bf = brute_force(knapsack_weight, items)
    max_benefit_bu, saved_items_bu, total_weight_bu = bottom_up(knapsack_weight, items)

    # print("\nBrute force")
    # print("The max benefit is: " + str(max_benefit_bf))
    # print("With the items: " + str(saved_items_bf))
    # print("For the weight of: " + str(total_weight_bf))
    
    print("\nBrute force")
    print("The max benefit is: " + str(max_benefit_bf))
    print("With the items: " + str(saved_items_bf))
    print("For the weight of: " + str(total_weight_bf))

    print("\nBottom-up")
    print("The max benefit is: " + str(max_benefit_bu))
    print("With the items: " + str(saved_items_bu))
    print("For the weight of: " + str(total_weight_bu))

def main(args):
    """ Function that executes the program and receives the arguments
            E: the arguments given in the console
            S: N/A
    """

    if len(args) > 2: 
        if not(args[1].isdigit()): #Algorithm validation
            print("First argument must be an integer between 1,2,3")
            quit()
        if not(args[-1].isdigit()): #Iterations validation
            print("Last argument must be an integer")
            quit()
        algorithm = Rational(args[1])
        if algorithm not in [1, 2, 3]: #Algorithm validation
            print("First argument must be an integer between 1,2,3")
            quit()
        iterations = Rational(args[-1])

    if len(args) == 5: # if it's for reading a file
        if args[2] != "-a":
            print("Second argument must be '-a'")
            quit()
        knapsack_weight, items = read_file(args[3])
    
    elif len(args) == 8: #if it's to generate the problem
        if args[2] != "-p":
            print("Second argument must be '-p'")
            quit()
        if not(args[3].isdigit()):#Knapsack weight
            print("Third argument must be an integer")
            quit()
        if not(args[4].isdigit()):#Number of items
            print("Fourth argument must be an integer")
            quit()

        knapsack_weight = Rational(args[3])
        number_of_items = int(args[4])
        weight_range = list(map(int, args[5].split("-")))
        benefit_range = list(map(int, args[6].split("-")))
        items = generate_items(number_of_items, weight_range, benefit_range)

    else:
        #print("Please read the file 'README.MD' to learn how to execute the program")
        average_time()
        quit()

    print("Algorithm: " + str(algorithm))
    print("Iterations: " + str(iterations))
    print("Knapsack weight: " + str(knapsack_weight))
    print("Items: " + str(items))

    if algorithm == 1:
        max_benefit, saved_items, total_weight = brute_force(knapsack_weight, items)
    elif algorithm == 2:
        max_benefit, saved_items, total_weight = bottom_up(knapsack_weight,items) 
    else:
        max_benefit, saved_items, total_weight = top_down(knapsack_weight,items) 

    print("The max benefit is: " + str(max_benefit))
    print("With the items: " + str(saved_items))
    print("For the weight of: " + str(total_weight))

    return 0

main(sys.argv)