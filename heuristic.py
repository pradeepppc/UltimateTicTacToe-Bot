board.board_status=[['-' for i in range(4*ib,4*ib+4)] for j in range(4*jb,4*jb+4)]
for i in range(4*ib,4*ib+4):
    board.board_status[i]=raw_input()
#print(board.board_status)
flag='x'
def heuristic():
    # block_corner_win block_corner_lost
    #block_edge_win block_edge_lost
    #block_center_win block_center_lost
    block_center_win=block_edge_win=block_corner_win=0
    for i in range(4*ib,4*ib+4):
        for j in range(4*jb,4*jb+4):
            if board.board_status[i][j]==flag :
                if (i==3 or i==0) and (j==0 or j==3):
                    block_corner_win+=1
                elif i==0 or j==0 or i==3 or j==3:
                    block_edge_win+=1
                else:
                    block_center_win+=1
            elif board.board_status[i][j]==chr(ord('x')+ord('o')-ord(flag)) :
                if (i==3 or i==0) and (j==0 or j==3):
                    block_corner_win-=1
                elif i==0 or j==0 or i==3 or j==3:
                    block_edge_win-=1
                else:
                    block_center_win-=1

    # block4_win block3_win block2_win block1_win
    brick_win = [0,0,0,0]
    # for i in range(4*ib,4*ib+4):
    #     if board.board_status[i][0]==flag and board.board_status[i][1]==flag and board.board_status[i][2]==flag and board.board_status[i][3]==flag:
    #         brick_win[3]+=1
    #     elif board.board_status[0][i]==flag and board.board_status[1][i]==flag and board.board_status[2][i]==flag and board.board_status[3][i]==flag:
    #         brick_win[3]+=1
    #     elif board.board_status[i][0]==chr(ord('x')+ord('o')-ord(flag)) and board.board_status[i][1]==chr(ord('x')+ord('o')-ord(flag)) and board.board_status[i][2]==chr(ord('x')+ord('o')-ord(flag)) and board.board_status[i][3]==chr(ord('x')+ord('o')-ord(flag)):
    #         brick_win[3]-=1
    #     elif board.board_status[0][i]==chr(ord('x')+ord('o')-ord(flag)) and board.board_status[1][i]==chr(ord('x')+ord('o')-ord(flag)) and board.board_status[2][i]==chr(ord('x')+ord('o')-ord(flag)) and board.board_status[3][i]==chr(ord('x')+ord('o')-ord(flag)):
    #         brick_win[3]-=1

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

    print(brick_win)
    print(block_corner_win,block_edge_win,block_center_win)
heuristic()
