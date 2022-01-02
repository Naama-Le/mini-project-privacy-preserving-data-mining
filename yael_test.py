from player import Player


def main():
    player = Player(4, 1, None)
    d = {
        'Age': '21-25',
        'CAEC': '1',
        'FAF': '0',
        'FAVC': 'yes',
        'Gender': 'Male',
        'Height': '1.61-1.7',
        'OFH': 'yes',
        'Weight': '81-95'
    }
    print(player.get_db())
    # print(player.get_Tac(d, 'Obesity'))
    # print(player.get_Tac(d, 'Normal'))
    # print(player.get_Tai(d))


if __name__ == "__main__":
    main()
