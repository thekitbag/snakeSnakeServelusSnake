import json
import os
import random
import bottle

from .api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print("GAME HAS STARTED")

    snakestyling = {
    "color": "#001dff",
    "headType": "beluga",
    "tailType": "curled"
    }


    return start_response(snakestyling['color'])


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    #Test.test_function(Assess.assessNextMoves,data)
    move = Decision.chooseBestOption(data)
    return move_response(move)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8000'),
        debug=os.getenv('DEBUG', True)
    )

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
        board_height = gamedata['board']['height']
        board_width = gamedata['board']['width']
        dimensions = {'height': board_height, 'width': board_width} 
        data = {
        'body': body,
        'head': head,
        'tail': tail,
        'length': length,
        'turn': turn,
        'food': food,
        'health': health,
        'board dimensions': dimensions
        }
        return data

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

    
    def nearestOptionToFood(options, gamedata):
        food = Status.getCurrentGoData(gamedata)['food']
        nearest_food_data = []
        for position in options:
            food_vs_head = []
            deltas = {}
            for foodbite in food:
                food_vs_head.append({'horizontal':foodbite['x']-position['x'], 'vertical':foodbite['y']-position['y']})
            for item in food_vs_head:           
                delta = abs(item['horizontal']) + abs(item['vertical'])
                deltas[food_vs_head.index(item)] = delta                        
            nearest = min(deltas.keys(), key=(lambda k: deltas[k]))
            directions = food_vs_head[nearest]          
            nearest_food_data.append({
                'position':position,
                'distance from food': deltas[nearest],
                'directions to food': food_vs_head[nearest],
                'food location': food[nearest]

                })      
        seq = [x['distance from food'] for x in nearest_food_data]
        closest = min(seq)
        for datapoint in nearest_food_data:
            if datapoint['distance from food'] == closest:
                return datapoint['food location']
        



class SquareStatus(object):

    def isOutOfBoardSquare(coord, gamedata):
        board_size = Status.getCurrentGoData(gamedata)['board dimensions']
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
        if gamedata['turn'] == 1:
            direction = 'right'
        elif gamedata['turn'] == 2:
            direction = 'down'
        else:
            current_position = Status.getMyBodyPosition(gamedata)
            next_moves_data = Assess.assessNextMoves(current_position, gamedata)
            projected_positions = next_moves_data['projected positions']        
            safe_options = next_moves_data['safe options']
            num_of_safe_options = next_moves_data['number of safe options']
            food_options = next_moves_data['food options']
            if num_of_safe_options == 0:
                direction = 'left'
            elif num_of_safe_options == 1:
                direction = Decision.convertToDirection(gamedata, safe_options[0])
            else:
                health = Status.getCurrentGoData(gamedata)['health']
                if health < 30:
                    if food_options:
                        direction = Decision.convertToDirection(gamedata, food_options[0])
                    else:
                        direction = Decision.convertToDirection(gamedata, random.choice(safe_options))
                else:
                    direction = Decision.convertToDirection(gamedata, random.choice(safe_options))
            return direction
        






