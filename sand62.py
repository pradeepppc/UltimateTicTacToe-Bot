from time import time
class Team62:
    def __init__(self):
        self.timelimit=15.5
        self.initdepth=2
        self.inittime=0
        self.timeovermid=False
        self.ply=''
        self.block_weights=[pow(20,3),pow(20,4),pow(20,5),pow(20,6)]
        self.board_weights=[pow(20,0),pow(20,1),pow(20,2),pow(20,3)]
        self.draw_weights=[pow(20,3)/6,pow(20,3)/9,pow(20,3)/12]
    def timeover(self):
        return time()-self.inittime > self.timelimit
    def move(self, board, old_move, flag):
        #this method called in the simulator
        self.inittime=time()
        self.timeovermid=False
        self.ply=flag
        avail_moves=board.find_valid_move_cells(old_move)
        depth_allow=self.initdepth
        #best_move means the index of the best move in the avail_moves
        best_move=-1;
        while not self.timeover:
            #break the loop when time limit exceeds
            #if it enters then check for best move in a depth of 'depth_allow'
            move=self.moveDepth(board,old_move,depth_allow,flag)
            if not self.timeovermid :
                # time still there
                best_move=move
                #increase the depth allowed
                depth_allow+=1
            else:
                #time is over in the middle of computing 'depth_allow' depth
                #return the best move till now
                pass
        return avail_moves[best_move];
    def moveDepth(self,board,old_move,depth_allow,flag):
        #Now search for the best move using alpha-beta pruning and minimax
        if timeover:
            self.timeovermid=True;
        avail_moves=board.find_valid_move_cells(old_move)
        best_moves=[] #contains indices of the bestmoves
        bestmoveValue=-10000000;
        for i in range(len(avail_moves)):
            #take this move and go forward with updating the board I mean visualize the board
            #and while coming back revert the moves i.e change the updated blocks in the board
            #board.update(old_move,avail_moves[i],flag)
            moveValue=self.minimax(board,avail_moves[i],depth_allow-1,-10000000,10000000,chr(ord('x')+ord('o')-ord(flag)),False)
            if moveValue>bestmoveValue:
                best_moves=[i]
                bestmoveValue=moveValue
            elif moveValue==bestmoveValue:
                #there may be one or more moves with equal significance
                #therefore append it in best_moves
                best_moves.append(i)
            #change the board_status to original state
            #board.board_status[avail_moves[i][0]][avail_moves[i][1]]='-'
            #board.block_status[avail_moves[i][0]/4][avail_moves[i][1]/4]='-'
        return best_moves[random.randint(0,len(best_moves)-1)]
    def minimax(self,board,old_move,depth_allow,alpha,beta,flag,maxply):
        if self.timeover:
            self.timeovermid=True
            return -1;
        if depth_allow==0:
            pass
            #self.heuristic(board,old_move)
            #return heuristic at that node after the old_move
        avail_moves=board.find_valid_move_cells(old_move)
        if maxply:
            for move in avail_moves:
                #check whether time is present or not
                if self.timeover:
                    return -1
                #if alpha > beta i.e we know that it is waste of expanding that node therefore break
                if alpha >= beta :
                    break
                #take this move and similar to above update the board and check
                board.update(old_move,move,flag)
                temp=max(temp,self.minimax(board,move,depth_allow-1,aplha,beta,chr(ord('x')+ord('o')-ord(flag)),not maxply))
                alpha=max(alpha,temp)
                board.board_status[avail_moves[i][0]][avail_moves[i][1]]='-'
                board.block_status[avail_moves[i][0]/4][avail_moves[i][1]/4]='-'
        else:
            for move in avail_moves:
                #check whether time is present or not
                if self.timeover:
                    return -1
                #if alpha > beta i.e we know that it is waste of expanding that node therefore break
                if alpha >= beta :
                    break
                #take this move and similar to above update the board and check
                board.update(old_move,move,flag)
                temp=min(temp,self.minimax(board,move,depth_allow-1,aplha,beta,chr(ord('x')+ord('o')-ord(flag)),not maxply))
                beta=min(beta,temp)
                board.board_status[avail_moves[i][0]][avail_moves[i][1]]='-'
                board.block_status[avail_moves[i][0]/4][avail_moves[i][1]/4]='-'

    def heuristic(self,board,old_move):
        flag=self.ply
        # block_corner_win block_corner_lost
        #block_edge_win block_edge_lost
        #block_center_win block_center_lost
        block_center_win=block_edge_win=block_corner_win=0
        for i in range(4):
            for j in range(4):
                if board.block_status[i][j]==flag :
                    if (i==3 or i==0) and (j==0 or j==3):
                        block_corner_win+=1
                    elif i==0 or j==0 or i==3 or j==3:
                        block_edge_win+=1
                    else:
                        block_center_win+=1
                elif board.block_status[i][j]==chr(ord('x')+ord('o')-ord(flag)) :
                    if (i==3 or i==0) and (j==0 or j==3):
                        block_corner_win-=1
                    elif i==0 or j==0 or i==3 or j==3:
                        block_edge_win-=1
                    else:
                        block_center_win-=1

        # block4_win block3_win block2_win block1_win
        block_win = [0,0,0,0]
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
            countp=counto=0
            for j in range(4):
                if board.block_status[i][j]==flag:
                    countp+=1
                    counto=-4
                elif board.block_status[i][j]==chr(ord('x')+ord('o')-ord(flag)):
                    countp=-4
                    counto+=1
            for j in range(1,5):
                if j==countp:
                    block_win[j-1]+=1
                elif j==counto:
                    block_win[j-1]-=1
        for j in range(4):
            countp=counto=0
            for i in range(4):
                if board.block_status[i][j]==flag:
                    countp+=1
                    counto=-4
                elif board.block_status[i][j]==chr(ord('x')+ord('o')-ord(flag)):
                    countp=-4
                    counto+=1
            for i in range(1,5):
                if i==countp:
                    block_win[i-1]+=1
                elif i==counto:
                    block_win[i-1]-=1
        #diamond
        #take each top of the diamond
        for i in range(2):
            for j in range(1,3):
                countp=counto=0
                if board.block_status[i][j]==flag:
                    countp+=1
                    counto=-4
                elif board.block_status[i][j]==chr(ord('x')+ord('o')-ord(flag)):
                    countp=-4
                    counto+=1

                if board.block_status[i+1][j-1]==flag:
                    countp+=1
                    counto=-4
                elif board.block_status[i+1][j-1]==chr(ord('x')+ord('o')-ord(flag)):
                    countp=-4
                    counto+=1

                if board.block_status[i+1][j+1]==flag:
                    countp+=1
                    counto=-4
                elif board.block_status[i+1][j+1]==chr(ord('x')+ord('o')-ord(flag)):
                    countp=-4
                    counto+=1

                if board.block_status[i+2][j]==flag:
                    countp+=1
                    counto=-4
                elif board.block_status[i+2][j]==chr(ord('x')+ord('o')-ord(flag)):
                    countp=-4
                    counto+=1

                for k in range(1,5):
                    if k==countp:
                        block_win[k-1]+=1
                    elif k==counto:
                        block_win[k-1]-=1

        #smallBoards checking
        small_heuristic=0
        brick_win = [0,0,0,0]
        for ib in range(4):
            for jb in range(4):
                for i in range(4*ib,4*ib+4):
                    countp=counto=0
                    for j in range(4*jb,4*jb+4):
                        if board.board_status[i][j]==flag:
                            countp+=1
                            counto=-4
                        elif board.board_status[i][j]==chr(ord('x')+ord('o')-ord(flag)):
                            countp=-4
                            counto+=1
                    for j in range(1,5):
                        if j==countp:
                            brick_win[j-1]+=1
                        elif j==counto:
                            brick_win[j-1]-=1
                for j in range(4*jb,4*jb+4):
                    countp=counto=0
                    for i in range(4*ib,4*ib+4):
                        if board.board_status[i][j]==flag:
                            countp+=1
                            counto=-4
                        elif board.board_status[i][j]==chr(ord('x')+ord('o')-ord(flag)):
                            countp=-4
                            counto+=1
                    for i in range(1,5):
                        if i==countp:
                            brick_win[i-1]+=1
                        elif i==counto:
                            brick_win[i-1]-=1
                #diamond
                #take each top of the diamond
                for i in range(4*ib,4*ib+2):
                    for j in range(4*jb+1,4*jb+3):
                        countp=counto=0
                        if board.board_status[i][j]==flag:
                            countp+=1
                            counto=-4
                        elif board.board_status[i][j]==chr(ord('x')+ord('o')-ord(flag)):
                            countp=-4
                            counto+=1

                        if board.board_status[i+1][j-1]==flag:
                            countp+=1
                            counto=-4
                        elif board.board_status[i+1][j-1]==chr(ord('x')+ord('o')-ord(flag)):
                            countp=-4
                            counto+=1

                        if board.board_status[i+1][j+1]==flag:
                            countp+=1
                            counto=-4
                        elif board.board_status[i+1][j+1]==chr(ord('x')+ord('o')-ord(flag)):
                            countp=-4
                            counto+=1

                        if board.board_status[i+2][j]==flag:
                            countp+=1
                            counto=-4
                        elif board.board_status[i+2][j]==chr(ord('x')+ord('o')-ord(flag)):
                            countp=-4
                            counto+=1

                        for k in range(1,5):
                            if k==countp:
                                brick_win[k-1]+=1
                            elif k==counto:
                                brick_win[k-1]-=1

        ret=0
        for i in range(len(block_win)) :
            ret+=block_win[i]*self.block_weights[i]
        for i in range(len(brick_win)) :
            ret+=brick_win[i]*self.board_weights[i]
        ret+=block_corner_win*self.draw_weights[0]+block_edge_win*self.draw_weights[1]+block_center_win*self.draw_weights[2]
        return ret
