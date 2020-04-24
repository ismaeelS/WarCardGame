import random

def compare_cards(p1_name, p2_name, card1, card2, ranks=['2','3','4','5','6','7','8','9','10','J','Q','K','A']):
  """Compares two cards by card rank

  Arguments are passed as strings in the format 'XY' where X is the card rank and Y is the first letter of the suite.
  Prints out the comparison and the comparison results.

  Parameters
  ----------
    p1_name: str
    p2_name: str
    card1 : str
    card2 : str
      
  Raises
  ------
  ValueError
    If the rank of card1 or card2 is not in the accepted list of ranks.
  
  Returns
  -------
  Integer
    an integer corresponding to whether there was a tie (0), first card won (1),
    or the second card won (2)
  """

  rank1, rank2 = card1[:-1], card2[:-1]

  if rank1 not in ranks: raise ValueError("Card 1 does not have a valid card value!")
  if rank2 not in ranks: raise ValueError("Card 2 does not have a valid card value!")

  print(p1_name+"\'s", card1, "vs.", p2_name+"\'s", card2)

  winner = -1

  if (rank1 == rank2): winner = 0
  elif (rank1 == '2' and rank2 == 'A'): winner = 1
  elif (rank1 == 'A' and rank2 == '2'): winner = 2
  else: winner = 1 if (ranks.index(rank1) > ranks.index(rank2)) else 2

  if (winner == 0): print("There Was a Tie Between", card1, "and", card2)
  elif (winner == 1): print(p1_name, "Wins This Round With a", card1, "Against a", card2)
  elif (winner == 2): print(p2_name, "Wins This Round With a", card2, "Against a", card1)

  return winner

def checkDeckOut(p1, p2):
  """Checks which player, if any, decks out

  Prints out any deck outs and the corresponding winner from the deck out.

  Parameters
  ----------
    p1: obj
    p2: obj
      
  Returns
  -------
  Integer
    an integer corresponding to whether both players deck out (0), 
    the first player decks out (1), the second player decks out (2)
    or neither (-1)
  """

  if (len(p1.deck)==len(p2.deck)==0):
    print("Both Players Have Decked Out")
    return 0
  elif (len(p1.deck) == 0):
    print(p1.name, "has Decked Out.", p2.name, "Wins.")
    return 1
  elif (len(p2.deck) == 0):
    print(p2.name, "has Decked Out.", p1.name, "Wins.")
    return 2
  else:
    return -1

def update_cards(p1, p2, p1_cards, p2_cards):
  """Adds topdeck from each deck to hand if possible

  Checks if each players has decked out. If there are any deck outs, drawn cards, if any (uses len() to check), are added to the appropriate decks and an empty list is returned.
  If neither deck would deck out from drawing one card, add each player's drawn card to their respective hands of drawn cards. Return these hands.
  
  If any player has decked out, instead returns an empty list.

  Parameters
  ----------
    p1: obj
    p2: obj
    p1_cards: list
      player one's current list of cards that can be lost to opponent
    p2_cards: list
      player two's current list of cards that can be lost to opponent
  
  Returns
  -------
  Empty List
    empty list is returned if either player decks out
  Tuple
    tuple containing player one's updated list of cards and player two's updated list of cards
  """

  out_of_cards = checkDeckOut(p1, p2)

  # if neither player decks out, skip rest of checks
  if (out_of_cards == -1): pass
  #both players deck out
  elif (out_of_cards == 0):
    if (len(p1_cards) > 0): p1.deck.add_cards(p1_cards)
    if (len(p2_cards) > 0): p2.deck.add_cards(p2_cards)
  else:
    if (len(p1_cards+p2_cards) > 0):
      if (out_of_cards == 1): p2.deck.add_cards((p1_cards+p2_cards))
      else: p1.deck.add_cards((p1_cards+p2_cards))
  # else: (above else same function as below else. different syntax)
    # (len(p1_cards+p2_cards) > 0) and ((p2.deck.add_cards((p1_cards+p2_cards))) if (out_of_cards == 1) else p1.deck.add_cards((p1_cards+p2_cards)))

  # if out_of_cards >= 0 then at least one player has decked out
  if (out_of_cards >= 0):
    return []
  
  p1_cards.append(p1.deck.remove_card())
  p2_cards.append(p2.deck.remove_card())

  return p1_cards, p2_cards
  
