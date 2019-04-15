import random

class Status(object):

	def getBodyPosition(gamedata):
		me = gamedata['you']		
		body = me['body']
		return body

	def getHeadPosition(gamedata):
		body = Status.getBodyPosition(gamedata)
		head = body[0]
		return head
	
	def getMyLength(gamedata):
		body = Status.getBodyPosition(gamedata)
		if body[0] == body[1] == body[2]:
			return 1
		elif body[1] == body[2]:
			return 2
		else: return len(body)

	def getCurrentTurn(gamedata):
		turn = gamedata['turn']
		return turn

	def getHealth(gamedata):
		me = gamedata['you']
		health = me['health']
		return health

	def getBoardSize(gamedata):
		board_height = gamedata['board']['height']
		board_width = gamedata['board']['width']
		dimensions = {'height': board_height, 'width': board_width}
		return dimensions

	def getFoodPositions(gamedata):
		food = gamedata['board']['food']
		return food

	def getOtherSnakesPositions(gamedata):
		snakes = gamedata['board']['snakes']
		me = Status.getBodyPosition(gamedata)
		snake_bodies = []		
		filled_positions = []
		for snake in snakes:
			if snake['body'] != me:
				snake_bodies.append(snake['body'])
				up = {'x': snake['body'][0]['x'], 'y':snake['body'][0]['y']-1}
				down = {'x': snake['body'][0]['x'], 'y':snake['body'][0]['y']+1}
				left = {'x': snake['body'][0]['x']-1, 'y':snake['body'][0]['y']}
				right = {'x': snake['body'][0]['x']+1, 'y':snake['body'][0]['y']}
				filled_positions.append(up)
				filled_positions.append(down)
				filled_positions.append(right)
				filled_positions.append(left)
		for body in snake_bodies:
			for coord in body:
				filled_positions.append(coord)
		return filled_positions

class Assess(object):

	def getAllPossibleMoves(gamedata):
		""" returns the coordinates of all four possible moves based
		on the position of the head, regardless of whether they are in
		the board space or not"""
		head = Status.getHeadPosition(gamedata)
		up = {'x': head['x'], 'y':head['y']-1}
		down = {'x': head['x'], 'y':head['y']+1}
		left = {'x': head['x']-1, 'y':head['y']}
		right = {'x': head['x']+1, 'y':head['y']}
		options = [up, down, left, right]
		return options

	def removeOutOfGridMoves(moves, board_size):
		safe_moves = []
		for move in moves:
			if board_size['width']-1 >= move['x'] >= 0 and board_size['height']-1 >= move['y'] >= 0:
				safe_moves.append(move)
		return safe_moves		

	def removeOwnBodyMoves(moves, body_position):					
		safe_moves = []
		for move in moves:
			if move not in body_position:
				safe_moves.append(move)
		return safe_moves

	def removeOtherSnakeMoves(moves, snakes):			
		safe_moves = []
		for move in moves:
			if move not in snakes:
				safe_moves.append(move)
		return safe_moves

	def addBackInTails(snakes):
		pass


	def getAllNonDeathMoves(body_position, gamedata):
		board_size = Status.getBoardSize(gamedata)
		other_snakes = Status.getOtherSnakesPositions(gamedata)
		all_moves = Assess.getAllPossibleMoves(gamedata)
		non_oob_moves = Assess.removeOutOfGridMoves(all_moves, board_size)
		non_own_body_moves = Assess.removeOwnBodyMoves(non_oob_moves, body_position)
		safe_moves = Assess.removeOtherSnakeMoves(non_own_body_moves, other_snakes)
		return safe_moves

	def findNearestfood(gamedata):
		food = Status.getFoodPositions(gamedata)
		head = Status.getHeadPosition(gamedata)
		food_vs_head = []
		deltas = {}
		for food in food:
			food_vs_head.append({'horizontal':food['x']-head['x'], 'vertical':food['y']-head['y']})
		for item in food_vs_head:			
			delta = abs(item['horizontal']) + abs(item['vertical'])
			deltas[food_vs_head.index(item)] = delta		
		nearest = min(deltas.keys(), key=(lambda k: deltas[k]))
		directions = food_vs_head[nearest]				
		return directions

	def getBodyCenterOfGravity(gamedata):
		"""return the center of gravity for the snake so that it can move away from itself better"""
		#average the xs and ys and then move away
		body = Status.getBodyPosition(gamedata)
		body_length = len(body)
		sum_x = 0
		sum_y = 0
		avg_postion = {}
		for coord in body:
			sum_x += coord['x']
			sum_y += coord['y']
		avg_postion['x'] = sum_x/body_length
		avg_postion['y'] = sum_y/body_length		
		return avg_postion




		
	

		


	def killPossible(gamedata):
		pass

	def smallerSnakeNearby(gamedata):
		pass

	def biggerSnakeNearby(gamedata):
		pass



