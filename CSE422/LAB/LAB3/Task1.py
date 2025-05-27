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
print(tree_lst)  

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