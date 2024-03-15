import random
from flask import *

app = Flask(__name__)
app.secret_key = "secret_key"

#open home page
@app.route('/')
def index():
    return render_template('index.html')

#submit play information into a session
@app.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        player1_name = request.form['player1']
        player2_name = request.form['player2']
        session['player1'] = {'name': player1_name, 'score': 0}
        session['player2'] = {'name': player2_name, 'score': 0}
        session['current_player'] = 'player1'
        return redirect(url_for('play')) #play.html

#assures that player names are stored in session, carries names over to play page    
@app.route('/play')
def play():
    if 'player1' in session and 'player2' in session: #checks both players data is present
        player1 = session['player1']
        player2 = session['player2']
        current_player = session['current_player']
        current_player_name = session[current_player]['name']
        dice_value = session.get('dice_value', 0) #retrieves value stored in dice_value key

        win_message = check_win()
        return render_template('play.html', 
                            player1=session['player1'], 
                            player2=session['player2'], 
                            dice_value=dice_value, 
                            current_player_name=session[current_player]['name'], 
                            win_message=win_message) #passes values to template
    else:
        return redirect(url_for('index'))

#button to carry out action of rolling the die
@app.route('/roll', methods=['POST'])
def roll():
    if 'player1' in session and 'player2' in session:
        dice_value = roll_dice()
        session['dice_value'] = dice_value
        
        return redirect(url_for('play'))
    else:
        return redirect(url_for('index'))

#action of rolling the die    
def roll_dice():
    current_player = session['current_player']
    dice_value = random.randint(1, 6)

    if dice_value == 1:
        session[current_player]['score'] = 0 #returns a player's score to 0 if a 1 is rolled
        current_player = pass_turn()
    else: 
        session[current_player]['score'] += dice_value #updates player's score
    return dice_value

#checks if a win condition is met
def check_win():
    current_player = session['current_player']
    if session[current_player]['score'] >= 20:
        return f"{session[current_player]['name']} wins!"
    else: 
        return None

#button to pass turn to other player    
@app.route('/pass', methods=['POST'])
def pass_turn():
    if 'player1' in session and 'player2' in session:
        current_player = session['current_player']
        session['current_player'] = 'player2' if current_player == 'player1' else 'player1'
        return redirect(url_for('play'))
    else:
        return redirect(url_for('index'))

#button to leave the game and return to homepage
@app.route('/quit', methods=['GET'])
def quit():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)