def exitStatement(reason):
  """Ends game and prints reason for it

  Parameters
  ----------
    reason: str
      reason is a key that corresponds to a value in the reasons dict to print out
  
  """

  reasons = {
    "Game Loop": "This State Has Been Seen Before. In a Game Loop.",
    "Normal Deck Out": "Deck Out While Comparing Topdecks",
    "Tie Comparison Deck Out 1": "Deck Out While Adding Middle Card During a Tie",
    "Tie Comparison Deck Out 2": "Deck Out While Adding Last Card During a Tie",
    "Turn Limit": "Reached Turn Limit of "
  }
  return "\nGame Over: "+reasons[reason]

def get_turn_limit():
  
    message = "Enter a limit to the number of turns allowed in this game. Any input that is not an integer equal to or greater than 0 will set the turn limit to 1000\n"

    try:
      turn_limit = int(input(message))
      turn_limit = 1000 if turn_limit < 0 else turn_limit
    except ValueError:
      turn_limit = 1000
      return 1000
    else:
      return turn_limit
    finally:
      print('Turn limit set. This game will have at most', turn_limit, 'turns.')

def get_number_of_turns_to_play():

  print()
  message = "Enter number of turns to play. Any input that's not an integer greater than 1 will move game to next hand.\n"

  try:
    turns_to_play = int(input(message))
    turns_to_play = 1 if turns_to_play < 2 else turns_to_play
  except ValueError:
    return 1
  else:
    if (turns_to_play > 1):
      print('Attempting to play', turns_to_play, 'turns.')
    return turns_to_play 

class PlayingCards():
  """
  A class used to represent a deck of playing cards

  ...

  Attributes
  ----------
  cards : list
    a list of cards in the deck

  Methods
  -------
  shuffle()
    Rearranges the order of the cards
  split()
    Splits all the cards into even piles
  """

  def __init__(self, ranks=['2','3','4','5','6','7','8','9','10','J','Q','K','A'], suites=['H','D','S','C']):
    """
    Parameters
    ----------
    ranks : char list
      list of all card ranks
    suites : char list
      list of all card suites (by first letter)
    """

    self.cards = [r+s for r in ranks for s in suites]

  def shuffle(self):
    random.shuffle(self.cards)

  def split(self):
    '''
    split gives every other card to each player. this way in case shuffle() is not called, it's a tie and not a win for second player who has the bigger ranked cards
    '''
    return [self.cards[::2], self.cards[1::2]]

class Deck():

  def __init__(self, cards = []):
    self.cards = cards
  
  def __len__(self):
    return len(self.cards)

  def add_cards(self, cards):
    self.cards.extend(cards)

  def remove_card(self):
    if (len(self.cards) > 0):
      removed = self.cards[0]
      del self.cards[0]
      return removed

class Player():

  def __init__(self, name, cards = []):
    self.name = name
    self.deck = Deck(cards)

  def battle(self, opponent):
    print() #CHECK IF NEEDED

    own_cards = []
    opp_cards = []

    updated_cards = update_cards(self, opponent, own_cards, opp_cards)

    if (updated_cards == []):
      return exitStatement("Normal Deck Out")
  
    own_cards, opp_cards = updated_cards

    winner = compare_cards(self.name, opponent.name, own_cards[-1], opp_cards[-1])

    #handle tie
    while (winner == 0):

      cards_at_stake = 0
      # try to add the next two cards from each deck
      # second card will be used to determine winner
      while (cards_at_stake < 2):
        #check if either has decked out
        updated_cards = update_cards(self, opponent, own_cards, opp_cards)

        if (updated_cards == []):
          return exitStatement("Tie Comparison Deck Out "+str(cards_at_stake + 1))

        own_cards, opp_cards = updated_cards

        cards_at_stake = cards_at_stake + 1

      winner = compare_cards(self.name, opponent.name, own_cards[-1], opp_cards[-1])
      print('At stake:', own_cards, opp_cards)

    if (winner == 1): self.deck.add_cards((own_cards + opp_cards))
    else: opponent.deck.add_cards((own_cards + opp_cards))
    
    print('cards after this round:', self.deck.cards, opponent.deck.cards)

    return ""

