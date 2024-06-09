import pygame
import time
import queue as queue
from copy import deepcopy
# Define constants
WIDTH, HEIGHT = 800, 700
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHTGRAY = (211, 211, 211)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lunar Lockout")
clock = pygame.time.Clock()
running = True

class LunarLanderGame:
    def __init__(self, map_file):
        self.load_map(map_file)
        self.init_buttons()
        self.init_algorithm_buttons()
        
    def init_buttons(self):
        buttons_y = 60
        buttons_x = 132
        button_width = 40
        button_height = 40
        button_count = 10  # Adjust the number of buttons
        self.buttons = {
            f'button{i}': pygame.Rect(buttons_x + (button_width + 5) * i, buttons_y, button_width, button_height) for i in range(1, button_count + 1)
        }

        # Initialize font
        self.font = pygame.font.Font(None, 36)

    def init_algorithm_buttons(self):
        buttons_y = 600
        buttons_x = 190
        button_width = 100
        button_height = 40

        self.algorithm_buttons = {
            'BFS': pygame.Rect(buttons_x, buttons_y, button_width, button_height),
            'DFS': pygame.Rect(buttons_x + button_width + 5, buttons_y, button_width, button_height),
            'Greedy': pygame.Rect(buttons_x + 2 * (button_width + 5), buttons_y, button_width, button_height),
            'A*': pygame.Rect(buttons_x + 3 * (button_width + 5), buttons_y, button_width, button_height),
        }

        self.font = pygame.font.Font(None, 36)

    def check_algorithm_button_click(self, pos):
        for button_name, rect in self.algorithm_buttons.items():
            if rect.collidepoint(pos):
                return button_name
        return None
    
    def run_algorithm(self, algorithm):
        if algorithm == 'BFS':
            result = self.bfs_alg()
        elif algorithm == 'DFS':
            result = self.dfs_alg()
        elif algorithm == 'Greedy':
            result = self.greedy_search()
        elif algorithm == 'A*':
            result = self.a_star_search()
        else:
            result = False

        if result:
            print(f"{algorithm} Algorithm: Solution found!")
        else:
            print(f"{algorithm} Algorithm: No solution found.")


    def check_button_click(self, pos):
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return button_name
        return None

    def load_map_by_button(self, button_name):
        # Load the corresponding map based on the button clicked
        button_number = int(button_name.replace('button', ''))
        self.load_map(f'maps/map{button_number}.txt')
        print(f"Map {button_number} loaded.")

    def load_map(self, map_file):
        with open(map_file, 'r') as f:
            lines = f.readlines()

        # Extract information from the map file
        self.rows = len(lines)
        self.cols = self.rows
        self.grid = [[lines[i][j] for j in range(self.cols)] for i in range(self.rows)]

        # print(self.grid)
        self.get_avalible_moves()
    def update(self, keys):
        # Update game state based on user input
        pass

    def draw_button_text(self, text, rect):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def draw(self, screen):
        # Draw the game state on the screen
        tile_size = 70

        # Center the map on the screen
        start_x = (WIDTH - self.cols * tile_size) // 2
        start_y = (HEIGHT - self.rows * tile_size) // 2

        

        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.grid[row][col]
                color = RED if tile == 'X' else self.get_robot_color(tile)

                pygame.draw.rect(screen, color, (start_x + col * tile_size, start_y + row * tile_size, tile_size, tile_size),)

                # Draw rectangle for the stroke (border)
                stroke_color = (0, 0, 0)  
                stroke_width = 1  
                pygame.draw.rect(screen, stroke_color, (start_x + col * tile_size - stroke_width,
                                                        start_y + row * tile_size - stroke_width,
                                                        tile_size + 2 * stroke_width,
                                                        tile_size + 2 * stroke_width),
                                 stroke_width)
                
        # Draw finish position in the center
        finish_color = RED
        finish_rect = pygame.Rect((start_x + 2.25*tile_size), (start_y + 2.25*tile_size) , tile_size/2, tile_size/2)
        pygame.draw.rect(screen, finish_color, finish_rect)

        # Draw buttons
        for button_name, rect in game.buttons.items():
            pygame.draw.rect(screen, (0, 0, 255), rect)  # Blue color for buttons
            self.draw_button_text(button_name.replace('button', ''), rect) 

        # Draw algorithm buttons
        for button_name, rect in game.algorithm_buttons.items():
            pygame.draw.rect(screen, (0, 0, 255), rect)
            self.draw_button_text(button_name, rect)



    def get_robot_color(self, robot_char):
        # Assign a unique color for each robot character
        # Customize this method based on your preferences
        robot_colors = {'A': (255, 0, 255), 'B': (0, 255, 0), 'C': (0, 0, 255), 'D': (255, 255, 0), 'E': (0, 0, 0)}
        # robot_colors = {'P': (255, 0, 255), 'G': (0, 255, 0), 'B': (0, 0, 255), 'Y': (255, 255, 0)}
        return robot_colors.get(robot_char, LIGHTGRAY)
    
    def get_avalible_moves(self):
        found_moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.grid[row][col]
                if tile != '0':
                    if col > 0:
                        builded_move = tile + self.check_left(tile,row,col)
                        if len(builded_move) == 2:found_moves.append(builded_move)
                    
                    if col < 4:
                        builded_move = tile + self.check_right(tile,row,col)
                        if len(builded_move) == 2:found_moves.append(builded_move)
                    if row > 0:
                        builded_move = tile + self.check_up(tile,row,col)
                        if len(builded_move) == 2:found_moves.append(builded_move)
                    if row < 4:
                        builded_move = tile + self.check_down(tile,row,col)
                        if len(builded_move) == 2:found_moves.append(builded_move)
        # print(found_moves)
        return found_moves
        
                    
    def check_left(self,tile, row, col):
        if self.grid[row][col-1] != '0':
            return ''
        for i in range(col-1,-1,-1):
            if self.grid[row][i] != '0':
                return 'L'
        return ''

    def check_right(self,tile, row, col):
        if self.grid[row][col+1] != '0':
            return ''
        for i in range(col+1,5):
            if self.grid[row][i] != '0':
                return 'R'
        return ''

    def check_up(self,tile, row, col):
        if self.grid[row-1][col] != '0':
            return ''
        for i in range(row-1,-1,-1):
            if self.grid[i][col] != '0':
                return 'U'
        return ''

    def check_down(self,tile, row, col):
        if self.grid[row+1][col] != '0':
            return ''
        for i in range(row+1,5):
            if self.grid[i][col] != '0':
                return 'D'
        return ''
    
    def is_solved(self):
        # Check if the game is solved
        if self.grid[2][2] == 'X':
            return True
        else:
            return False
        
    def find_robot(self, robot_char):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == robot_char:
                    return row,col
        return -1,-1   
        
    def move_robot(self, robot_char, direction):
        row, col = self.find_robot(robot_char)
        if direction == 'L':
            while self.grid[row][col-1] == '0':
                self.grid[row][col-1] = robot_char
                self.grid[row][col] = '0'
                col -= 1
        elif direction == 'R':
            while self.grid[row][col+1] == '0':
                self.grid[row][col+1] = robot_char
                self.grid[row][col] = '0'
                col += 1
        elif direction == 'U':
            while self.grid[row-1][col] == '0':
                self.grid[row-1][col] = robot_char
                self.grid[row][col] = '0'
                row -= 1
        elif direction == 'D':
            while self.grid[row+1][col] == '0':
                self.grid[row+1][col] = robot_char
                self.grid[row][col] = '0'
                row += 1

    def show_correct_moves(self, moves):

        for move in moves:
            self.move_robot(move[0], move[1])
            screen.fill(WHITE)
            text = self.font.render('Showing final path!', True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, 140))
            screen.blit(text, text_rect)        
            self.draw(screen)
            pygame.display.flip()
            time.sleep(0.4)

    def display_solved_message(self):

        # Display a message on the screen
        text = self.font.render('Solved!', True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(0.5)

    def heuristic(self, person, direction):

        initial_state = deepcopy(self.grid)
        self.move_robot(person, direction)
        
        if person == 'X':
            player_row, player_col = self.find_robot('X')
            goal_row, goal_col = 2, 2

            # Calculate Manhattan distance
            distance = abs(player_row - goal_row) + abs(player_col - goal_col)
            distance = distance / 2
            # Estimate the number of robots in the way
            robots_in_the_way = 0
            for robot_char in ['A', 'B', 'C', 'D', 'E']:

                robot_row, robot_col = self.find_robot(robot_char)
                if robot_row == -1 and robot_col == -1:
                    continue
                # Check if the robot might be in the way
                if (player_row == goal_row and robot_row == player_row and
                        ((player_col < robot_col < goal_col) or (player_col > robot_col > goal_col))):
                    robots_in_the_way += 1
                elif (player_col == goal_col and robot_col == player_col and
                        ((player_row < robot_row < goal_row) or (player_row > robot_row > goal_row))):
                    robots_in_the_way += 1

            self.grid = deepcopy(initial_state)
            return distance + robots_in_the_way
        else:
            player_row, player_col = self.find_robot(person)
            if player_row == 2 and player_col == 2:
                self.grid = deepcopy(initial_state)

                return 2
            elif player_row == 1 and player_col == 2:
                self.grid = deepcopy(initial_state)

                return 0
            elif player_row == 2 and player_col == 1:
                self.grid = deepcopy(initial_state)

                return 0
            elif player_row == 3 and player_col == 2:
                self.grid = deepcopy(initial_state)

                return 0
            elif player_row == 2 and player_col == 3:
                self.grid = deepcopy(initial_state)

                return 0
            else:
                self.grid = deepcopy(initial_state)

                return 1

            

    def transform_field(self):
        new_field = deepcopy(self.grid)
        for row in range(self.rows):
            for col in range(self.cols):
                if new_field[row][col] != 'X' and new_field[row][col] != '0':
                    new_field[row][col] = '1'  
        return new_field 

    def calculate_lengthOfMove(self, move):
        robot_char = move[0]
        direction = move[1]
        row, col = self.find_robot(robot_char)
        number_of_steps = 0
        if direction == 'L':
            while self.grid[row][col-1] == '0':
                number_of_steps += 1
                col -= 1
        elif direction == 'R':
            while self.grid[row][col+1] == '0':
                number_of_steps += 1
                col += 1
        elif direction == 'U':
            while self.grid[row-1][col] == '0':
                number_of_steps += 1
                row -= 1
        elif direction == 'D':
            while self.grid[row+1][col] == '0':
                number_of_steps += 1
                row += 1
        return number_of_steps
    
    def display_number_of_moves_and_depth(self, number_of_moves, depth):
        # Display a message on the screen
        text = self.font.render('Solved!', True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        text = self.font.render(f'Visited states: {number_of_moves}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2  + 200))
        screen.blit(text, text_rect)

        text = self.font.render(f'Depth: {depth}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2 + 140, HEIGHT // 2 + 200))
        screen.blit(text, text_rect)

        pygame.display.flip()
        time.sleep(4)

    # ================== BFS ==================
    def bfs_alg(self):
        initial_state = self.grid        
        avalible_moves = self.get_avalible_moves()
        number_of_moves = 0
        visited = []
        visited.append(self.transform_field())
        
        if avalible_moves == []:
            return False
        
        # queueAvailMoves = queue.Queue()
        # queueGrids = queue.Queue()
        # move, grid, depth, move_history
        bfs_queue = queue.Queue()
        for move in avalible_moves:
            # queueAvailMoves.put(move)
            # queueGrids.put(deepcopy(initial_state))
            bfs_queue.put((move, deepcopy(initial_state), 1, [move]))

        while not bfs_queue.empty():
            number_of_moves += 1
            current_move, current_grid, current_depth, current_move_history = bfs_queue.get()
            # current_move = queueAvailMoves._get()
            # print('current_move',current_move)
            self.grid = current_grid
            self.move_robot(current_move[0],current_move[1])
            screen.fill(WHITE)        
            self.draw(screen)
            pygame.display.flip()
            # time.sleep(0.1)
            if self.is_solved():
                print('Number of moves: ',number_of_moves)
                print('Move history: ',current_move_history)
                print('Depth: ',current_depth)
                self.display_solved_message()
                self.grid = initial_state
                screen.fill(WHITE)        
                self.draw(screen)
                pygame.display.flip()
                time.sleep(1)
                self.show_correct_moves(current_move_history)
                self.display_number_of_moves_and_depth(number_of_moves, current_depth)
                return True
            
            elif self.transform_field() not in visited:
                visited.append(self.transform_field())
                avalible_moves = self.get_avalible_moves()
                for move in avalible_moves:
                    # queueAvailMoves.put(move)
                    # queueGrids.put(deepcopy(self.grid))
                    bfs_queue.put((move, deepcopy(self.grid), current_depth + 1, current_move_history + [move]))

            screen.fill(WHITE)        
            self.draw(screen)
            pygame.display.flip()
            # time.sleep(0.1)

        return False
    
    # ================== DFS ==================
    def dfs_alg(self):
        initial_state = self.grid
        available_moves = self.get_avalible_moves()
        number_of_moves = 0
        visited = []
        visited.append(self.transform_field())

        if not available_moves:
            return False

        dfs_stack = []
        for move in available_moves:
            dfs_stack.append((move, deepcopy(initial_state), 1, [move]))

        while dfs_stack:
            number_of_moves += 1
            current_move, current_grid, current_depth, current_move_history = dfs_stack.pop()
            self.grid = current_grid
            self.move_robot(current_move[0], current_move[1])
            screen.fill(WHITE)
            self.draw(screen)
            pygame.display.flip()

            if self.is_solved():
                print('Number of moves: ', number_of_moves)
                print('Move history: ', current_move_history)
                print('Depth: ', current_depth)
                self.display_solved_message()
                self.grid = initial_state
                screen.fill(WHITE)
                self.draw(screen)
                pygame.display.flip()
                time.sleep(1)
                self.show_correct_moves(current_move_history)
                self.display_number_of_moves_and_depth(number_of_moves, current_depth)
                return True

            elif self.transform_field() not in visited:
                visited.append(self.transform_field())
                available_moves = self.get_avalible_moves()
                for move in available_moves:
                    dfs_stack.append((move, deepcopy(self.grid), current_depth + 1, current_move_history + [move]))

            screen.fill(WHITE)
            self.draw(screen)
            pygame.display.flip()

        return False

    # ================== Greedy ==================
    def greedy_search(self):
        initial_state = deepcopy(self.grid)
        available_moves = self.get_avalible_moves()
        number_of_moves = 0
        visited = []
        visited.append(self.transform_field())

        if not available_moves:
            return False

        greedy_queue = queue.PriorityQueue()
        for move in available_moves:
            greedy_queue.put((self.heuristic(move[0], move[1]), move, deepcopy(initial_state), 1, [move]))

        while not greedy_queue.empty():
            number_of_moves += 1
            current_move, current_grid, current_depth, current_move_history = greedy_queue.get()[1:]
            self.grid = current_grid
            self.move_robot(current_move[0], current_move[1])
            screen.fill(WHITE)
            self.draw(screen)
            pygame.display.flip()

            if self.is_solved():
                print('Number of moves: ', number_of_moves)
                print('Move history: ', current_move_history)
                print('Depth: ', current_depth)
                self.display_solved_message()
                self.grid = initial_state
                screen.fill(WHITE)
                self.draw(screen)
                pygame.display.flip()
                time.sleep(1)
                self.show_correct_moves(current_move_history)
                self.display_number_of_moves_and_depth(number_of_moves, current_depth)
                return True

            elif self.transform_field() not in visited:
                visited.append(self.transform_field())
                available_moves = self.get_avalible_moves()
                for move in available_moves:
                    greedy_queue.put((self.heuristic(move[0], move[1]), move, deepcopy(self.grid), current_depth + 1, current_move_history + [move]))
            screen.fill(WHITE)
            self.draw(screen)
            pygame.display.flip()

        return False
    
    # ================== A* ==================
    def a_star_search(self):
        initial_state = deepcopy(self.grid)
        available_moves = self.get_avalible_moves()
        number_of_moves = 0
        visited = []
        visited.append(self.transform_field())

        if not available_moves:
            return False

        a_star_queue = queue.PriorityQueue()
        for move in available_moves:
            a_star_queue.put((self.heuristic(move[0], move[1]) + self.calculate_lengthOfMove(move), move, deepcopy(initial_state), [move], self.calculate_lengthOfMove(move)))

        while not a_star_queue.empty():
            number_of_moves += 1
            current_move, current_grid, current_move_history, comulative_value = a_star_queue.get()[1:]
            self.grid = current_grid
            self.move_robot(current_move[0], current_move[1])
            screen.fill(WHITE)
            self.draw(screen)
            pygame.display.flip()

            if self.is_solved():
                print('  Number of moves: ', number_of_moves)
                print('  Move history: ', current_move_history)
                print('  Depth: ', len(current_move_history))
                self.display_solved_message()
                self.grid = initial_state
                screen.fill(WHITE)
                self.draw(screen)
                pygame.display.flip()
                time.sleep(1)
                self.show_correct_moves(current_move_history)
                self.display_number_of_moves_and_depth(number_of_moves, len(current_move_history))
                return True

            elif self.transform_field() not in visited:
                visited.append(self.transform_field())
                available_moves = self.get_avalible_moves()
                for move in available_moves:
                    comulative_value += self.calculate_lengthOfMove(move)
                    a_star_queue.put((self.heuristic(move[0], move[1]) + comulative_value , move, deepcopy(self.grid),current_move_history + [move],comulative_value))
            screen.fill(WHITE)
            self.draw(screen)
            pygame.display.flip()

        return False


# Create an instance of the game with a map file
game = LunarLanderGame('maps/map1.txt')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                clicked_button = game.check_button_click(mouse_pos)
                clicked_algorithm_button = game.check_algorithm_button_click(mouse_pos)
                if clicked_button:
                    game.load_map_by_button(clicked_button)
                elif clicked_algorithm_button:
                    game.run_algorithm(clicked_algorithm_button)
    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Update game state
    game.update(keys)

    # Update display
    screen.fill(WHITE)
    game.draw(screen)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
