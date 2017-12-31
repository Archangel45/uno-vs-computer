import random

# Colors and types for setting up the cards
COLORS = ["red", "green", "blue", "yellow"]
TYPES = ["skip", "draw-2", "reverse"]
SP_TYPES = ["wild", "wild-draw-4"]

def make_deck():
    "Make a new deck."

    generated_deck = [] # The deck itself, empty at the moment.

    # Generate the color cards.
    for color in COLORS:

        # Add a pair of ranks.
        for rank in range(10):
            if rank != 0:
                for i in range(2): # Make a pair if non-zero.
                    generated_deck.append(color + "-" + str(rank))
            else:
                generated_deck.append(color + "-" + str(rank)) # Add a single 0 for each color.

        # Add a pair of rank types.
        for rank_type in TYPES:
            for i in range(2):
                generated_deck.append(color + "-" + rank_type)

    # Generate the special type cards.
    for sp_type in SP_TYPES:
        for i in range(4): # add 4 each.
            generated_deck.append(sp_type)

    random.shuffle(generated_deck)

    return generated_deck

def draw_card(deck, draw_number):
    "Draw a card depending how many it will be drawn."

    # We need a copy since we'll be deleting the first 7 in the list.
    draw_copy = deck[0:draw_number]
    del deck[0:draw_number]

    return draw_copy

def find_card(hand, card):
    "Find the card in the player's hand."

    try:
        if hand.index(card):
            return True
    except ValueError:
        return False

def card_compare(card1, card2):
    "Compare card 1's match to card 2's."

    # Split the two contents so that it can be parsed.
    # I also put maxsplit so that the 'draw-2' part can't be splitted.
    # Ex: ['blue', 'draw-2']

    if "-" in card1 and "-" in card2:
        c1_content = card1.split(sep='-', maxsplit=1)
        c2_content = card2.split(sep='-', maxsplit=1)

        # It is assumed to be a color card.
        if ((c1_content[0] == c2_content[0]) or (c1_content[1] == c2_content[1])):
            return True

    # It is assumed to be a wildcard.
    if card1 in SP_TYPES or card2 in SP_TYPES:
        return True
    # If all the above failed, return False.
    else:
        return False

def play_card(hand, card_index, discard_pile):
    "Discard the card into play."

    copied_card = hand[card_index] # Copy this card on the located index.

    if not discard_pile:
        del hand[card_index]
        discard_pile.append(copied_card) # Put this to the discard pile.
    elif card_compare(hand[card_index], discard_pile[-1]): # If it matches.
        del hand[card_index]
        discard_pile.append(copied_card) # Put this to the discard pile.

def do_action(hand, deck, discard_pile):
    "Do an action depending on the top of the discard pile."

    top_discard_card = discard_pile[-1]

    if top_discard_card == "wild-draw-4":
        print("The draw 4 wildcard has been played. The game will automatically draw 4 cards for you.")
        new_4_cards = ' '.join(deck[0:4])
        hand += draw_card(deck, 4)
        print("The new cards are:", new_4_cards)

    elif top_discard_card.endswith("draw-2"):
        top_discard_card_color = top_discard_card.split("-")[0]
        print("The draw 2 card from the color", top_discard_card_color, "has been played. The game will \
automatically draw 2 cards for you.")
        new_2_cards = ' '.join(deck[0:2])
        hand += draw_card(deck, 2)
        print("The news cards are", new_2_cards)

def main():
    """\
    This is the main function of the program.

    This function will be called immediately at start of execution."""

    my_deck = make_deck()
    my_hand = draw_card(my_deck, 7)

    discard_pile = []

    beginning = True # If the game has just started
    game_over = False

    while not game_over:

        if beginning:
            print("Drop a card to the discard pile to start.\n")
        else:
            print("Pick the right card to drop to the discard pile.\n")

        if discard_pile: # Show this to stdout if there's at least 1 card.
            print("Current play:", discard_pile[-1])

        for card in enumerate(my_hand, start=1):
            print(str(card[0]) + ":", card[1])

        repeat_process = True

        while repeat_process:
            print("Number of cards in deck:", len(my_deck))
            try:
            	selected_card = int(input("Select card (0 to draw, -1 to check hand): "))
            except ValueError:
            	continue # Ignore the error and continue to loop.

            if selected_card <= len(my_hand) and selected_card >= 1:
                play_card(my_hand, selected_card-1, discard_pile)
                do_action(my_hand, my_deck, discard_pile) # Do an action

                repeat_process = False
            elif selected_card == 0:
                my_hand += draw_card(my_deck, 1)
                print("New card has been added to your hand ({})".format(my_hand[-1]))
                continue
            elif selected_card == -1:
                if discard_pile: # Show this to stdout if there's at least 1 card
                    print("Current play:", discard_pile[-1])

                for card in enumerate(my_hand, start=1):
                    print(str(card[0]) + ":", card[1])
                continue
            else:
                print("Please pick a number that is shown at the screen.")
                continue

if __name__ == "__main__":
    main()
