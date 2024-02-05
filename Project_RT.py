import random as rnd
import numpy as np

def tic_tac_toe(board):
    for i in range(3):
        if(board[i]==board[i+3] == board[i+6] and board[i] !='n'): #column victorys
            return True
        if(board[3*i] == board[3*i+1] == board[3*i+2] and board[3*i] !='n'): #row victorys
            return True
    if(((board[0] == board[4] == board[8]) or (board[2] == board[4]  == board[6])) and board[4] !='n'): #diagonal victorys
        return True
    return False

def print_board(board):
    '''prints the current board layout in 3x3 grid'''
    c=0
    for i in range(3):
        print(f'{board[c]},{board[c+1]},{board[c+2]}') #print 3 values on one line
        c+=3 #c moves to next row of board

def board_state(board):
    '''get number of occupied spaces on board'''
    cnt=0
    for n in board:
        if(n !='n'):
            cnt+=1
    return cnt

def minimax(board,depth,isMaxing):
    '''minimax function'''
    bestmove=-1
    if tic_tac_toe(board)==True: #base case #1: tic tac toe has been reached on either players turn
        if(isMaxing): #ttt is for human player
            return (-10+depth),0
        else: #ttt is for AI player
            return (10-depth),0
    if(board_state(board)==9): #base case #2: game has tied
        return 0,0
    
    if(isMaxing):
        score=-np.inf
    else:
        score=np.inf
    for i in range(len(board)):
        if(board[i] == 'n'):
            if(isMaxing): #AI 'turn'
                board[i]='o' #try move for ai
                # print('AI max at depth %d'%depth)
                # print(f'replacing pos {i+1} with an o')
                # print_board(board)
                newscore,_=minimax(board,depth+1,False) #run minimax with goal to min score
                if(newscore>score):#new turn is better for ai than previous score
                    # print(f'new score of {newscore} replacing {score} for maxscore at depth {depth}')

                    score=newscore
                    bestmove=i
                board[i]='n' #clear option
                

            else:
                board[i]='x' #try move for opponent
                # print('player min at depth %d'%depth)
                # print(f'replacing pos {i+1} with an x')
                # print_board(board)
                newscore,_=minimax(board,depth+1,True) #run minimax with goal to max score
                if(newscore <score):#new turn is better for opponent than previous score
                    # print(f'new score of {newscore} replacing {score} for minscore at depth {depth}')
                    score=newscore
                    bestmove=i
                board[i]='n' #clear option
    return score,bestmove



def minimax_abp(board,depth,isMaxing,alpha,beta):
    '''minimax function including alpha beta pruning'''
    bestmove=-1
    if tic_tac_toe(board)==True: #base case #1: tic tac toe has been reached on either players turn
        if(isMaxing): #ttt is for human player
            return (-10+depth),0
        else: #ttt is for AI player
            return (10-depth),0
    if(board_state(board)==9): #base case #2: game has tied
        return 0,0
    
    if(isMaxing):
        score=-np.inf
    else:
        score=np.inf
    for i in range(len(board)):
        if(board[i] == 'n'):
            if(isMaxing): #AI 'turn'
                board[i]='o' #try move for ai
                # print('AI max at depth %d'%depth)
                # print(f'replacing pos {i+1} with an o')
                # print_board(board)
                newscore,_=minimax_abp(board,depth+1,False,alpha,beta) #run minimax with goal to min score
                board[i]='n' #clear option
                if(newscore>score):#new turn is better for ai than previous score
                    # print(f'new score of {newscore} replacing {score} for maxscore at depth {depth}')
                    score=newscore
                    bestmove=i

                if(score>alpha):
                    alpha=score
                if(beta<=alpha):
                    break
                
                

            else:
                board[i]='x' #try move for opponent
                # print('player min at depth %d'%depth)
                # print(f'replacing pos {i+1} with an x')
                # print_board(board)
                newscore,_=minimax_abp(board,depth+1,True,alpha,beta) #run minimax with goal to max score
                board[i]='n' #clear option
                if(newscore <score):#new turn is better for opponent than previous score
                    # print(f'new score of {newscore} replacing {score} for minscore at depth {depth}')
                    score=newscore
                    bestmove=i
                if score < beta:
                    beta=score
                if beta <=alpha:
                    break
                
    return score,bestmove
    


board=['n','n','n','n','n','n','n','n','n'] #default blank board
# board=['o','x','o','x','n','o','n','n','n'] #example board for testing, always start by typing 5, ai should pick 9


game_won=False
rnd.seed()
move=rnd.randint(0,1) #choose a random person to start
algo_choice=False
while algo_choice==False:
    try:
        algo_type=int(input('type 0 for standard minimax algorithm or 1 for alpha-beta pruning algorithm: '))
    except:
        print('please enter a number')
    if algo_type==0 or algo_type==1:
        algo_choice=True

if(algo_type==0):
    print('using standard algorithm')
else:
    print('using ABP algorithm')




while(not game_won):
    print_board(board)
    player_moved=False
    if(move %2 ==0): #human turn
        turn="Human"
        print('Human\'s Turn')
        while(not player_moved):
            try:
                pm=int(input('type -1 to quit or \nenter a number from 1 to 9 to replace an n with an x: '))
            except:
                print('please enter a number')
                continue
            if pm==-1:
                game_won=True
                break
            elif(pm<1 or pm>9):
                print('number is not in range, please enter a different number')
            elif(board[pm-1] != 'n'):
                print(f'space {pm} is already taken, pick a new location')
            else:
                board[pm-1]='x'
                player_moved=True
                move+=1
    else: #ai turn
        turn="Ai"
        print('AI\'s turn')
        if algo_type==0:
            bestscore,bestmove=minimax(board,-1,True)
        else:
            bestscore,bestmove=minimax_abp(board,-1,True,-np.inf,np.inf)
        print(f'best move at postion {bestmove+1} with a score of {bestscore}')
        board[bestmove]='o'
        move+=1
    if(tic_tac_toe(board)==True):
        if(turn=="Human"):
            print("Human wins!")
        
        elif turn=='Ai':
            print('Ai wins!')
        game_won=True
        break
    if(board_state(board)==9):
        print('tie game')
        game_won=True

print_board(board)
print('game over')
    
