import pygame
import pygame.gfxdraw
import button
import copy
pygame.init()

screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h
#screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Diamond Dual")




WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED=(255,3,3)
OPTION_COLOR=(196, 215, 178)
GREEN=(17,0,158)

#load button img


center_x = width // 2
center_y = height // 2+(70)


bigger_side = width//2.5


smaller_side = height//2



rhombus_width = 140  
rhombus_height = 140  
rhombus_thickness = 3


top = (center_x, center_y - bigger_side // 2)
top_l=(top[0] + rhombus_width // 2, top[1]+rhombus_height//2)
top_r=(top[0] - rhombus_width // 2, top[1]+rhombus_height//2)
top_t=((top[0] , top[1]+rhombus_height))

right = (center_x + bigger_side // 2, center_y)
right_r=(right[0]-rhombus_width//2, right[1]-rhombus_height//2)
right_l=(right[0]-rhombus_height//2, right[1]+rhombus_height//2)
right_t=(right[0]-rhombus_height,right[1])

left = (center_x - bigger_side // 2, center_y)
left_r=(left[0]+rhombus_height//2,left[1]+rhombus_width//2)
left_l=(left[0]+rhombus_height//2,left[1]-rhombus_width//2)
left_t=(left[0]+rhombus_height,left[1])


bottom = (center_x, center_y + bigger_side // 2)
bottom_r=(bottom[0]+rhombus_height//2, bottom[1]-rhombus_height//2)
bottom_l=(bottom[0]-rhombus_height//2, bottom[1]-rhombus_height//2)
bottom_t=(bottom[0],bottom[1]-rhombus_height)

center=(center_x,center_y)
center_l=(center[0]-rhombus_height//2,center[1])
center_r=(center[0]+rhombus_height//2,center[1])
center_t_up=(center[0],center[1]-rhombus_height//2)
center_t_down=(center[0],center[1]+rhombus_height//2)

ai_beads_position=[top,top_l,top_r,top_t,left_l,right_r]
human_beads_position=[bottom,bottom_l,bottom_r,bottom_t,left_r,right_l]



def Get_First_Hop_Neighbour(): 
    Neighbour={
        (top):(top_l,top_r,top_t),
        (top_r):(top,top_t,left_l),
        (top_l):(top,top_t,right_r),
        (top_t):(top,top_l,top_r,center_t_up),
        
        (left):(left_l,left_r,left_t),
        (left_l):(left,left_t,top_r),
        (left_r):(left,left_t,bottom_l),
        (left_t):(left,left_l,left_r,center_l),
        
        (right):(right_r,right_l,right_t),
        (right_r):(right,right_t,top_l),
        (right_l):(right,right_t,bottom_r),
        (right_t):(right_r,right_l,right,center_r),
        
        (bottom):(bottom_l,bottom_r,bottom_t),
        (bottom_r):(bottom,bottom_t,right_l),
        (bottom_l):(bottom,bottom_t,left_r),
        (bottom_t):(bottom,bottom_l,bottom_r,center_t_down),
        
        (center):(center_l,center_r,center_t_up,center_t_down),
        (center_l):(center,center_t_up,center_t_down,left_t),
        (center_r):(center,center_t_down,center_t_up,right_t),
        (center_t_up):(center,center_l,center_r,top_t),
        (center_t_down):(center,center_l,center_r,bottom_t)
        
        }
    return Neighbour


def Valid_Position_For_Circle(): 
    circle_position=[]
    circle_position.append(top)
    circle_position.append(top_r)
    circle_position.append(top_l)
    circle_position.append(top_t)
    
    circle_position.append(left)
    circle_position.append(left_r)
    circle_position.append(left_l)
    circle_position.append(left_t)
    
    circle_position.append(right)
    circle_position.append(right_r)
    circle_position.append(right_l)
    circle_position.append(right_t)
    
    circle_position.append(bottom)
    circle_position.append(bottom_r)
    circle_position.append(bottom_l)
    circle_position.append(bottom_t)
    
    circle_position.append(center)
    circle_position.append(center_r)
    circle_position.append(center_l)
    circle_position.append(center_t_up)
    circle_position.append(center_t_down)
   
   
    
    return circle_position

circle_radius = 10
circle_color_AI = RED
circle_color_Human = GREEN  

circle_x = width // 2
circle_y = height // 2


valid_position=Valid_Position_For_Circle()
neighbour=Get_First_Hop_Neighbour()


text_font=pygame.font.SysFont("Arial", 25)

text_font_won=pygame.font.SysFont("Arial", 35)
font=pygame.font.SysFont("gabriola", 80)
            


def draw_text(text,font,text_col, x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))
    

def Draw_Circle(ara,color):
    for item in ara:
        pygame.draw.circle(screen,color,item,10)
        

def Find_Match(ara, pos): 
    for item in ara :
        x=item[0]
        y=item[1]
        
        if(abs(x-pos[0])<=40 and abs(y-pos[1])<=40):
            return x,y
    
    return -1,-1

def Heuristic_Val(pos,neighbour): 
    ara=neighbour[pos]
    count=len(ara)
    
    for item in ara:
        x,y=Find_Match(ai_beads_position, item)
        if(x!=-1):
            count-=1
            continue
        x,y=Find_Match(human_beads_position, item)
        if(x!=-1):
            count-=1
         
    return count


def Check_Winner(ai_beads_position, human_beads_position):
    if len(ai_beads_position)<4:
        return 1
    elif len(human_beads_position)<4:
        return 0
    else:
        winner=False
        return -1

def Trap_Beads(x,y, neighbour,color):
    ara=neighbour[(x,y)]
    count=len(ara)
    
    count2=0
    
   
    for item in ara:
        x,y=Find_Match(ai_beads_position, item)
        if(x!=-1):
            count-=1
            if(color==GREEN):
                count2+=1
                continue
            
        x,y=Find_Match(human_beads_position,item)
        if(x!=-1):
            count-=1
            if(color==RED):
                count2+=1
                continue
    return count,count2






def Draw_Polygon():
    
    pygame.draw.polygon(screen, BLACK, [top,right,bottom,left],rhombus_thickness)
    
    pygame.draw.polygon(screen, BLACK, [center_t_up,center_r,center_t_down,center_l],rhombus_thickness)
                                  
   
    pygame.draw.polygon(screen, BLACK, [top ,top_l,top_t,top_r], rhombus_thickness)

   
    pygame.draw.polygon(screen, BLACK, [right_l,right,right_r,right_t],rhombus_thickness)                                         
                                         
   
    pygame.draw.polygon(screen, BLACK, [bottom_r,bottom_t,bottom_l,bottom],rhombus_thickness)
                                                                            
    
    pygame.draw.polygon(screen, BLACK, [left_l,left_t,left_r,left],rhombus_thickness)
     




def Heuristic_Value_Min_Max(pos,ara_ai, ara_human): 
    
    ara=neighbour[pos]
    count=len(ara)
    for item in ara:
        x,y=Find_Match(ara_ai, item)
        p,q=Find_Match(ara_human, item)
        
        if(x!=-1 or p!=-1):
            count-=1
    return count



def All_Heuristic_Value_Min_Max(ara_ai,ara_human):
    result=[]
    for item in ara_ai:
        x=Heuristic_Value_Min_Max(item, ara_ai, ara_human)
        result.append(x)
    return result
     

def Ai_Move(max_node):   
    max_node_empty_neighbour=(-1,-1)
    ara=neighbour[max_node]
    a=[]
    mm=-1000
    for item in ara:
        x,y=Find_Match(ai_beads_position, item)
        p,q=Find_Match(human_beads_position, item)
        
        if(x==-1 and p==-1):
            c=Heuristic_Val(item, neighbour)
            if(c>mm):
                mm=c
                max_node_empty_neighbour=item    
    return max_node_empty_neighbour


def Empty_Neighbour(node):
    ara=neighbour[node]
    ara1=[]
    
    for item in ara:
        x,y=Find_Match(ai_beads_position,item)
        if(x!=-1):
            
            continue
        x,y=Find_Match(human_beads_position, item)
        if(x!=-1):
            continue
        
        ara1.append(item)
    
    return ara1


def Max_Beads_Value():
    maxi=-1000
    node=(1,1)
    
    #print(human_beads_position)
    for item in ai_beads_position:
        x=Heuristic_Val(item, neighbour) 
        
        if(x==1): 
            one_neighbor=Ai_Move(item) 
            
            for ele in human_beads_position:
                ara=Empty_Neighbour(ele) 
                
                x,y=Find_Match(ara, one_neighbor) 
                if(x!=-1):
                    return item
            
        
        if(x>maxi):
            maxi=x
            node=item
    return node


def All_Heuristic_Value_Min_Max_Ai(ara_ai,ara_human):
    result=[]
    
    for item in ara_ai:
        x=Heuristic_Value_Min_Max(item, ara_ai, ara_human)
        result.append(x)
    return result



def All_Heuristic_Value_Min_Max_Human(ara_ai,ara_human):
    result=[]
    
    for item in ara_human:
        x=Heuristic_Value_Min_Max(item, ara_ai, ara_human)
        result.append(x)
    return result







def Mini_Max_Move(ara_ai, ara_human, depth, maxPlayer):
    best_item=None
    best_node=None
    if depth == 0:
        result1 = All_Heuristic_Value_Min_Max_Ai(ara_ai, ara_human)
        result2 = All_Heuristic_Value_Min_Max_Human(ara_ai, ara_human)
        return (sum(result1) - sum(result2)) + len(ai_beads_position) - len(human_beads_position) , best_item , best_node

    if maxPlayer:
        maxEle = -10000
        best_item = None
        best_node = None
        for node in ara_ai:
            
            val= Heuristic_Val(node, neighbour)
            if val==0:
                continue
            else:
                ara= Empty_Neighbour(node)
                for item in ara:
                    temp_ai = copy.deepcopy(ara_ai)
                    x, y = Find_Match(temp_ai, item)
                    p, q = Find_Match(ara_human, item)
                    if x != -1 and p != -1:
                        continue
                    temp_ai.append(item)
                    temp_ai.remove(node)
                    result, _, _ = Mini_Max_Move(temp_ai, ara_human, depth-1, False)
                    if result > maxEle:
                        maxEle = result
                        best_item = item
                        best_node = node
            

        return maxEle, best_item, best_node

    else:
        minEle = 100000
        best_item = None
        best_node = None
        for node in ara_human:
            val= Heuristic_Val(node, neighbour)
            if val==0:
                continue
            else:
                ara= Empty_Neighbour(node)
                for item in ara:
                    temp_human = copy.deepcopy(ara_human)
                    x, y = Find_Match(ara_ai, item)
                    p, q = Find_Match(temp_human, item)
                    if x != -1 or p != -1:
                        continue
                    temp_human.append(item)
                    temp_human.remove(node)
                    result, _, _ = Mini_Max_Move(ara_ai, temp_human, depth-1, True)
                    if result < minEle:
                        minEle = result
                        best_item = item
                        best_node = node
            

        return minEle, best_item, best_node               

         



def Game_Loop():
    running = True
    
    ara=[]
    
    start_time = pygame.time.get_ticks()
   
    count_human=0

    

    human_cor_x=-1
    human_cor_y=-1
    turn=-1
    
    human_move=False
    ai_move=True
    winner=False
    game_paused=True
    ai_img=pygame.image.load("robot.png").convert_alpha()
    ai_button=button.Button(width//3-50, 310, ai_img, 0.4)
    
    valid=False
    
    human_img=pygame.image.load("hacker.png").convert_alpha()
    human_button=button.Button(width//1.5-60, 310,human_img, 0.4)
    
    win_img=pygame.image.load("Win.jpg").convert_alpha()
    win_button=button.Button(width//4+50, 260, win_img, 1)
    
    lose_img=pygame.image.load("lose.jpg").convert_alpha()
    lose_button=button.Button(width//4, 260, lose_img, 1)

    while running:
        
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
                
            if(ai_move==False and human_move==True):
                ara_ai_1=copy.deepcopy(ai_beads_position)
                ara_human_1=copy.deepcopy(human_beads_position)
                
                
                
                result1, i1, n1= (Mini_Max_Move(ara_ai_1, ara_human_1, 4, True))
               
                    
               
                ai_beads_position.remove(n1)
                ai_beads_position.append(i1)
                    
         
                    
                
                ai_move=True
                human_move=False
            
                
                
            if event.type == pygame.QUIT:
                
               
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    winner=False
                    print("pause") 
                    if game_paused == False:
                        game_paused=True
                    elif game_paused == True :
                        game_paused =False
                    
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                
                if event.button == 1:
                    
                    if(count_human==1 and ai_move==True and human_move==False): #already clicked on the bead i want to move
                       
                       node=(human_cor_x,human_cor_y)
                       ara=Empty_Neighbour(node)
                       #print("empty path is:", ara)
                       Draw_Circle(ara, OPTION_COLOR)
                       mouse_pos = pygame.mouse.get_pos()
                       
                       x,y=Find_Match(ai_beads_position, mouse_pos)
                       if(x!=-1):
                          count_human=0
                          human_cor_x=-1
                          human_cor_y=-1
                          continue
                       x,y=Find_Match(human_beads_position, mouse_pos)
                       if(x!=-1):
                           count_human=0
                           human_cor_x=-1
                           human_cor_y=-1
                           continue
                       valid=False
                       valid_path=neighbour[(human_cor_x,human_cor_y)]
                       x,y=Find_Match(valid_path, mouse_pos)
                       
                       if(x!=-1):
                           human_beads_position.remove((human_cor_x,human_cor_y))
                           human_beads_position.append((x,y))
                           human_move=True
                           ai_move=False
                       count_human=0
                       human_cor_x=-1
                       human_cor_y=-1
                       continue
                    if(count_human==0 and ai_move==True and human_move==False): # clicked on correct human bead?
                       mouse_pos = pygame.mouse.get_pos()
                       x,y=Find_Match(human_beads_position, mouse_pos)
                       if(x!=-1):
                           count_human+=1
                           human_cor_x=x
                           human_cor_y=y
                           valid=True
                           ara=Empty_Neighbour((human_cor_x,human_cor_y))
                           
                           
                        
        
        elapsed_time = pygame.time.get_ticks() - start_time
        screen.fill((253, 253, 189))
        for item in ai_beads_position:
            x,y=Trap_Beads(item[0], item[1], neighbour, RED)
            if(x==0 and y!=0):
                ai_beads_position.remove(item)
        
        
        for item in human_beads_position:
            x,y=Trap_Beads(item[0], item[1], neighbour,GREEN)
            
            
            if(x==0):
                if(y>0):
                    
                    human_beads_position.remove(item)
                
                
        
        
        len_ai=(len(ai_beads_position))
        len_human=(len(human_beads_position))
        
        ai_score= "System Score : "
        draw_text(ai_score, text_font, RED, 100, 100)
        ai_score=str(6-len_human)
        draw_text(ai_score, font, RED, 275, 75)
    
        
        human_score= "Player Score : "
        draw_text(human_score, text_font, GREEN, width-300,100)
        ai_score=str(6-len_ai)
        draw_text(ai_score, font, GREEN, width-135, 75)
        
        
        if valid==True:
            for item in ara:
                pygame.draw.circle(screen,OPTION_COLOR,item,10)
        

       
        
        pygame.draw.line(screen, BLACK, top, bottom, 2)
        pygame.draw.line(screen, BLACK, right, left, 2)
        
        
        Draw_Polygon()
        
        #Drawing six circle for AI
        Draw_Circle(human_beads_position, GREEN)
            
        Draw_Circle(ai_beads_position, RED)
        
        if game_paused==False:
            draw_text("Press SPACE to Pause", text_font, BLACK, width//2-100, 50 )
        else:
            screen.fill((253, 253, 189))
            
            draw_text("Chose first player", font, BLACK,width//2-200, 70 )
            draw_text("Computer", text_font, BLACK,width//3, 530 )
            draw_text("Player", text_font, BLACK, width//1.5+10, 530 )
            if ai_button.draw(screen):
                game_paused=False
                ai_move=False
                human_move=True
                turn=1
            if human_button.draw(screen):
                game_paused=False
                turn=0
                ai_move=True
                human_move=False
        val=Check_Winner(ai_beads_position, human_beads_position)
        if(val==-1):
            winner=False
        elif(val==1):
            winner=True
        elif(val==0):
            winner=True   
        if winner==True:
            
            screen.fill(BLACK)

            if val==1:
                if win_button.draw(screen):
                    game_paused=True
                    winner=False
                    


            elif val==0:
                if lose_button.draw(screen):
                    game_paused=True
                    winner=False
                    
                
       
        
        pygame.display.flip()
        pygame.display.update()
        
    



Game_Loop()

pygame.quit()

