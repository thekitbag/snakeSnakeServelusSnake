import random

class Status(object):

	def getMyBodyPosition(gamedata):
		for snake in gamedata['board']['snakes']:
			if snake['id'] == gamedata['you']['id']:
				body = snake['body']
		return body


	def getCurrentGoData(gamedata):
		me = gamedata['you']
		turn = gamedata['turn']
		health = me['health']	
		body = Status.getMyBodyPosition(gamedata)
		head = body[0]
		food = gamedata['board']['food']		
		length = len(body)
		tail = body[length-1]
		data = {
		'body': body,
		'head': head,
		'tail': tail,
		'length': length,
		'turn': turn,
		'food': food
		}
		return data

	def getBoardSize(gamedata):
		board_height = gamedata['board']['height']
		board_width = gamedata['board']['width']
		dimensions = {'height': board_height, 'width': board_width} 
		return dimensions

	def getOtherSnakesPositions(gamedata):
		snakes = gamedata['board']['snakes']
		me = Status.getMyBodyPosition(gamedata)	
		snake_bodies = []		
		filled_positions = []
		for snake in snakes:
			if snake['body'] != me:	
				for i in snake['body']:		
					snake_bodies.append(i)
				up = {'x': snake['body'][0]['x'], 'y':snake['body'][0]['y']-1}
				down = {'x': snake['body'][0]['x'], 'y':snake['body'][0]['y']+1}
				left = {'x': snake['body'][0]['x']-1, 'y':snake['body'][0]['y']}
				right = {'x': snake['body'][0]['x']+1, 'y':snake['body'][0]['y']}
				snake_bodies.append(up)
				snake_bodies.append(down)
				snake_bodies.append(right)
				snake_bodies.append(left)
		for coord in snake_bodies:			
			filled_positions.append(coord)					
		return filled_positions


class Assess(object):

	
	def assessNextMoves(position, gamedata):		
		given_position = position			
		safe_options = []
		food_options = []
		deaths = 0
		foods = 0
		projected_positions = Assess.getPossibleNewPositions(position, gamedata)
		head_positions = []		
		for projected_position in projected_positions:
				head_positions.append(projected_position[0])
		for head_position in head_positions:
			if SquareStatus.isOutOfBoardSquare(head_position, gamedata) == True:				
				deaths +=1
			elif SquareStatus.isOtherSnakeSquare(head_position, gamedata) == True:
				deaths +=1
			elif SquareStatus.isFoodSquare(head_position, gamedata) == True:
				foods +=1
				safe_options.append(head_position)
				food_options.append(head_position)
			else: safe_options.append(head_position)
		next_moves_data = {
		'turn': gamedata['turn'],
		'current_position': given_position,
		'projected positions': projected_positions,
		'projected head positions': head_positions,
		'safe options': safe_options,
		'food options': food_options,
		'number of safe options': len(safe_options),
		'deaths': deaths,
		'foods': foods
		}
		return next_moves_data

	def getPossibleNewPositions(position, gamedata):
		original_position = position
		new_positions = []
		head = position[0]
		length = len(position)
		tail = position[length-1]
		possible_moves = [
		{'x': head['x'], 'y':head['y']-1},
		{'x': head['x'], 'y':head['y']+1},
		{'x': head['x']-1, 'y':head['y']},
		{'x': head['x']+1, 'y':head['y']}
		]
		for move in possible_moves:
			if move not in original_position:
				new_body_position = []
				new_body_position.append(move)				
				for coord in original_position:
					new_body_position.append(coord)
				new_body_position.remove(new_body_position[length])
				new_positions.append(new_body_position)
		return new_positions

	def assessSecondTierMoves(projected_positions, gamedata):
		tier_2_data = []
		for position in projected_positions:
			position_data = Assess.assessNextMoves(position, gamedata)
			available_moves = position_data['number of safe options']
			data = {
			"tier 1 move":position[0],
			"score": available_moves
			}
			tier_2_data.append(data)
		return tier_2_data

	def bestOption(next_moves_data, second_tier_data):
		#do some scoring and pick an option
		options = second_tier_data
		seq = [x['score'] for x in options]
		best_score = max(seq)
		for option in options:  
			if option['score'] == best_score:
				return option['tier 1 move']
		"""print(" ")
		print("next moves data")
		print (" ")
		print(next_moves_data)
		print(" ")
		print("second tier data")
		print (" ")
		print(second_tier_data)
		print(" ")
		return random.choice(next_moves_data['safe options'])"""


class SquareStatus(object):

	def isOutOfBoardSquare(coord, gamedata):
		board_size = Status.getBoardSize(gamedata)
		if board_size['width']-1 >= coord['x'] >= 0 and board_size['height']-1 >= coord['y'] >= 0:				
			return False
		else: return True

	def isOtherSnakeSquare(coord, gamedata):
		other_snakes = Status.getOtherSnakesPositions(gamedata)
		if coord in other_snakes:
			return True
		else: return False

	def isFoodSquare(coord, gamedata):
		food_squares = gamedata['board']['food']	
		if coord in food_squares:
			return True
		else: return False



class Decision(object):

	def convertToDirection(gamedata, move):
		head_position = Status.getCurrentGoData(gamedata)['head']
		if head_position['x'] > move['x']:
			return 'left'
		elif head_position['x'] < move['x']:
			return 'right'
		elif head_position['y'] > move['y']:
			return 'up'
		elif head_position['y'] < move['y']:
			return 'down'
		else: return 'error'

	def chooseBestOption(gamedata):
		current_position = Status.getMyBodyPosition(gamedata)
		next_moves_data = Assess.assessNextMoves(current_position, gamedata)
		projected_positions = next_moves_data['projected positions']		
		safe_options = next_moves_data['safe options']
		num_of_safe_options = next_moves_data['number of safe options']
		if num_of_safe_options == 0:
			direction = 'up'
		elif num_of_safe_options == 1:
			direction = Decision.convertToDirection(gamedata, safe_options[0])
		else:
			second_tier_data = Assess.assessSecondTierMoves(projected_positions, gamedata)
			best_option = Assess.bestOption(next_moves_data, second_tier_data)
			direction = Decision.convertToDirection(gamedata, best_option)			
		return direction
		

class Simulate(object):
	def simSecondTiermoves(gamedata, next_moves):
		second_tier_moves = {}		
		for move in next_moves:
			data = {}
			data['deaths'] = move['deaths']




