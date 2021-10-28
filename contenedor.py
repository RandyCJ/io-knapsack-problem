import sys 
from sympy import Rational
from random import randrange
import copy

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

        This is a brute force algorithm adaptation from Maya Hristakeva and Dipti Shrestha
        http://www.micsymposium.org/mics_2005/papers/paper102.pdf
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

        This is a bottom_up algorithm adaptation from Bhavya Jain
        https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/
    """
    wt = []
    val =[]
    for i in items:
        wt.append(i[0])
        val.append(i[1])
    

    K = [[0 for x in range(knapsack_weight + 1)] for x in range(len(items) + 1)]
    
    best_items = []
    best_weight = []

    # Build table K[][] in bottom up manner
    for i in range(len(items) + 1):
        for w in range(knapsack_weight + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i-1]
                          + K[i-1][w-wt[i-1]], 
                              K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
    best_benefit = K[len(items)][knapsack_weight]
    
    #Find the items entered in the backpack (bottom_up)
    best_weight, best_items = find_items(K, items, knapsack_weight)
    
    return [best_benefit, best_items, best_weight]

def top_down(knapsack_weight, items):
    """ Function that solves the knapsack problem with top-down
            E: the knapsack weight and the items
            S: the max benefit, the items stored in the knapsack and the total 
            weight of those items
    """
    tmp = [[-1 for i in range(knapsack_weight + 1)] for j in range(len(items))]
    return top_down_recursive(tmp, knapsack_weight, items, 0)


def top_down_recursive(matrix, knapsack_weight, items, ind):

    if knapsack_weight <= 0 or ind >= len(items):
        return 0

    if matrix[ind][knapsack_weight] != -1:
        return matrix[ind][knapsack_weight]

    profit1 = 0
    if items[ind][0] <= knapsack_weight:
        profit1 = items[ind][1] + top_down_recursive(matrix, knapsack_weight - items[ind][0], items, ind + 1)

    # recursive call after excluding the element at the currentIndex
    profit2 = top_down_recursive(matrix, knapsack_weight, items, ind + 1)

    matrix[ind][knapsack_weight] = max(profit1, profit2)
    return matrix[ind][knapsack_weight]

def find_items(matrix, items, knapsack_weight):
    """ Gets stored knapsack items from matrix 
            E: A matrix from bottom-up or top-down, the items and the knapsack weight
            S: The weight and the items in the knapsack
    """
    items.reverse()
    best_items = []
    current_knapsack_weight = 0
    i = 0
    while i < len(items):
        if matrix[-1][-1] not in matrix[-2] and i == 0:
            best_items.append((len(matrix)-1,(items[i])))
            current_knapsack_weight = items[i][0]
            previous_benefit = matrix[-1][-1]
            matrix.pop(-1)
            
        elif (previous_benefit - items[i-1][1]) not in matrix[-2] and knapsack_weight > (current_knapsack_weight + items[i][0]):
            best_items.append((len(matrix)-1,(items[i])))
            previous_benefit = previous_benefit - items[i-1][1]
            current_knapsack_weight = current_knapsack_weight + items[i][0]
            matrix.pop(-1)
        
        else:
            matrix.pop(-1)

        i += 1
    
    best_weight = current_knapsack_weight
    best_items.sort()

    return [best_weight, best_items]

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
        print("Please read the file 'README.MD' to learn how to execute the program")
        quit()

    print("Algorithm: " + str(algorithm))
    print("Iterations: " + str(iterations))
    print("Knapsack weight: " + str(knapsack_weight))
    print("Items: " + str(items))

    if algorithm == 1:
        max_benefit, saved_items, total_weight = brute_force(knapsack_weight, items)
    elif algorithm == 2:
        #bottom_up
        max_benefit, saved_items, total_weight = bottom_up(knapsack_weight,items) 
        pass
    else:
        #top-down
        print(top_down(knapsack_weight, items))
        quit()
        max_benefit, saved_items, total_weight = top_down(knapsack_weight,items) 
        pass

    print("The max benefit is: " + str(max_benefit))
    print("With the items: " + str(saved_items))
    print("For the weight of: " + str(total_weight))

    return 0

main(sys.argv)