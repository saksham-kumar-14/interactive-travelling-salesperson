import pygame, random, math, sys
pygame.init()
width, height = 1000,800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 30
play = True
pygame.display.set_caption("Interactive Shortest connections")

def display_text(screen,string, coordx, coordy, fontSize,color):
    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    text = font.render(string, True, color) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 

    screen.blit(text,textRect)

class Node:
	def __init__(self, radius, bias):
		self.x = random.randrange(radius, width-radius)
		self.y = random.randrange(radius+ bias, height-radius)
		self.radius = radius

	def generate_coord(self, bias):
		self.x = random.randrange(self.radius, width-self.radius)
		self.y = random.randrange(self.radius+ bias, height-self.radius)

	def display(self,screen):
		pygame.draw.circle(screen, (0,150,150), (self.x,self.y), self.radius)

	def is_overlapping(self, nodes):
		for node in nodes:
			if math.sqrt( (self.x-node.x)**2 + (self.y-node.y)**2 ) < self.radius + node.radius + 5 :
				return True
		return False

class Path:
	def __init__(self, connections, distance):
		self.connections = connections
		self.distance = distance

def permutations(elements):
    if len(elements) <= 1:
        yield elements
        return
    for perm in permutations(elements[1:]):
        for i in range(len(elements)):
            # nb elements[0:1] works in both string and list contexts
            yield perm[:i] + elements[0:1] + perm[i:]

def swap(arr, i,j):
	temp = arr[i]
	arr[i] = arr[j]
	arr[j] = temp
	return arr

def main():
	global screen, width, height, play

	#user interaction
	user_lines = []
	lines_color = (0,0,0)
	current_node_1 = None
	current_node_2 = None
	prev_m_pressed = False
	bias = 50
	btn_x, btn_y, btn_width, btn_height = width//2 - 100,0,200,bias
	btn_color = (0,255,0)

	#node
	radius = 20
	nodes = []
	n = 5
	for i in range(n):
		node = Node(radius, bias)
		while node.is_overlapping(nodes):
			node.generate_coord(bias)
		nodes.append(node)
	all_prem_nodes = list(permutations(nodes))
	current_prem_idx = 0

	# computer solving
	comp_solving = False
	current_shortest_path = Path([], sys.maxsize)

	running = True
	while running :
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE] or pygame.key.get_pressed()[pygame.K_q] :
				running = False
				play = False
			if pygame.key.get_pressed()[pygame.K_r]:
				running = False
		screen.fill((255,255,255))
		mx,my = pygame.mouse.get_pos()
		m_pressed = True in pygame.mouse.get_pressed()

		# user draws lines
		if current_node_1 == None:
			for i in nodes:
				if math.sqrt( (mx-i.x)**2 + (my-i.y)**2 ) < i.radius and m_pressed :
					current_node_1 = i
					current_node_2 = [mx,my]
					break
		else:
			if m_pressed:
				current_node_2= [mx,my]
			elif prev_m_pressed and not m_pressed:
				for i in nodes:
					if math.sqrt( (mx-i.x)**2 + (my-i.y)**2 ) < i.radius and i!= current_node_1 :
						user_lines.append([current_node_1, i])
			else:
				current_node_1 = None
				current_node_2 = None


		for i in user_lines:
			pygame.draw.line(screen, lines_color, (i[0].x, i[0].y), (i[1].x, i[1].y), 20)

		if current_node_1!= None and current_node_2!=None:
			pygame.draw.line(screen, (255,0,0), (current_node_1.x, current_node_1.y), (current_node_2[0], current_node_2[1]), 20)

		# display nodes
		for i in nodes:
			i.display(screen)
		pygame.draw.line(screen, (0,0,0), (0,bias), (width,bias))

		if comp_solving:
			display_text(screen,"Progress: " + str(100*(current_prem_idx/len(all_prem_nodes)))[:6] + "%", 200, bias//2, 25, (0,0,0))
			if current_prem_idx!=len(all_prem_nodes):
				temp_dis = 0
				for i in range(len(all_prem_nodes[0])):
					if i!=0:
						t = all_prem_nodes[current_prem_idx]
						pygame.draw.line(screen, (0,255,0), (t[i-1].x, t[i-1].y), (t[i].x, t[i].y))
						temp_dis += math.sqrt( (t[i-1].x-t[i].x)**2 + (t[i-1].y-t[i].y)**2 )

				if temp_dis < current_shortest_path.distance:
					current_shortest_path.distance = temp_dis
					current_shortest_path.connections = t

				current_prem_idx += 1


			t = current_shortest_path.connections
			for i in range(len(t)):
				if i!=0:
					pygame.draw.line(screen, (255,0,0), (t[i-1].x, t[i-1].y), (t[i].x, t[i].y))

		else:
			pygame.draw.rect(screen, btn_color, pygame.Rect(btn_x, btn_y, btn_width, btn_height))
			display_text(screen,"Start", width//2, bias//2, 25, (0,0,0))
			if btn_x < mx < btn_x+btn_width and btn_y<my<btn_y+btn_height:
				btn_color = (0,150,0)
				if m_pressed:
					comp_solving = True
					lines_color = (200,200,200)
			else:
				btn_color = (0,255,0)


		prev_m_pressed = m_pressed
		clock.tick(FPS)
		pygame.display.flip()

if __name__ == '__main__':
	while play:
		main()