class GameOfWar():

  def __init__(self):
    self.game_over = False
    self.turns = 0
    self.turn_limit = 1000
    self.game_states = []

    self.playing_cards = PlayingCards()
    self.playing_cards.shuffle()

    # self.playing_cards.cards = '2S 2S 3S 3S 4S 5S 6S'.split() #testing
    # self.playing_cards.cards = '2S 3S AS 5S 8C 8C 2C 2C 3C 4C 8C 8C 2C 2C 4C 3C'.split() #testing 

    p1_name = input("What is player 1's name?\n")
    if (p1_name == ""): p1_name = "Player 1"

    p2_name = input("What is player 2's name?\n")
    if (p2_name == ""): p2_name = "Player 2"

    self.turn_limit = get_turn_limit() 

    self.players = []
    self.player1 = Player(p1_name, self.playing_cards.split()[0])
    self.players.append(self.player1)
    self.player2 = Player(p2_name, self.playing_cards.split()[1])
    self.players.append(self.player2)
  
  def print_game_info(self):
    print("\nEach player's deck:")
    for player in self.players:
      print(player.name+"\'s deck:", player.deck.cards)
    print(self.turns, "turns taken.")
   

  #allow printing of deck length while playing
  def play(self):

    requested_turns_played = 0
    reason_for_game_over = ""

    while (self.turns < self.turn_limit):
      if (self.game_over): break

      turns_to_play = get_number_of_turns_to_play()

      requested_turns_played = 0
      while (requested_turns_played < turns_to_play):
        if (self.turns >= self.turn_limit): break

        # check if stuck in a game loop
        current_game_state = ("".join(self.player1.deck.cards))[::2]+" "+("".join(self.player2.deck.cards))[::2]
        
        if (current_game_state in self.game_states):
          reason_for_game_over = exitStatement("Game Loop")
          self.game_over = True
          break
        else:
          self.game_states.append(current_game_state)

        reason_for_game_over = self.player1.battle(self.player2)

        if (len(reason_for_game_over) > 0):
          self.game_over = True
          break
        else:
          self.turns = self.turns + 1
        
        requested_turns_played = requested_turns_played + 1
        if (requested_turns_played == turns_to_play and requested_turns_played != 1):
          print("\nAble to play", turns_to_play, "rounds.")

    if (requested_turns_played < turns_to_play):
      print("Able to play", requested_turns_played, "of the", turns_to_play, "requested rounds due to the game ending.")

    if (not self.game_over and self.turns >= self.turn_limit):
      reason_for_game_over = exitStatement("Turn Limit")+str(self.turn_limit)

    print(reason_for_game_over)
    
    self.print_game_info()



#main control flow
game = GameOfWar()
game.print_game_info()
game.play()

#To-Do: need a discard for each player
#To-Do: Add rest of the docstrings

# Below has a game loop at round 193. can use to test
# a's deck: ['2C', '10H', '4D', '10D', '8D', '5D', '2H', '9C', '5S', 'QD', '8S', 'QS', '5H', 'JH', '4C', 'KH', '8H', 'AH', '6D', 'AD', '7D', 'QH', '3C', 'JC', '3H', '10C', '3S']
# b's deck: ['9H', '2S', '10S', '2D', 'KS', '4H', 'JD', '4S', '9D', '6S', 'JS', '7H', 'QC', '5C', 'AS', '9S', 'AC', '3D', '8C', '6C', 'KC', '7C', 'KD', '6H', '7S']

#Below has b deck out at round 318 can use to test
# a's deck: ['5S', '10S', '4D', '5D', 'KS', '10H', '8C', '6C', '7H', '6S', '8D', 'JH', '7S', 'QD', '8H', '4C', '6D', '3H', 'AD', '9C', '7D', '6H', 'QC', '5H', 'KH', '9S']
# b's deck: ['KD', '9H', '3D', '8S', '2S', 'JC', 'JD', '4S', '2D', 'AH', '4H', '3C', 'AC', '9D', 'QS', 'JS', '10C', '7C', '5C', 'AS', '3S', '2H', 'QH', '10D', 'KC', '2C']
