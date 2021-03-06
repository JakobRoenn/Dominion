import random


class Card:
    def __init__(self, name, type, cost, gold=0, vp=0, draw=0, actions=0, buys=0):
        self.name = name
        self.cost = cost
        self.type = type
        self.gold = gold
        self.vp = vp
        self.draw = draw
        self.actions = actions
        self.buys = buys


class Player:
    def __init__(self, name, deck, top_deck, hand, discard):
        self.name = name
        self.deck = deck
        self.top_deck = top_deck
        self.hand = hand
        self.discard = discard


def draw_from_deck(p):
    if len(p.top_deck) != 0:
        print(len(p.top_deck), p.top_deck)
        n_c = p.top_deck.pop[0]
        p.hand.append(n_c)
    else:
        if len(p.deck) != 0:
            draw = random.randrange(len(p.deck))
            card = p.deck.pop(draw)
            p.hand.append(card)
        else:
            p.deck = p.discard
            p.discard = []
            draw_from_deck(p)


def get_top_card(p):
    if len(p.top_deck) != 0:
        top_card = (p.top_deck.pop[0])
    else:
        if len(p.deck) != 0:
            draw = random.randrange(len(p.deck))
            top_card = p.deck.pop(draw)
        else:
            p.deck = p.discard
            p.discard = []
            top_card = get_top_card(p)
    return top_card


def cards_in_hand_print(hand):
    print("Cards in hand:", end=" ")
    for card in hand:
        print(card.name, end=", ")
    print("")


def card_in_list(list, text):
    i = 1
    for c in list:
        print(i, ":", c.name)
        i += 1
    print(text)
    c_c = int(input(" ")) - 1
    if c_c == -1:
        return False
    else:
        bob = list[c_c]
        return bob


def gain_card(max_cost, type=""):
    temp_list = []
    for s in stacks:
        if s[0].cost < max_cost+1 and type in s[0].type and s[1] != 0:
            temp_list.append(s[0])
    i = 1
    for t in temp_list:
        print(i, ":", t.name)
        i += 1
    print("Choose card to gain")
    c_c = int(input("")) - 1
    p.discard.append(temp_list[c_c])
    for s in stacks:
        if s[0] == temp_list[c_c]:
            s[1] -= 1


def play_action_card(a_c, gold, actions, buys):
    in_play.append(a_c)
    gold += a_c.gold
    actions += a_c.actions
    buys += a_c.buys
    for _ in range(a_c.draw):
        draw_from_deck(p)
    if "classic" in sets_in_play:
        gold, actions, buys = dominion_basic_actions(a_c, gold, actions, buys)
    if "classic_1e" in sets_in_play:
        gold, actions, buys = dominion_1e_actions(a_c, gold, actions, buys)
    if "classic_2e" in sets_in_play:
        gold, actions, buys = dominion_2e_actions(a_c, gold, actions, buys)
    return gold, actions, buys


def dominion_basic_actions(a_c, gold, actions, buys):
    if a_c == cellar:
        for _ in range(len(p.hand)):
            c_c = card_in_list(p.hand, "Choose card to discard. 0 = none")
            if c_c == False:
                break
            else:
                p.discard.append(p.hand.pop(c_c))
                draw_from_deck(p)
    elif a_c == chapel:
        d = 0
        while d < 4:
            c_c = card_in_list(p.hand, "Choose card to trash. 0 = none")
            if c_c == False:
                break
            else:
                p.hand.remove(c_c)
                d += 1
    elif a_c == workshop:
        gain_card(4)
    elif a_c == bureaucrat:
        if stacks[1][1] != 0:
            p.top_deck.insert(0, silver)
            stacks[1][1] -= 1
        for o in other_players:
            if check_for_moat(o):
                continue
            else:
                for c in o.hand:
                    if "v" in c.type:
                        o.top_deck.insert(0, o.hand.pop(c))
                        continue
                cards_in_hand_print(o.hand)
    elif a_c == militia:
        for o in other_players:
            if check_for_moat(o):
                continue
            else:
                while len(o.hand) > 3:
                    c_c = card_in_list(o.hand, o.name + ", choose card to discard")
                    o.discard.append(c_c)
                    o.hand.remove(c_c)
    elif a_c == moneylender:
        for c in p.hand:
            if c == copper:
                p.hand.remove(c)
                gold += 3
                break
    elif a_c == remodel:
        c_c = card_in_list(p.hand, "chose card to thrash")
        gain_card(c_c.cost + 2)
    elif a_c == throne_room:
        c_c = card_in_list(p.hand, "Choose action card, and then play it twice")
        if "a" in c_c.type:
            gold, actions, buys = play_action_card(c_c, gold, actions, buys)
            gold, actions, buys = play_action_card(c_c, gold, actions, buys)
            in_play.remove(c_c)

    elif a_c == council_room:
        for o in other_players:
            draw_from_deck(o)
    elif a_c == library:
        set_aside = []
        while len(p.hand) < 8:
            top_card = get_top_card(p)
            if "a" in top_card.type:
                print("set aside", top_card.name, "? Yes = 1")
                sa = input("")
                if sa == "1":
                    set_aside.append(top_card)
                else:
                    p.hand.append(top_card)
            else:
                p.hand.append(top_card)
        p.discard += set_aside
    elif a_c == mine:
        c_c = card_in_list(p.hand, "Choose treasure to trash")
        if "t" in c_c.type:
            p.hand.remove(c_c)
            gain_card(c_c.cost + 3, "t")
            p.hand.append(p.discard[len(p.discard) - 1])
    elif a_c == witch:
        for o in other_players:
            if stacks[6][1] != 0:
                o.discard.append(curse)
                stacks[6][1] -= 1
    return gold, actions, buys


