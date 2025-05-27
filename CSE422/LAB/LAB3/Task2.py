def alpha_beta_pruning_pacman(make_tree, depth, alpha, beta, maximize):

    if depth == 0:    #last node
        return make_tree
    
    if maximize: #flag = True
        max_result_alpha = float('-inf')  #alpha
        for i in make_tree:  
            outcome_1 = alpha_beta_pruning_pacman(i, depth-1, alpha, beta, False)
            max_result_alpha = max(max_result_alpha, outcome_1)
            alpha = max(alpha, outcome_1)    
            if alpha >= beta:
                break   
        return max_result_alpha    
    
    else:  #flag = False 
        min_result_beta = float('inf')   #beta
        for i in make_tree: 
            outcome_2 = alpha_beta_pruning_pacman(i, depth-1, alpha, beta, True)
            min_result_beta = min(min_result_beta, outcome_2)
            beta = min(beta, outcome_2)
            if alpha >= beta:
                break
        return min_result_beta  
    
def tree(leaf):
    branch_lst1 = [] #left side
    branch_lst2 = [] #right side
    branch = []
    #for left
    branch1 = leaf[0:2]
    branch2 = leaf[2:4]
    #for right
    branch3 = leaf[4:6]
    branch4 = leaf[6:8]
    
    branch_lst1.append(branch1)
    branch_lst1.append(branch2)
    branch_lst2.append(branch3)
    branch_lst2.append(branch4)
    branch.append(branch_lst1)
    branch.append(branch_lst2) #2ta branch under one list 
    # print(branch)
    # [[[3, 6], [2, 3]], [[7, 1], [2, 0]]]
    return branch 
    
def pacman(input_c):
    leaf = [3, 6, 2, 3, 7, 1, 2, 0]     
    make_tree = tree(leaf)
    # print(make_tree)
    alpha_beta_pruning_value = alpha_beta_pruning_pacman(make_tree, 3, float('-inf'), float('inf'), True)
    left = max(leaf[:4]) - input_c #6-5=1
    right = max(leaf[4:]) - input_c #7-5 =2
    print(alpha_beta_pruning_value) #3
    if left > alpha_beta_pruning_value or right > alpha_beta_pruning_value:
        if left > right:
            print(f"The new minimax value is {left}. Pacman goes right and uses dark magic.")
        else:    #4<5
            print(f"The new minimax value is {right}. Pacman goes right and uses dark magic.")
    else:
        print(f"The minimax value is {alpha_beta_pruning_value}. Pacman does not use dark magic.")

input_c = int(input("Dark magic cost: "))
pacman(input_c)           