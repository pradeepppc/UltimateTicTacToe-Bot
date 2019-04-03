from time import time
import random


class Team62:

    def __init__(self):
        # initial depth or default depth
        self.depth = 4
        self.player_num = ''
        self.opp = ''
        self.timeLimit = 14
        self.maxvalue = 10000000000
        self.start_time = 0
        self.to_break = False
        self.block_weights = [pow(20, 3), pow(20, 4), pow(20, 5), pow(20, 6)]
        self.board_weights = [pow(20, 0), pow(20, 1), pow(20, 2), pow(20, 3)]
        #self.draw_weights = [pow(20, 3) / 6, pow(20, 3) / 9, pow(20, 3) / 12]
        # self.openmove_weight = pow(20,3)/4
        #
        # self.bonuscount=0
        # self.bonusweight= pow(20,4)/2

    # move function for the simulator to call
    def move(self, board, old_move, flag):

        # To know if player is 'x' (player 1) or 'o' (player2)
        if flag == 'x':
            self.player_num = 'x'
            self.opp = 'o'
        elif flag == 'o':
            self.player_num = 'o'
            self.opp = 'x'

        # now iterate through all possible states upto some depth given checking the time

        self.start_time = time()
        self.to_break=False
        time_elapsed = 0
        self.depth = 4
        depth = self.depth
        possible_moves = board.find_valid_move_cells(old_move)
        action = possible_moves[random.randrange(len(possible_moves))]
        # loop until time exceeds
        main_action = action
        while time_elapsed < self.timeLimit:
            # iterative deepening
            action = self.ids(board, old_move, depth)
            if self.to_break:
                break
            else:
                main_action = action
            depth += 1
            time_elapsed = time() - self.start_time

        return main_action

    def ids(self, board, old_move, depth):
        possible_moves = board.find_valid_move_cells(old_move)
        max_val = -self.maxvalue
        action_index = []
        alpha = -self.maxvalue
        beta = self.maxvalue
        #tempbonuscount=self.bonuscount
        for moves in possible_moves:
            #self.bonuscount=tempbonuscount
            next_move = moves
            board.update(old_move, next_move, self.player_num)
            # if board.block_status[next_move[0]/4][next_move[1]/4]!='-' :
            #     if self.bonuscount==0:
            #         self.bonuscount=1
            #         val = self.min_max(board, next_move, self.player_num, depth - 1, alpha, beta)
            #     else:
            #         val = self.min_max(board, next_move, self.opp, depth - 1, alpha, beta)
            #         self.bonuscount=0
            # else:
            #     self.bonuscount = 0
            val = self.min_max(board, next_move, self.opp, depth-1, alpha,beta)
            # change the board again to the original shape
            board.board_status[next_move[0]][next_move[1]] = '-'
            board.block_status[next_move[0] / 4][next_move[1] / 4] = '-'

            if val > max_val:
                max_val = val
                action_index = [moves]
            elif val == max_val:
                action_index.append(moves)
            # this condition is kept after the loop so that at least one condition holds
            if self.to_break:
                break

        return random.choice(action_index)

    def min_max(self, board, old_move, flag, depth, alpha, beta):

        # check if it is a terminal node or the depth becomes zero
        if depth == 0 or board.find_terminal_state() !=('CONTINUE', '-'):
            return self.heuristic(board,old_move,flag)

        # check if it got exceeded the given time limit
        if time() - self.start_time > self.timeLimit:
            self.to_break = True
            return 1
        if flag == self.player_num:
            max_value = -self.maxvalue
            moves = board.find_valid_move_cells(old_move)
            if len(moves) == 0:
                return self.heuristic(board,old_move,flag)
            #tempbonuscount=self.bonuscount
            for move in moves:
                self.bonuscount=tempbonuscount
                if self.to_break:
                    return 1

                next_move = move
                board.update(old_move,next_move,self.player_num)
                # openmove = board.block_status[old_move[0] % 4][old_move[1] % 4] != '-'
                # if board.block_status[next_move[0] / 4][next_move[1] / 4] != '-':
                #     if self.bonuscount == 0:
                #         self.bonuscount = 1
                #         val = self.min_max(board, next_move, self.player_num, depth - 1, alpha, beta)
                #     else:
                #         self.bonuscount = 0
                #         val = self.min_max(board, next_move, self.opp, depth - 1, alpha, beta)
                # else:
                #     self.bonuscount = 0
                val = self.min_max(board, next_move, self.opp, depth - 1, alpha, beta)
                # if openmove:
                #     val += self.openmove_weight
                board.board_status[next_move[0]][next_move[1]] = '-'
                board.block_status[next_move[0] / 4][next_move[1] / 4] = '-'
                max_value = max(max_value, val)
                alpha = max(alpha,max_value)
                # alpha beta pruning
                if beta <= alpha:
                    break

            return max_value

        elif flag == self.opp:
            min_value = self.maxvalue
            moves = board.find_valid_move_cells(old_move)
            if len(moves) == 0:
                return self.heuristic(board,old_move,flag)
            #tempbonuscount=self.bonuscount
            for move in moves:
                #self.bonuscount=tempbonuscount
                if self.to_break:
                    return 1

                next_move = move
                board.update(old_move, next_move, self.opp)
                # openmove = board.block_status[old_move[0] % 4][old_move[1] % 4] != '-'
                # if board.block_status[next_move[0] / 4][next_move[1] / 4] != '-':
                #     if self.bonuscount == 0:
                #         self.bonuscount = 1
                #         val = self.min_max(board, next_move, self.player_num, depth - 1, alpha, beta)
                #     else:
                #         self.bonuscount = 0
                #         val = self.min_max(board, next_move, self.opp, depth - 1, alpha, beta)
                # else:
                #     self.bonuscount=0
                val = self.min_max(board,next_move,self.opp,depth-1,alpha,beta)
                # if openmove:
                #     val-=self.openmove_weight + self.bonuscount*self.bonusweight
                board.board_status[next_move[0]][next_move[1]] = '-'
                board.block_status[next_move[0] / 4][next_move[1] / 4] = '-'
                min_value = min(min_value,val)
                beta = min(beta , min_value)
                # alpha beta pruning
                if beta <= alpha:
                    break

            return min_value



    def heuristic(self, board, old_move, flags):
        flag = self.player_num

        #openmove
        #openmove = board.block_status[old_move[0]%4][old_move[1]%4] != '-'

        # block_corner_win block_corner_lost
        # block_edge_win block_edge_lost
        # block_center_win block_center_lost
        block_center_win = block_edge_win = block_corner_win = 0
        for i in range(4):
            for j in range(4):
                if board.block_status[i][j] == flag:
                    if (i == 3 or i == 0) and (j == 0 or j == 3):
                        block_corner_win += 1
                    elif i == 0 or j == 0 or i == 3 or j == 3:
                        block_edge_win += 1
                    else:
                        block_center_win += 1
                elif board.block_status[i][j] == chr(ord('x') + ord('o') - ord(flag)):
                    if (i == 3 or i == 0) and (j == 0 or j == 3):
                        block_corner_win -= 1
                    elif i == 0 or j == 0 or i == 3 or j == 3:
                        block_edge_win -= 1
                    else:
                        block_center_win -= 1

        # block4_win block3_win block2_win block1_win
        block_win = [0, 0, 0, 0]
        # for i in range(4):
        #     if board.block_status[i][0]==flag and board.block_status[i][1]==flag and board.block_status[i][2]==flag and board.block_status[i][3]==flag:
        #         block_win[3]+=1
        #     elif board.block_status[0][i]==flag and board.block_status[1][i]==flag and board.block_status[2][i]==flag and board.block_status[3][i]==flag:
        #         block_win[3]+=1
        #     elif board.block_status[i][0]==chr(ord('x')+ord('o')-ord(flag)) and board.block_status[i][1]==chr(ord('x')+ord('o')-ord(flag)) and board.block_status[i][2]==chr(ord('x')+ord('o')-ord(flag)) and board.block_status[i][3]==chr(ord('x')+ord('o')-ord(flag)):
        #         block_win[3]-=1
        #     elif board.block_status[0][i]==chr(ord('x')+ord('o')-ord(flag)) and board.block_status[1][i]==chr(ord('x')+ord('o')-ord(flag)) and board.block_status[2][i]==chr(ord('x')+ord('o')-ord(flag)) and board.block_status[3][i]==chr(ord('x')+ord('o')-ord(flag)):
        #         block_win[3]-=1

        for i in range(4):
            countp = counto = 0
            for j in range(4):
                if board.block_status[i][j] == flag:
                    countp += 1
                    counto = -4
                elif board.block_status[i][j] == chr(ord('x') + ord('o') - ord(flag)):
                    countp = -4
                    counto += 1
            for j in range(1, 5):
                if j == countp:
                    block_win[j - 1] += 1
                elif j == counto:
                    block_win[j - 1] -= 1
        for j in range(4):
            countp = counto = 0
            for i in range(4):
                if board.block_status[i][j] == flag:
                    countp += 1
                    counto = -4
                elif board.block_status[i][j] == chr(ord('x') + ord('o') - ord(flag)):
                    countp = -4
                    counto += 1
            for i in range(1, 5):
                if i == countp:
                    block_win[i - 1] += 1
                elif i == counto:
                    block_win[i - 1] -= 1
        # diamond
        # take each top of the diamond
        for i in range(2):
            for j in range(1, 3):
                countp = counto = 0
                if board.block_status[i][j] == flag:
                    countp += 1
                    counto = -4
                elif board.block_status[i][j] == chr(ord('x') + ord('o') - ord(flag)):
                    countp = -4
                    counto += 1

                if board.block_status[i + 1][j - 1] == flag:
                    countp += 1
                    counto = -4
                elif board.block_status[i + 1][j - 1] == chr(ord('x') + ord('o') - ord(flag)):
                    countp = -4
                    counto += 1

                if board.block_status[i + 1][j + 1] == flag:
                    countp += 1
                    counto = -4
                elif board.block_status[i + 1][j + 1] == chr(ord('x') + ord('o') - ord(flag)):
                    countp = -4
                    counto += 1

                if board.block_status[i + 2][j] == flag:
                    countp += 1
                    counto = -4
                elif board.block_status[i + 2][j] == chr(ord('x') + ord('o') - ord(flag)):
                    countp = -4
                    counto += 1

                for k in range(1, 5):
                    if k == countp:
                        block_win[k - 1] += 1
                    elif k == counto:
                        block_win[k - 1] -= 1

        # smallBoards checking
        small_heuristic = 0
        brick_win = [0, 0, 0, 0]
        for ib in range(4):
            for jb in range(4):
                if board.block_status[ib][jb] == '-':
                    for i in range(4 * ib, 4 * ib + 4):
                        countp = counto = 0
                        for j in range(4 * jb, 4 * jb + 4):
                            if board.board_status[i][j] == flag:
                                countp += 1
                                counto = -4
                            elif board.board_status[i][j] == chr(ord('x') + ord('o') - ord(flag)):
                                countp = -4
                                counto += 1
                        for j in range(1, 5):
                            if j == countp:
                                brick_win[j - 1] += 1
                            elif j == counto:
                                brick_win[j - 1] -= 1
                    for j in range(4 * jb, 4 * jb + 4):
                        countp = counto = 0
                        for i in range(4 * ib, 4 * ib + 4):
                            if board.board_status[i][j] == flag:
                                countp += 1
                                counto = -4
                            elif board.board_status[i][j] == chr(ord('x') + ord('o') - ord(flag)):
                                countp = -4
                                counto += 1
                        for i in range(1, 5):
                            if i == countp:
                                brick_win[i - 1] += 1
                            elif i == counto:
                                brick_win[i - 1] -= 1
                # diamond
                # take each top of the diamond
                    for i in range(4 * ib, 4 * ib + 2):
                        for j in range(4 * jb + 1, 4 * jb + 3):
                            countp = counto = 0
                            if board.board_status[i][j] == flag:
                                countp += 1
                                counto = -4
                            elif board.board_status[i][j] == chr(ord('x') + ord('o') - ord(flag)):
                                countp = -4
                                counto += 1

                            if board.board_status[i + 1][j - 1] == flag:
                                countp += 1
                                counto = -4
                            elif board.board_status[i + 1][j - 1] == chr(ord('x') + ord('o') - ord(flag)):
                                countp = -4
                                counto += 1

                            if board.board_status[i + 1][j + 1] == flag:
                                countp += 1
                                counto = -4
                            elif board.board_status[i + 1][j + 1] == chr(ord('x') + ord('o') - ord(flag)):
                                countp = -4
                                counto += 1

                            if board.board_status[i + 2][j] == flag:
                                countp += 1
                                counto = -4
                            elif board.board_status[i + 2][j] == chr(ord('x') + ord('o') - ord(flag)):
                                countp = -4
                                counto += 1

                            for k in range(1, 5):
                                if k == countp:
                                    brick_win[k - 1] += 1
                                elif k == counto:
                                    brick_win[k - 1] -= 1

        ret = 0
        for i in range(len(block_win)):
            ret += block_win[i] * self.block_weights[i]
        for i in range(len(brick_win)):
            ret += brick_win[i] * self.board_weights[i]
        #ret += block_corner_win * self.draw_weights[0] + block_edge_win * self.draw_weights[1] + block_center_win * self.draw_weights[2]
        # if openmove:
        #     if flags==self.player_num:
        #         ret+= self.openmove_weight
        #     else:
        #         ret -= self.openmove_weight
        # if flags==self.player_num:
        #     ret+=self.bonuscount * self.bonusweight
        # else:
        #     ret -= self.bonuscount * self.bonusweight
        #print ret
        return ret