def check_for_moat(o):
    for c in o.hand:
        if c == moat:
            print(o.name, "has a moat")
            return True


def dominion_1e_actions(a_c, gold, actions, buys):
    if a_c == chancellor:
        print("Put deck in discard pile? yes = 1")
        a_r = input("")
        if a_r == "1":
            p.discard.append(p.deck)
            p.deck = []
    elif a_c == feast:
        in_play.remove(a_c)
        gain_card(5)
    elif a_c == spy:
        for ap in players:
            if check_for_moat(ap):
                continue
            else:
                c_c = get_top_card(ap)
                print(ap.name + "'s top card is", c_c.name, ". Discard (1) or return to deck (2)")
                c_a = input("")
                if c_a == "1":
                    ap.discard.append(c_c)
                if c_a == "2":
                    ap.top_deck.insert(0, c_c)
    elif a_c == thief:
        t_t = []
        for o in other_players:
            if check_for_moat(o):
                continue
            else:
                t_r = []
                for _ in range(2):
                    c_c = get_top_card(o)
                    if "t" in c_c.type:
                        t_r.append(c_c)
                    else:
                        o.discard.append(c_c)
                if len(t_r) == 1:
                    t_t.append(t_r[0])
                if len(t_r) > 1:
                    c_c = card_in_list(t_r, "Choose treasure to thrash")
                    t_t.append(c_c)
                    t_r.remove(c_c)
                    o.discard += t_r
        c_c = card_in_list(t_t, "Choose treasure to gain")
        p.discard.append(c_c)
    elif a_c == adventurer:
        t_c = 0
        while t_c != 2:
            top_card = get_top_card(p)
            print("You drew:", top_card.name)
            if "t" in top_card.type:
                p.hand.append(top_card)
                t_c += 1
            else:
                p.discard.append(top_card)
    return gold, actions, buys


def dominion_2e_actions(a_c, gold, actions, buys):
    if a_c == artisan:
        gain_card(5)
        p.hand.append(p.discard[len(p.discard)-1])
        c_c = card_in_list(p.hand, "Choose card to put on top of deck")
        p.top_deck.insert(0, c_c)
    elif a_c == bandit:
        p.discard.append(gold)
        stacks[2][1] -= 1
        for o in other_players:
            if check_for_moat(o):
                continue
            else:
                r_t = []
                for _ in range(2):
                    c_d = get_top_card(o)
                    print(o.name, "reveal", c_d.name)
                    if "t" in c_d.type and c_d != copper:
                        r_t.append(c_d)
                    else:
                        o.discard.append(c_d)
                if len(r_t) == 2:
                    c_c = card_in_list(r_t, (o.name, ", choose treasure to trash"))
                    r_t.remove(c_c)
                    o.discard += r_t
    elif a_c == harbinger:
        c_c = card_in_list(p.discard, "Choose card to put on top of deck")
        if c_c != False:
            p.top_deck.insert(0, c_c)
    elif a_c == poacher:
        e_p = 0
        for st in stacks:
            if st[1] == 0:
                e_p += 1
        for _ in range(e_p):
            c_c = card_in_list(p.hand, "Choose card to discard")
            p.discard.append(c_c)
    elif a_c == sentry:
        c_l = []
        for _ in range(2):
            c_l.append(get_top_card(p))
        while len(c_l) != 0:
            c_c = card_in_list(c_l, "Choose card to discard or trash. 0 = none")
            if c_c == False:
                break
            else:
                print("Discard (1) or trash (2)", c_c.name)
                t_d = input("")
                if t_d == "1":
                    p.discard.append(c_c)
                c_l.remove(c_c)
            if len(c_l) == 2:
                print(c_l[1].name, "is going to be top card. Want", c_l[0].name, "instead. Yes =1" )
                ans = input("")
                if ans == "1":
                    c_l.reverse()
            for c in c_l:
                p.top_deck.insert(0, c)
    elif a_c == vassal:
        t_c = get_top_card(p)
        ans = "bob"
        if "a" in t_c.type:
            print("Play", t_c+"? Yes = 1")
            ans = input("")
        else:
            print("You drew", t_c)
        if ans == "1":
            gold, actions, buys = play_action_card(t_c, gold, actions, buys)

    return gold, actions, buys


