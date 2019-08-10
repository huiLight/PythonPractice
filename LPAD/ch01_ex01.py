import random
import textwrap

def show_theme_message(width=72):
    show_dotted_line()
    print("\033[lm"+"Attack of The Orcs v0.0.1:" + "\033[0m")

    msg = (
        "The war between humans and their arch enemies, Orcs, was in the "
        "offing. Sir Foo, one of the brave knights guarding the southern "
        "plains began a long journey towards the east through an unknown "
        "dense forest. On his way, he spotted a small isolated settlement."
        " Thired and hoping to replenish his food stock, he decided to take"
        " a datour. As he approached the village, he saw five huts. There "
        "was no one to be seen around. Hesitantly, he decided to enter..")

    print(textwrap.fill(msg, width=width))


def show_game_mission():
    print('\033[1m' + "Mission:" +"\033[0m")
    print("\tChoose a hut where Sir Foo can rest...")
    print("\033[1m" + "TIP:" + "\033[0m")
    print("Be careful as there are enemies luking around!")
    show_dotted_line()


def occupy_huts():
    occupants = ['enemy', 'friend', 'unoccupied']
    huts = []
    # Randomly append 'enemy' or 'friend' or None to the huts list
    while len(huts) < 5:
        computer_choice = random.choice(occupants)
        huts.append(computer_choice)
    return huts


def process_user_choice():
    # Prompt user to select a hut
    msg = "\033[1m" + "Choose a hut number to enter (1-5):" + "\033[0m"
    user_choice = input("\n" + msg)
    idx = int(user_choice)

    # Print the occupant info
    print("Revealing the occupants...")
    
    return idx


def reveal_occupants(idx, huts):
    msg = ""
    for i in range(len(huts)):
        occupant_info = '<%d:%s>'%(i+1, huts[i])
        if i + 1 == idx:
            occupant_info = "\033[1m" + occupant_info + "\033[0m"
        msg += occupant_info + " "
    print("\t" + msg)
    show_dotted_line()


def enter_hut(idx, huts):
    print("\033[1m" + "Entering hut %d... "%idx + "\033[0m", end=" ")

    # Determine and announce the winner
    if huts[idx-1] == 'enemy':
        print("\033[1m" + "YOU LOSE: (Better luck next time!)" + 
              "\033[0m")
    else:
        print("\033[1m" + "Congratulations! YOU WIN!!!" + "\033[0m")
    show_dotted_line()


def print_bold(msg, end='\n'):
    """Print a string in 'bold' font"""
    print("\033[1m" + msg + "\033[0m", end=end)


def show_dotted_line(width=72):
    print('-' * width)


def reset_health_meter(health_meter):
    health_meter['player'] = 40
    health_meter['enemy'] = 30


def run_application():
    keep_playing = 'y'
    health_meter = {}

    show_theme_message()
    show_game_mission()
    while keep_playing == 'y':
        reset_health_meter(health_meter)
        play_game(health_meter)

        keep_playing = input("Play again? Yes(y)/No(n):")


def show_health(health_meter, bold=False):
    msg = "Sir Foo: {}, Enemy: {}".format(health_meter['player'], 
        health_meter['enemy'])
    if bold:
        msg = "\033[1m" + msg + "\033[0m"
    print(msg)


def play_game(health_meter):
    huts = occupy_huts()
    idx = process_user_choice()
    reveal_occupants(idx, huts)

    if huts[idx-1] != 'enemy':
        print_bold("Congratulations! YOU WIN!!!")
    else:
        print_bold("ENEMY SIGHTED! ", end='')
        show_health(health_meter, bold=True)
        continue_attack = True

        while continue_attack:
            continue_attack = input("....continue attack? (y/n):")
            if continue_attack == 'n':
                print_bold("RUNNING AWAY with folloing health dtatus..")
                show_health(health_meter, bold="True")
                print_bold("Game Over!")

            attack(health_meter)

            if health_meter['enemy'] <= 0:
                print_bold("Good Job! Enemy defeated! YOU WIN!!!")
                break
            if health_meter['player'] <= 0:
                print_bold("YOU LOSE! Better luck next time")
                break



def attack(health_meter):
    hit_list = 4 * ['player'] + 6 * ['enemy']
    injured_unit = random.choice(hit_list)
    hit_points = health_meter[injured_unit]
    injury = random.randint(10, 15)
    health_meter[injured_unit] = max(hit_points-injury, 0)
    print("ATTACK!", end='')
    show_health(health_meter)


if __name__ == '__main__':
    run_application()