class Action(object):

	def avoidDeath():
		pass

	def chaseFood():
		pass

	def fleeSnake():
		pass

	def chaseSnake():
		pass

class Decision(object):

	def convertToDirection(gamedata, move):
		head_position = Status.getHeadPosition(gamedata)
		if head_position['x'] > move['x']:
			return 'left'
		elif head_position['x'] < move['x']:
			return 'right'
		elif head_position['y'] > move['y']:
			return 'up'
		elif head_position['y'] < move['y']:
			return 'down'
		else: return 'shit'

	def chooseBestOption(gamedata):
		#this needs major splitting out and cleaning up
		body_position = Status.getBodyPosition(gamedata)
		safe_coords = Assess.getAllNonDeathMoves(body_position, gamedata)
		safe_moves = []
		for coord in safe_coords:
			direction = Decision.convertToDirection(gamedata, coord)
			safe_moves.append(direction)
		great_safe_moves = []
		good_safe_moves = []
		for safe_move in safe_moves:
			if Simulate.getNumberOfNextMoves(safe_move, gamedata) == 3:
				great_safe_moves.append(safe_move)
			elif Simulate.getNumberOfNextMoves(safe_move, gamedata) == 2:
				good_safe_moves.append(safe_move)
		food_directions = Decision.foodDirections(gamedata)
		away_from_body_directions = Decision.awayFromBodyDirections(gamedata)
		health = Status.getHealth(gamedata)
		turn = Status.getCurrentTurn(gamedata)		
		go_for_food_options = []
		avoid_self_directions = []
		go_for_food = False
		if turn < 20:
			go_for_food = True
		elif health < 20:
			go_for_food = True		
		for option in food_directions:
			if option in great_safe_moves:
				go_for_food_options.append(option)
			elif option in good_safe_moves:
				go_for_food_options.append(option)
		for direction in away_from_body_directions:
	 		if direction in great_safe_moves:
	 			avoid_self_directions.append(direction)
	 		elif direction in good_safe_moves:
	 			avoid_self_directions.append(direction)
		if go_for_food == True:
			if go_for_food_options:
				print('going for food!')
				chosen_direction = random.choice(go_for_food_options)
			else: 
				if avoid_self_directions:
					print('no safe food options, avoiding myself instead')
					chosen_direction = random.choice(avoid_self_directions)
				else:
					print('no food, no away from self, picking a safe one')
					chosen_direction = random.choice(safe_moves)
		else:
			if avoid_self_directions:
				print('not hungry avoiding myself instead')
				chosen_direction = random.choice(avoid_self_directions)
			else:
				chosen_direction = random.choice(safe_moves)
				print('no away from self, picking a safe one')
		print('safe_moves', safe_moves)
		print('great safe moves', great_safe_moves)
		print('good_safe_moves', good_safe_moves)
		print('chosen_direction', chosen_direction)
		return chosen_direction

	def foodDirections(gamedata):
		instructions = Assess.findNearestfood(gamedata)
		directions = []
		if instructions['horizontal'] > 0:
			directions.append('right')
		elif instructions['horizontal'] < 0:
			directions.append('left')
		if instructions['vertical'] > 0:
			directions.append('down')
		elif instructions['vertical'] < 0:
			directions.append('up')
		return directions

	def awayFromBodyDirections(gamedata):
		avg_position = Assess.getBodyCenterOfGravity(gamedata)
		head_position = Status.getHeadPosition(gamedata)
		best_directions = []
		if head_position['x'] > avg_position['x']:
			best_directions.append('right')
		if head_position['x'] < avg_position['x']:
			best_directions.append('left')
		if head_position['y'] > avg_position['y']:
			best_directions.append('down')
		if head_position['y'] < avg_position['y']:
			best_directions.append('up')
		return best_directions



class Simulate(object):
	def getNumberOfNextMoves(move, gamedata):
		body = Status.getBodyPosition(gamedata)
		length = Status.getMyLength(gamedata)
		new_pos = []
		de_tailed_body = body[0:length-1]
		if move == 'up':
			new_pos.append({'x':body[0]['x'],'y':body[0]['y']-1})
			new_pos.append(body)
		elif move == 'down':
			new_pos.append({'x':body[0]['x'],'y':body[0]['y']+1})
			new_pos.append(body)
		elif move == 'left':
			new_pos.append({'x':body[0]['x']-1,'y':body[0]['y']})
			new_pos.append(body)
		elif move =='right':
			new_pos.append({'x':body[0]['x']+1,'y':body[0]['y']})
			new_pos.append(body)
		else: return 'no move given'
		number_of_available_moves = Assess.getAllNonDeathMoves(new_pos, gamedata)
		return len(number_of_available_moves)

	def getNumberOfSecondRowMoves(first_row_moves, gamedata):
		pass