# Basic cards
copper = Card("copper", "t", 0, 1, 0)
silver = Card("silver", "t", 3, 2, 0)
gold = Card("gold", "t", 6, 3, 0)
estate = Card("estate", "v", 2, 0, 1)
duchy = Card("duchy", "v", 5, 0, 3)
province = Card("province", "v", 8, 0, 6)
curse = Card("curse", "v", 0, 0, -1)

# Classic cards
cellar = Card("cellar", "a", 2, 0, 0, 0, 1)
chapel = Card("chapel", "a", 2)
moat = Card("moat", "ar", 2, 0, 0, 2)
chancellor = Card("chancellor", "a", 3, 2)
village = Card("village", "a", 3, 0, 0, 1, 2)
woodcutter = Card("woodcutter", "a", 3, 2, 0, 0, 0, 1)
workshop = Card("workshop", "a", 3)
bureaucrat = Card("bureaucrat", "a", 4)
feast = Card("feast", "a", 4)
gardens = Card("gardens", "v", 4)
militia = Card("militia", "a", 4, 2)
moneylender = Card("moneylender", "a", 4)
remodel = Card("remodel", "a", 4)
smithy = Card("smithy", "a", 4, 0, 0, 3)
spy = Card("spy", "a", 4, 0, 0, 1, 1)
thief = Card("thief", "a", 4)
throne_room = Card("throne room", "a", 4)
council_room = Card("council room", "a", 5, 0, 0, 4, 0, 1)
festival = Card("festival", "a", 5, 2, 0, 0, 2, 1)
laboratory = Card("laboratory", "a", 5, 0, 0, 2, 1)
library = Card("library", "a", 5)
market = Card("market", "a", 5, 1, 0, 1, 1, 1)
mine = Card("mine", "a", 5)
witch = Card("witch", "a", 5, 0, 0, 2)
adventurer = Card("adventurer", "a", 6)

#  name, type, cost, gold=0, vp=0, draw=0, actions=0, buys=0
artisan = Card("artisan", "a", 6)
bandit = Card("bandit", "a", 5)
harbinger = Card("harbinger", "a", 3, 0, 0, 1, 1)
merchant = Card("merchant", "a", 3, 0, 0, 1, 1)
poacher = Card("poacher", "a", 4, 1, 0, 1, 1)
sentry = Card("sentry", "a", 5, 0, 0, 1, 1)
vassal = Card("vassal", "a", 3, 2)


dominion_classic = [cellar, chapel, moat, village, workshop, bureaucrat, gardens, militia, moneylender, remodel, smithy,
                    council_room, festival, laboratory, library, market, mine, witch]
dominion_classic_1e = [chancellor, woodcutter, feast, spy, thief, adventurer]
dominion_classic_2e = [artisan, bandit, harbinger, merchant, poacher, sentry]


# Set up players:
player_1 = Player("player 1", [], [], [], [])
player_2 = Player("player 2", [], [], [], [])
player_3 = Player("player 3", [], [], [], [])
player_4 = Player("player 4", [], [], [], [])

players = [player_1]
print("How many players?")
p_n = int(input(""))
if p_n > 1:
    players.append(player_2)
if p_n > 2:
    players.append(player_3)
if p_n > 3:
    players.append(player_4)

for p in players:
    print("rename", p.name, "?  yes = 1")
    ans = input("")
    if ans == "1":
        print("Write new name of", p.name)
        p.name = input("")
    p.deck = [copper, copper, copper, copper, copper, copper, copper, estate, estate, estate]
    for _ in range(5):
        draw_from_deck(p)


