import random

"""
assessNextMoves(current_pos, gamedata)
Safe_options = [ ]
Food_options = [ ]
Number_of_safe_options = len(safe_options)
Deaths= int
Foods = int
Projected_positions = getNewPositions(current_pos)
For pos in projected_poditions:
  If isOutOfBoardSquare(pos) or isOtherSnakeSquare(pos) == True:
  Deaths +=1
Elif isFoodSquare == True:
  Food +=1
 Safe_options.append(pos)
  Food_options.append(pos)
Else:
  Safe_options.append(pos)
Return dictionarywithallthatinit

Decision()
Data = AssessNextMoves(currentpos, gamedata
If data[deaths] == 3
 We're fucked
Elif data[deaths] == 2
  Take only safe option
Elif data[deaths] < 2:
 best_option = PickBestOption(data[safeoptions])
Direction= convert(best_option)
Return direction


PickBestOption(lst_of_options, gamedata):
Recommendations = [ ]
Options_data = [ ]
For option in lst_of_options: Options_data.append( {'option':option, 'data':  assesnextMoves(option)})
For I in  options_data:
 If i[data][deaths] == 3:       Recommendations.append('option': i[option], 'rec score' = -5
elif ...
Best_option = ...
Return best_option
#use assesnextMoves on getNewPositions(I[data][projected_positions)
"""

class Status(object):

	def getBodyPosition(gamedata):
		me = gamedata['you']		
		body = me['body']
		return body

	def getHeadPosition(gamedata):
		body = Status.getBodyPosition(gamedata)
		head = body[0]
		return head

	def getTailPosition(gamedata):
		body = Status.getBodyPosition(gamedata)
		length = len(body)
		tail = body[length-1]
		return tail
	
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

	def assessNextMoves(gamedata):
		safe_options = []
		food_options = []
		number_of_safe_options = len(safe_options)
		deaths = 0
		foods = 0
		projected_positions = Assess.getPossibleNewPositions(gamedata)
		for position in projected_positions:
			if SquareStatus.isOutOfBoardSquare(position[0], gamedata) or SquareStatus.isOtherSnakeSquare(position[0], gamedata) == True:
				deaths +=1
			elif SquareStatus.isFoodSquare(position[0], gamedata) == True:
				food +=1
				safe_options.append(position[0])
				food_options.append(position[0])
		else:
			safe_options.append(position[0])
		next_moves_data = {
		'safe options': safe_options,
		'food options': food_options,
		'number of safe options': len(safe_options),
		'deaths': deaths,
		'foods': foods,
		'projected positions': projected_positions
		}
		return next_moves_data

	def getPossibleNewPositions(gamedata):
		new_positions = []
		current_position = Status.getBodyPosition(gamedata)
		head = Status.getHeadPosition(gamedata)
		tail = Status.getTailPosition(gamedata)
		current_position.remove(tail)
		possible_moves = [
		{'x': head['x'], 'y':head['y']-1},
		{'x': head['x'], 'y':head['y']+1},
		{'x': head['x']-1, 'y':head['y']},
		{'x': head['x']+1, 'y':head['y']}
		]
		for move in possible_moves:
			if move not in current_position:
				new_body_position = []
				new_body_position.append(move)
				for position in current_position:
					new_body_position.append(position)
				new_positions.append(new_body_position)
		return new_positions




class SquareStatus(object):

	def isOutOfBoardSquare(coord, gamedata):
		board_size = Status.getBoardSize(gamedata)
		if board_size['width']-1 >= coord['x'] >= 0 and board_size['height']-1 >= coord['y'] >= 0:				
			return True
		else: return False

	def isOtherSnakeSquare(coord, gamedata):
		other_snakes = Status.getOtherSnakesPositions(gamedata)
		if coord in other_snakes:
			return True
		else: return False

	def isfoodSquare(coord, gamedata):
		food_squares = Status.getFoodPositions(gamedata)
		if coord in food_squares:
			return True
		else: return False



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
		print(Assess.assessNextMoves(gamedata))
		return 'left'
		



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









