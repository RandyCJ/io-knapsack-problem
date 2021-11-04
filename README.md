# io-knapsack-problem

Example of a file:  
Given a knapsack with weight = 30  
5 items with weights: 5, 15, 10, 10, 8  
Benefits of: 20, 50, 60, 62, 40  
The txt file has to be like

```
30  
5,20  
15,20  
10,60  
10,62  
8,40  
```

Dependencies: `pip install -r requirements.txt`

Execution example with a file:
    
  `python contenedor.py algorithm -a file.txt iterations`

  - `algorithm` is an integer where; 1 = Brute Force; 2 = DP Bottom-Up; 3 = DP Top-Down; 4 = All of them
  - `-a file.txt` is a file path with the problem
  - `iterations` is the number of times the program will be executed in order to measure the average time


Execution example with parameters to automatically generate a problem:

  `python contenedor.py algorithm -p W N weightsRange  benefitsRange iterations`
  
  - `algorithm` is an integer where; 1 = Brute Force; 2 = DP Bottom-Up; 3 = DP Top-Down
  - `W` knapsack weight
  - `N` number of items
  - `weightsRange` range of values for the item's weights
  - `benefitsRange` range of values for the item's benefits
  - `iterations` is the number of times the program will be executed in order to measure the average time
  - The ranges must be given in the form `Min-Man`; example: `7-25`

