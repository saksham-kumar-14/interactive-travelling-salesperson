import pygame,random,math,time

pygame.init()
SIDE = 800
SCREEN = pygame.display.set_mode((SIDE,SIDE))
CLOCK = pygame.time.Clock()
running = True

mat_no = 50
mat_size = SIDE/mat_no

A = [random.randrange(0,mat_no),random.randrange(0,mat_no)]
B = [random.randrange(0,mat_no),random.randrange(0,mat_no)]

obstacles = []
for i in range(1000):
    obs = [random.randrange(0,mat_no),random.randrange(0,mat_no)]
    if obs != A and obs!=B and obs not in obstacles:
        obstacles.append(obs)

open_set = [A] # to be evaluated
closed_set = [] # already evaluated

current = None

def lowest_fcost(s,target):
    result = None
    for i in s:
        if result ==  None:
            result = i
        else:
            if ( (i[0]-target[0])**2 + (i[1]-target[1])**2 ) < ( (result[0]-target[0])**2 + (result[1]-target[1])**2 ):
                result = i

    return result


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        if pygame.key.get_pressed()[pygame.K_r]:
            A = [random.randrange(0,mat_no),random.randrange(0,mat_no)]
            B = [random.randrange(0,mat_no),random.randrange(0,mat_no)]

            obstacles = []
            for i in range(1000):
                obs = [random.randrange(0,mat_no),random.randrange(0,mat_no)]
                if obs != A and obs!=B and obs not in obstacles:
                    obstacles.append(obs)

            open_set = [A] # to be evaluated
            closed_set = [] # already evaluated

            current = None


    SCREEN.fill((255,255,255))

    # algorithm
    if current!=B:
        current = lowest_fcost(open_set,B)
        open_set.remove(current)
        closed_set.append(current)

        for i in range(current[0]-1,current[0]+2):
            for j in range(current[1]-1,current[1]+2):
                if i in range(0,mat_no) and j in range(0,mat_no) and [i,j] not in closed_set and [i,j] not in obstacles:
                    pygame.draw.rect(SCREEN,(0,255,255),pygame.Rect(i*mat_size,j*mat_size,mat_size,mat_size))
                    open_set.append([i,j])


    # drawing stuff

    for i in range(mat_no):
        pygame.draw.line(SCREEN, (0,0,0), (0,i*mat_size),(SIDE,i*mat_size), 1)
    for i in range(mat_no):
        pygame.draw.line(SCREEN, (0,0,0), (i*mat_size,0),(i*mat_size,SIDE), 1)

    a_rec = pygame.Rect(A[0]*mat_size,A[1]*mat_size,mat_size,mat_size)
    b_rec = pygame.Rect(B[0]*mat_size,B[1]*mat_size,mat_size,mat_size)
    pygame.draw.rect(SCREEN,(255,0,0),a_rec)
    pygame.draw.rect(SCREEN,(255,255,0),b_rec)

    for i in obstacles:
        pygame.draw.rect(SCREEN,(0,0,0),pygame.Rect(i[0]*mat_size,i[1]*mat_size,mat_size,mat_size))


    for i in closed_set:
        if i != A and i!=B:
            pygame.draw.rect(SCREEN,(0,0,0),pygame.Rect(i[0]*mat_size,i[1]*mat_size,mat_size,mat_size))
            pygame.draw.rect(SCREEN,(0,255,0),pygame.Rect(i[0]*mat_size+0.5,i[1]*mat_size+0.5,mat_size-0.5,mat_size-0.5))

    pygame.display.update()
    time.sleep(0.1)


pygame.quit()