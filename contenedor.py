import sys 
import copy
import numpy as np
from sympy import Rational
from random import randrange
import matplotlib.pyplot as plt
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

def find_items(matrix, items):
    """ Gets stored knapsack items from matrix 
        I: A matrix from bottom-up, the items and the knapsack weight
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

def top_down(knapsack_weight, items):
    """ Main function of top down algorithm
        I: the knapsack weight and the items
        O: the max benefit, the items stored in the knapsack and the total 
            weight of those items
    """
    memoization_dict = {}
    max_benefit, index_selected_items = top_down_recursive(knapsack_weight, items, 0, memoization_dict)
    weight = 0
    best_items = []
    for index in index_selected_items:
        best_items.append((index+1, items[index]))
        weight += items[index][0]
    best_items.reverse()
    return [max_benefit, best_items, weight]

def top_down_recursive(knapsack_weight, items, ind, mem_dict):
    """ Function that solves the knapsack problem with top-down recursive
        I: The knapsack weight, the items, index of an item and a memoization dictionary
        O: The best benefit and the index of the items stored in the knapsack
    """
    #Base case
    if ind >= len(items) or knapsack_weight <= 0:
        return [0, []]

    #Memoization key
    key = (ind, knapsack_weight)

    #If the key is in dict, no calculation is needed
    if key in mem_dict.keys():
        return mem_dict[key]

    profit1 = -1 #in case the item is not included
    if knapsack_weight >= items[ind][0]:#If the item can be included
        tmp = top_down_recursive(knapsack_weight-items[ind][0], items, ind+1, mem_dict)
        profit1 = items[ind][1] + tmp[0]
        items1 = tmp[1]

    #Benefit of not including the item
    profit2, items2 = top_down_recursive(knapsack_weight, items, ind+1, mem_dict)

    if profit1 >= profit2:
        profit = profit1
        selected_items = copy.deepcopy(items1)
        selected_items.append(ind)#appending the current item index
    else:
        profit = profit2
        selected_items = copy.deepcopy(items2)
    
    #Saving in the dict
    mem_dict[key] = [profit, selected_items]
    return [profit, selected_items]

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

def get_bar_chart(knapsack_weight, items, iterations):
    averages = []
    algorithms = ["Brute Force", "Bottom-up", "Top-down"]

    averages.append(perform_iterations(iterations, 1, knapsack_weight, items))
    averages.append(perform_iterations(iterations, 2, knapsack_weight, items))
    averages.append(perform_iterations(iterations, 3, knapsack_weight, items))

    print("test averages: " + str(averages))

    x = np.arange(3)
    width = 0.35
    fig, ax = plt.subplots()
    ax.set_ylabel("Average time (seconds)")
    ax.set_title("Avegare time per algorithm")
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms)

    pps = ax.bar(x - width/2, averages, width, label='Average time')
    for p in pps:
        height = p.get_height()
        ax.annotate('{}'.format(height),
        xy=(p.get_x() + p.get_width() / 2, height),
        xytext=(0, 3), # 3 points vertical offset
        textcoords="offset points",
        ha='center', va='bottom')

    plt.show()

def average_time():
    """ Calculates the average time of the three algorithms
        I: N/A
        O: N/A
    """

    #First Test
    print("First", end=" ")
    knapsack_weight = 100
    number_of_items = 5
    weight_range = [40, 55]
    benefit_range = [45, 70]
    iterations = 100
    items = generate_items(number_of_items, weight_range, benefit_range)
    get_bar_chart(knapsack_weight, items, iterations)

    #Second Test
    print("Second", end=" ")
    knapsack_weight = 500
    number_of_items = 10
    weight_range = [100, 200]
    benefit_range = [45, 70]
    iterations = 100
    items = generate_items(number_of_items, weight_range, benefit_range)
    get_bar_chart(knapsack_weight, items, iterations)

    #Third Test
    print("Third", end=" ")
    knapsack_weight = 1000
    number_of_items = 15
    weight_range = [90, 150]
    benefit_range = [45, 70]
    iterations = 20
    items = generate_items(number_of_items, weight_range, benefit_range)
    get_bar_chart(knapsack_weight, items, iterations)

    #Fourth Test
    print("Fourth", end=" ")
    knapsack_weight = 200
    number_of_items = 20
    weight_range = [30, 55]
    benefit_range = [45, 70]
    iterations = 2
    items = generate_items(number_of_items, weight_range, benefit_range)
    get_bar_chart(knapsack_weight, items, iterations)

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