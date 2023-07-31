# PBNGenerateRandomHands.py
# version 1 - Initial version
# version 2 - Change to implement option to reject boards if no hand is greater than 11 points
# This is part of the PBN_Generator app
# This module generates a random deal of 52 cards and divides them in 4.
# The passed parameter, dealer, is one of N,E,W or S.  The returned result has the cards sorted into 4 hands with each suit sorted in order.
# The order of the suits is spades,hearts,diamonds,clubs.  The order of the 4 hands starts with the dealer and goes clockwise.

import random

convert_card = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
convert_back = {"14": "A", "13": "K", "12": "Q", "11": "J", "10": "T"}


def sort_suit(suit_list):
    """
    This function sorts a suit in the order AKQJT98765432 returning a string.
    If no cards in suit return empty string
    """
    sorted_suit = ""
    if len(suit_list) > 0:
        suit_list.sort(reverse=True)  # Sort cards into descending order
        # Converts high numbers back into honour cards
        for i in suit_list:
            if i > 9:
                den = convert_back[str(i)]
            else:
                den = str(i)
            sorted_suit = sorted_suit + den
    return sorted_suit


def sort_hand(hand):
    """
    This function sorts the cards in a random hand into suits in the order S,H,D,C and sorts each
    suit in the order AKQJT9876542. Convert honour cards into numbers so that they can be sorted.
    """
    hand_spades = []
    hand_hearts = []
    hand_diamonds = []
    hand_clubs = []
    for card in hand:
        den = card[0:1]
        suit = card[1:2]

        if den.isalpha():
            num = convert_card[den]
        else:
            num = int(den)
        if suit == "S":
            hand_spades.append(num)
            continue
        if suit == "H":
            hand_hearts.append(num)
            continue
        if suit == "D":
            hand_diamonds.append(num)
            continue
        hand_clubs.append(num)
    # The following code is better, but match/case is a new feature in Python 3.10
    # and pyinstaller does not seem to handle it - it generate a 'module PBNGenRandomHands
    # not found' error at run time.
    # match suit:
    #     case 'S': handspades.append(num)
    #     case 'H': handhearts.append(num)
    #     case 'D': handdiamonds.append(num)
    #     case 'C': handclubs.append(num)

    # Sort each of the suits into descending order and concatenate them with a '.' between each suit
    sorted_spades = sort_suit(hand_spades)
    sorted_hearts = sort_suit(hand_hearts)
    sorted_diamonds = sort_suit(hand_diamonds)
    sorted_clubs = sort_suit(hand_clubs)
    sorted_hand = (
        sorted_spades + "." + sorted_hearts + "." + sorted_diamonds + "." + sorted_clubs
    )
    return sorted_hand


SPADES = [
    "AS",
    "KS",
    "QS",
    "JS",
    "TS",
    "9S",
    "8S",
    "7S",
    "6S",
    "5S",
    "4S",
    "3S",
    "2S",
]
HEARTS = [
    "AH",
    "KH",
    "QH",
    "JH",
    "TH",
    "9H",
    "8H",
    "7H",
    "6H",
    "5H",
    "4H",
    "3H",
    "2H",
]
DIAMONDS = [
    "AD",
    "KD",
    "QD",
    "JD",
    "TD",
    "9D",
    "8D",
    "7D",
    "6D",
    "5D",
    "4D",
    "3D",
    "2D",
]
CLUBS = [
    "AC",
    "KC",
    "QC",
    "JC",
    "TC",
    "9C",
    "8C",
    "7C",
    "6C",
    "5C",
    "4C",
    "3C",
    "2C",
]


def generate_random_hand(dealer, passed_out):
    """
    This is the function that is called in this module.
    It generates a board with random hands but if the 'passed_out' option is set to '1' it will check that at least one
    hand has more than 11 points otherwise it will reject the board and generate a new one.
    Shuffle a pack of 52 playing cards
    """
    less_than_11 = True
    while less_than_11:
        cards = SPADES + HEARTS + DIAMONDS + CLUBS
        random.shuffle(cards)

        # Divide shuffled into 4 hands
        north_hand = cards[0:13]
        east_hand = cards[13:26]
        south_hand = cards[26:39]
        west_hand = cards[39:52]
        if passed_out == "1":
            less_than_11 = check_passed_out_hand(
                north_hand, east_hand, south_hand, west_hand
            )
        else:
            less_than_11 = False
    # Sort the hands
    n = sort_hand(north_hand)
    e = sort_hand(east_hand)
    s = sort_hand(south_hand)
    w = sort_hand(west_hand)

    if dealer == "N":
        result = dealer + ":" + n + " " + e + " " + s + " " + w
    if dealer == "E":
        result = dealer + ":" + e + " " + s + " " + w + " " + n
    if dealer == "S":
        result = dealer + ":" + s + " " + w + " " + n + " " + e
    if dealer == "W":
        result = dealer + ":" + w + " " + n + " " + e + " " + s
    return result


# check hands to make sure one has at least 11 HCP.
def check_passed_out_hand(north, east, south, west):
    if hcp_count(north) > 11:
        return False
    if hcp_count(east) > 11:
        return False
    if hcp_count(south) > 11:
        return False
    if hcp_count(west) > 11:
        return False
    return True


def hcp_count(hand):
    hcp = 0
    for card in hand:
        value = card[:1]
        if value == "A":
            hcp += 4
            continue
        if value == "K":
            hcp += 3
            continue
        if value == "Q":
            hcp += 2
            continue
        if value == "J":
            hcp += 1
            continue
    # The following code is better, but match/case is a new feature in Python 3.10
    # and pyinstaller does not seem to handle it - it generate a 'module PBNGenRandomHands
    # not found' error at run time.
    # match Value:
    #     case 'A': HCP+=4
    #     case 'K': HCP+=3
    #     case 'Q': HCP+=2
    #     case 'J': HCP+=1
    return hcp
