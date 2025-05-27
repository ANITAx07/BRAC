# TASK - 1

import random

def crossover(p1, p2, n, t):
    length = n * t
    point = random.randrange(1, length-1)
    part1_of_p1 = p1[:point]
    part2_of_p1 = p1[point:]
    
    part1_of_p2 = p2[:point]
    part2_of_p2 = p2[point:]
    
    child1 = part1_of_p1 + part2_of_p2
    child2 = part2_of_p1 + part1_of_p2 
    return child1, child2

def mutation(child, n, t):  #child = time schedule
    length = n * t
    index = random.randint(0, length-1)
    time_schedule_list = list(child)
    if time_schedule_list[index] == "1":
        time_schedule_list[index] = "0"
    else:
        time_schedule_list[index] = "1" 
    mutated_list = ''.join(time_schedule_list)
    # print(mutated_list)
    return mutated_list     
    
def overlap(time, n, t): #101 011 111
    overlap_penalty_count = 0
    for i in range(t): #3
        slot = time[i*n:(i+1)*n]  #101 
        course = 0
        for i in slot:
            if i == "1":
                course += 1
        if course > 1:
            overlap_penalty_count += course - 1  #2-1=1
    return overlap_penalty_count                
        
            
def consistency(time, n, t):  #101 011 111
    consistency_penalty_count = 0
    # print(len(time))
    for i in range(n): #1
        course_sch = 0
        for j in range(t): #2
            index = j *n + i  #index=0,1,2
            course_sch += int(time[index]) # +1+0+1=2 / +0+1+1=2
        if course_sch != 1:
            consistency_penalty_count += abs(course_sch - 1)  #2-1 + 1-1 +3-1 
    return consistency_penalty_count             
            
def fitness_check(time, n, t): #101011111
    calculate_overlap = overlap(time, n, t)
    calculate_consistency = consistency(time, n, t)
    total = - (calculate_overlap + calculate_consistency)
    return total
    
def choose_parent(select, n, t):  #n=course no , t= time, main=schedule
    var = sorted(select)
    # print(var)
    p1 = var[0][1]
    p2 = var[1][1]
    
    # p1 = random.choice(main_population)
    # p2 = random.choice(main_population)
    return p1, p2

def create_population(n, t, size):  #size =5
    population_lst = []
    population_size = size
    for i in range(population_size):
        lst = []
        length = n*t  #9
        for j in range(length):
            lst.append(random.choice('10'))
        # print(lst)
        population_lst.append(''.join(lst))
    print(population_lst) 
    #['100101010', '101011111', '110111100', '001001001', '000010111']    
    
    return population_lst        

# function for TASK - 2
def two_point_crossover(parent1, parent2, n, t):
    # print(parent1)
    # print(parent2)
    cross1 = parent1[:3] + parent2[3:7] + parent1[7:]
    cross2 = parent2[:3] + parent1[3:7] + parent2[7:]
    # print(child_1)
    # print(child_2)
    return cross1, cross2        
        
def genetic_algorithm(n, t, size, iteration):
    main_population = create_population(n, t, size)
    # print(main_population)
    
    #for task 2
    parent1, parent2 = random.choice(main_population), random.choice(main_population)
    # print(parent1)
    # print(parent2)
    cross1, cross2 = two_point_crossover(parent1, parent2, n, t)
    
    select = []
    for i in main_population:
        a = fitness_check(i, n, t)
        select.append((a,i))
    # print(select) 
    
    for i in range(iteration): #int val, everytime 2ta kore
        new = []
        for j in range(size//2):
            p1, p2 = choose_parent(select, n, t)
            # print(p1)
            crossed_child_1, crossed_child_2 = crossover(p1, p2, n, t)
            mutation_of_child1 = mutation(crossed_child_1, n, t)
            new.append(mutation_of_child1)
            mutation_of_child2 = mutation(crossed_child_2, n, t)
            new.append(mutation_of_child2)
        main_population = new
        # print(main_population)
        fitness_list = []
        for i in main_population:
            func_call = fitness_check(i, n, t)
            fitness_list.append(func_call)    
        max_fitness = max(fitness_list)    
        schedule_index = fitness_list.index(max_fitness)
        schedule = main_population[schedule_index]
        
        if max(fitness_list) == 0:
            break
    return schedule, max(fitness_list), cross1, cross2 

input = open('E:\CSE422\LAB\LAB2\input.txt', 'r')
output = open('E:\CSE422\LAB\LAB2\output.txt', 'w')
lst = []
a = input.readline().strip()
temp_lst = a.split(" ")
n = int(temp_lst[0])
t = int(temp_lst[1])
# print(n)
for i in range(n):
    temp = input.readline().strip()
    lst.append(temp)
print(lst)   
size = 5
iteration = 5
if t < n:
    output.write("n should be less than t")
else:    
    penalty, fitness, cross1, cross2  = genetic_algorithm(n, t, size, iteration)
    #output of task1
    output.write(f"Schedule: {penalty}\n")
    output.write(str(fitness))
    
    #output of task2   (only this one)
    # output.write(f"{cross1}\n")
    # output.write(cross2)

## OUTPUT task-1
# Schedule: 100101001
# -4 

## OUTPUT task-2
# parent1 - 100111011
# parent2 - 010000010
# cross1 - 100000011
# cross2 - 010111010