# Set up stacks:
if len(players) > 2:
    b_vp = 4
else:
    b_vp = 0

stacks = [[copper, 60-(len(players)*7)], [silver, 40], [gold, 30], [estate, 8+b_vp], [duchy, 8+b_vp],
          [province, 8+b_vp], [curse, (len(players)-1)*10]]


pos_kingdom = []
kingdom_selection = []
sets_in_play = []
print("1 = Dominion classic")
print("Choose set(s) to use")
ans = input("")
if ans == "1":
    pos_kingdom += dominion_classic
    sets_in_play.append("classic")
    print("Use first edition (1), second edition(2), or both (3)?")
    ans = input("")
    if ans == "1":
        pos_kingdom += dominion_classic_1e
        sets_in_play.append("classic_1e")
    elif ans == "2":
        pos_kingdom += dominion_classic_2e
        sets_in_play.append("classic_2e")
    else:
        pos_kingdom += dominion_classic_1e + dominion_classic_2e
        sets_in_play.append("classic_1e")
        sets_in_play.append("classic_2e")

for _ in range(10):
    r_n = random.randrange(len(pos_kingdom))
    k_c = pos_kingdom[r_n-1]
    kingdom_selection.append([k_c, 10])
    pos_kingdom.remove(k_c)
    if "v" in k_c.type:
        if len(players) > 3:
            kingdom_selection[len(kingdom_selection)-1][1] -= 2
        else:
            kingdom_selection[len(kingdom_selection)-1][1] += 2

kingdom_selection = sorted(kingdom_selection, key=lambda a: a[0].cost)
stacks += kingdom_selection

# Taking turns:
playing = True
while playing:
    for p in players:
        gold = 0
        actions = 1
        buys = 1
        in_play = []
        action_s = []
        other_players = []
        for o in players:
            if o != p:
                other_players.append(o)

        print("-----")
        print("it is", p.name+"'s turn")
        cards_in_hand_print(p.hand)
        print("deck size:", len(p.deck))
        print("discard pile size:", len(p.discard))

        # Playing action cards:
        while actions != 0:
            for card in p.hand:
                if "a" in card.type:
                    action_s.append(card)
            if len(action_s) != 0:
                print("-----")
                cards_in_hand_print(p.hand)
                i = 1
                for card in action_s:
                    print(i, card.name)
                    i += 1
                print("Actions left:", actions)
                print("Choose action card to play")
                a_c = action_s[int(input(""))-1]
                if a_c == -1:
                    actions = 0
                    continue
                p.hand.remove(a_c)
                gold, actions, buys = play_action_card(a_c, gold, actions, buys)
                action_s = []
                actions -= 1
            else:
                actions = 0

        # Buy cards:
        for card in p.hand:
            if "t" in card.type:
                gold += card.gold
            if merchant in in_play and silver in p.hand:
                for merchant in p.hand:
                    gold += 1
        while buys != 0:
            i = 1
            print("-----")
            cards_in_hand_print(p.hand)
            for s in stacks:
                if s[1] != 0:
                    print(i, s[0].name, "cost:", s[0].cost, "left:", s[1])
                    i += 1
                else:
                    print(i, s[0].name, "is sold out")
                    i += 1
            print("Gold:", gold)
            print("You have", buys, "buys left")
            print("What do you want to buy?")
            buy = int(input(""))-1
            if buy == -1:
                buys = 0
                continue
            if stacks[buy][1] == 0:
                print("Out of stock")
            elif stacks[buy][0].cost < gold+1:
                p.discard.append(stacks[buy][0])
                stacks[buy][1] -= 1
                gold -= stacks[buy][0].cost
                buys -= 1
            else:
                print("You cannot afford that")

        # Clean-up
        for card in p.hand:
            p.discard.append(card)
        p.hand = []
        for card in in_play:
            p.discard.append(card)
        if len(in_play) != 0:
            in_play = []

        # Draw new hand
        for _ in range(5):
            draw_from_deck(p)

        # Check for game end
        if stacks[5][1] == 0:
            playing = False
        e_s = 0
        for s in stacks:
            if s[1] == 0:
                e_s += 1
        if e_s > 2:
            playing = False

# Final score
print("-----")
for p in players:
    v_p = 0
    p.discard += p.hand
    p.discard += p.deck
    for c in p.discard:
        if "v" in c.type:
            v_p += c.vp
            if c == gardens:
                v_p += len(p.discard)/10
    print(p.name, "got", v_p, "points")
