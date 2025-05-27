####### TASK - 1 #######  

import random
tree_lst = []
counter = 0
while counter < 32:
    if counter % 2 == 0:
        tree_lst.append(random.choices([-1,1]))
    else:
        tree_lst.append(random.choices([-1,1]))     
    counter += 1
# print(tree_lst)  
 
def alpha_beta_pruning(initial_position, depth, alpha, beta, player):
    # global tree
    if depth == 3:    #last node
        return tree_lst[initial_position][0]
    if player:
        max_result_alpha = float('-inf')
        counter = 0
        while counter < 2:  
            outcome_1 = alpha_beta_pruning(initial_position * 2 + counter, depth-1, alpha, beta, False)
            max_result_alpha = max(max_result_alpha, outcome_1)
            alpha = max(alpha, max_result_alpha)
            if alpha >= beta:
                break
            counter += 1
            # print(max_result_alpha)    
        return max_result_alpha    
    
    else:  #flag = False 
        min_result_beta = float('inf')
        counter = 0
        while counter < 2:
            outcome_1 = alpha_beta_pruning(initial_position * 2 + counter, depth-1, alpha, beta, True)
            min_result_beta = min(min_result_beta, outcome_1)
            beta = min(beta, min_result_beta)
            if alpha >= beta:
                break
            counter += 1
        return min_result_beta  
def game_algorithm(input):
    player = input
    round_lst = []
    scorpion_result = 0
    subzero_result = 0
    fixed_round = 3
    completed_round = 1
    
    for i in range(fixed_round):
        result = alpha_beta_pruning(0, 5, float('-inf'), float('inf'), player)
        if result == 1:   #subzero
            subzero_result += 1
            round_lst.append('sub-zero')
            if round_lst.count('sub-zero') == 2:
                break
        
        else:   #scorpion
            scorpion_result += 1
            round_lst.append('scorpion')
            if round_lst.count('scorpion') == 2:
                break
        
        player = 1 - player
        completed_round += 1
    
    if scorpion_result > subzero_result:
        winner = "scorpion"
    else:
        winner = 'subzero'
    return winner, completed_round, round_lst                    
            


# -1 if scorpion wins --> minimizing
# 1 if sub-zero wins  --> maximizing


first_input = int(input("Enter 0 for Scorpion or 1 for Sub-zero: "))
game_winner, round_played, each_round = game_algorithm(first_input) 
# branching_factor = 2
# depth = 5
# print(each_round)
print(f"Game Winner: {game_winner}\n")
print(f"Total Rounds Played:{round_played}\n")

for i in range(len(each_round)):
    print(f"Winner of Round {i+1}:{each_round[i]}")    
    
### OUTPUT OF TASK 1 -->    
#     Game Winner: scorpion

#     Total Rounds Played:3

#     Winner of Round 1:scorpion
#     Winner of Round 2:sub-zero
#     Winner of Round 3:scorpion
    
    
####### TASK - 2 #######  

# def alpha_beta_pruning_pacman(make_tree, depth, alpha, beta, maximize):

#     if depth == 0:    #last node
#         return make_tree
    
#     if maximize: #flag = True
#         max_result_alpha = float('-inf')
#         for i in make_tree:  
#             outcome_1 = alpha_beta_pruning_pacman(i, depth-1, alpha, beta, False)
#             max_result_alpha = max(max_result_alpha, outcome_1)
#             alpha = max(alpha, outcome_1)    
#             if alpha >= beta:
#                 break   
#         return max_result_alpha    
    
#     else:  #flag = False 
#         min_result_beta = float('inf')
#         for i in make_tree: 
#             outcome_2 = alpha_beta_pruning_pacman(i, depth-1, alpha, beta, True)
#             min_result_beta = min(min_result_beta, outcome_2)
#             beta = min(beta, outcome_2)
#             if alpha >= beta:
#                 break
#         return min_result_beta  
    
# def tree(leaf):
#     branch_lst1 = [] #right side
#     branch_lst2 = [] #left side
#     branch = []
#     branch1 = leaf[0:2]
#     branch2 = leaf[2:4]
#     branch3 = leaf[4:6]
#     branch4 = leaf[6:8]
#     branch_lst1.append(branch1)
#     branch_lst1.append(branch2)
#     branch_lst2.append(branch3)
#     branch_lst2.append(branch4)
#     branch.append(branch_lst1)
#     branch.append(branch_lst2)
#     # print(branch)
#     return branch 
    
# def pacman(input_c):
#     leaf = [3, 6, 2, 3, 7, 1, 2, 0]     
#     make_tree = tree(leaf)
#     # print(make_tree)
#     alpha_beta_pruning_value = alpha_beta_pruning_pacman(make_tree, 3, float('-inf'), float('inf'), True)
#     left = max(leaf[:4]) - input_c #6-5=1
#     right = max(leaf[4:]) - input_c #7-5 =2
#     print(alpha_beta_pruning_value) #3
#     if left > alpha_beta_pruning_value or right > alpha_beta_pruning_value:
#         if left > right:
#             print(f"The new minimax value is {left}. Pacman goes right and uses dark magic.")
#         else: #4<5
#             print(f"The new minimax value is {right}. Pacman goes right and uses dark magic.")
#     else:
#         print(f"The minimax value is {alpha_beta_pruning_value}. Pacman does not use dark magic.")

# input_c = int(input("Dark magic cost: "))
# pacman(input_c)           


### OUTPUT OF TASK 2 -->
# Dark magic cost: 2
# The new minimax value is 5. Pacman goes right and uses dark magic.