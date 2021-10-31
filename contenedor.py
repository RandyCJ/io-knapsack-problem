import sys 
from sympy import Rational
from random import randrange
import copy
from timeit import default_timer as timer

def read_file(file_name):
    """ Function in charge or reading the txt file
        I: string with the problem's path
        O: a list with the knapsack weight and a list of tuples with the
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
        I: number of items to generate, the weight and benefit range
        O: a list of tuples with the weight and benefits of each item
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
        I: the knapsack weight and the items
        O: the max benefit, the items stored in the knapsack and the total 
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
        I: the knapsack weight and the items
        O: the max benefit, the items stored in the knapsack and the total 
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
    best_weight, best_items = find_items(matrix, items)
    
    return [best_benefit, best_items, best_weight]

def top_down(knapsack_weight, items):
    """ Function that prepares matrix for recursion
        I: the knapsack weight and the items
        O: the max benefit, the items stored in the knapsack and the total 
           weight of those items
     """
    tmp_ben = [[-1 for _ in range(knapsack_weight + 1)] for _ in range(len(items))]
    max_benefit, index_selected_items = top_down_recursive(tmp_ben, knapsack_weight, items, 0, [])

    weight = 0
    best_items = []
    for index in index_selected_items:
        best_items.append((index+1, items[index]))
        weight += items[index][0]
    
    return [max_benefit, best_items, weight]

def top_down_recursive(matrix, knapsack_weight, items, ind, items_indexes):
    """ Function that solves the knapsack problem with top-down
        I: The knapsack weight, the items, the matrix, the index and the listed items in the knapsack
        O: The best benefit and the indexes of the items stored in the knapsack
    """
    if ind >= len(items) or knapsack_weight <= 0:
        return [0, items_indexes]

    if knapsack_weight < items[ind][0]:
        matrix[ind][knapsack_weight], selected_items = top_down_recursive(matrix, knapsack_weight, items, ind+1, items_indexes)
    else:
        tmp = copy.deepcopy(items_indexes)
        tmp.append(ind)
        res = top_down_recursive(matrix, knapsack_weight-items[ind][0], items, ind+1, tmp)
        profit1 = items[ind][1] + res[0]
        items1 = res[1]
        profit2, items2 = top_down_recursive(matrix, knapsack_weight, items, ind+1, items_indexes)

        if profit1 >= profit2:
            matrix[ind][knapsack_weight] = profit1
            selected_items = items1
        else:
            matrix[ind][knapsack_weight] = profit2
            selected_items = items2
            
    return [matrix[ind][knapsack_weight], selected_items]

def find_items(matrix, items):
    """ Gets stored knapsack items from matrix 
        I: A matrix from bottom-up or top-down, the items and the knapsack weight
        O: The weight and the items in the knapsack
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
    """ Perform n iterations of an algorithm, and estimates the average time
        I: number of iterations, the algorithm, the knapsack weight and the items
        O: returns the average time
    """
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
    """ Calculates the average time of the three algorithms
        I: N/A
        O: N/A
    """
    knapsack_weight = 200
    number_of_items = 20
    weight_range = [20, 35]
    benefit_range = [45, 70]
    iterations = 15
    items = generate_items(number_of_items, weight_range, benefit_range)
    print("\nITEMS: " + str(items) + "\n")

    brute_force_avg = perform_iterations(iterations, 1, knapsack_weight, items)
    bottom_up_avg = perform_iterations(iterations, 2, knapsack_weight, items)
    top_down_avg = perform_iterations(iterations, 3, knapsack_weight, items)

    print("\nBrute force average time: " + str(brute_force_avg))
    print("Bottom-up average time: " + str(bottom_up_avg))
    print("Top-down average time: " + str(top_down_avg))

    print("\nTesting that the algorithms have the same answer")

    max_benefit_bf, saved_items_bf, total_weight_bf = brute_force(knapsack_weight, items)
    items_benefit_bf = calculate_benefit(saved_items_bf, max_benefit_bf)
    max_benefit_bu, saved_items_bu, total_weight_bu = bottom_up(knapsack_weight, items)
    items_benefit_bu = calculate_benefit(saved_items_bu, max_benefit_bu)
    max_benefit_td, saved_items_td, total_weight_td = top_down(knapsack_weight, items)
    items_benefit_td = calculate_benefit(saved_items_td, max_benefit_td)
    
    print("\nBrute force")
    print("The max benefit is: " + str(max_benefit_bf))
    print("With the items: " + str(saved_items_bf))
    print("Weight: " + str(total_weight_bf))
    print("Benefit equals to items benefit?: " + str(items_benefit_bf))

    print("\nBottom-up")
    print("The max benefit is: " + str(max_benefit_bu))
    print("With the items: " + str(saved_items_bu))
    print("Weight: " + str(total_weight_bu))
    print("Benefit equals to items benefit?: " + str(items_benefit_bu))

    print("\nTop-down")
    print("The max benefit is: " + str(max_benefit_td))
    print("With the items: " + str(saved_items_td))
    print("Weight: " + str(total_weight_td))
    print("Benefit equals to items benefit?: " + str(items_benefit_td))

def calculate_benefit(items, benefit):
    """ Makes sure that the total benefit of the selected items equals to the benefit calculated
        I: items selected
        O: True if the benefit of the items equal to the benefit, false if not
    """
    items_benefit = 0
    for _, v in items:
        items_benefit += v[1]
    
    return items_benefit == benefit

def main(args):
    """ Function that executes the program and receives the arguments
        I: the arguments given in the console
        O: N/A
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
    print("Benefit equals to items benefit?: " + str(calculate_benefit(saved_items, max_benefit)))

    return 0

main(sys.argv)