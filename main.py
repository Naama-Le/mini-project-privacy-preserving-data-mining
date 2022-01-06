from dealer import Dealer
from player import Player
from shared import PLAYERS
import csv

dealer = Dealer(4)


def build_tree():
    R = {
        'Age': ['<=20', '21-25', '26-35', '36+'],
        'Weight': ['<=50', '51-65', '66-80', '81-95', '96+'],
        'Height': ['<=1.6', '1.61-1.7', '1.71-1.8', '1.81+'],
        'OFH': ['yes', 'no'],
        'FAVC': ['yes', 'no'],
        'CAEC': ['0', '1', '2', '3'],
        'FAF': ['0', '1', '2', '3'],
        'Gender': ['Male', 'Female'],
    }
    C = ['Insufficient', 'Normal', 'Overweight', 'Obesity']
    dealer.build_tree(R, C)


def vals_to_str(d):
    ls = []
    for i in range(len(d)):
        ls.append(f"{i + 1}. {d[i + 1]}")
    return "\n".join(ls) + "\n"


def print_path(path):
    for i in range(len(path)):
        if i == len(path) - 1:
            print(('\t' * i + f'label: {path[i]}\n'))
        else:
            print(('\t' * i + f'node: {path[i]}'))


def run_gui():
    while True:
        print("Hello, what would you like to do?")
        ans = input("Press 1 if you'd like to predict your obesity level, or 2 if you want to leave\n")
        if int(ans) == 2:
            break
        print("Enter the corresponding number for the following questions:\n")

        print("What is your gender?")
        gender_vals = {1: "Male", 2: "Female"}
        _gender = input(vals_to_str(gender_vals))
        Gender = gender_vals[int(_gender)]

        print("How old are you?")
        age_vals = {1: "<=20", 2: "21-25", 3: "26-35", 4: "36+"}
        _age = input(vals_to_str(age_vals))
        Age = age_vals[int(_age)]

        print("What is your weight?")
        weight_vals = {1: "<=50", 2: "51-65", 3: "66-80", 4: "81-95", 5: "96+"}
        _weight = input(vals_to_str(weight_vals))
        Weight = weight_vals[int(_weight)]

        print("What is your height?")
        height_vals = {1: "<=1.6", 2: "1.61-1.7", 3: "1.71-1.8", 4: "1.81+"}
        _height = input(vals_to_str(height_vals))
        Height = height_vals[int(_height)]

        binary_vals = {1: "Yes", 2: "No"}

        print("Do you have family history of overweight?")
        _ofh = input(vals_to_str(binary_vals))
        OFH = binary_vals[int(_ofh)]

        print("Do you eat high caloric food frequently?")
        _favc = input(vals_to_str(binary_vals))
        FAVC = binary_vals[int(_favc)]

        print("Do you eat any food between meals?")
        caec_vals = {1: "No", 2: "Sometimes", 3: "Frequently", 4: "Always"}
        _caec = input(vals_to_str(caec_vals))
        CAEC = str(int(_caec) - 1)

        print("How often do you have physical activity")
        faf_vals = {1: "Never", 2: "One or two days", 3: "Two or four days", 4: "Four or five days"}
        _faf = input(vals_to_str(faf_vals))
        FAF = str(int(_faf) - 1)

        attrs = {
            'Gender': Gender,
            'Age': Age,
            'Weight': Weight,
            'Height': Height,
            'OFH': OFH,
            'FAVC': FAVC,
            'CAEC': CAEC,
            'FAF': FAF
        }
        path = []
        prediction = dealer.predict(attrs, path)
        print(f"\nYour predicted obesity level is {prediction}")

        ans = input("If want to see your path through the tree, press 1. Else, press 2.\n")
        if int(ans) == 2:
            break
        else:
            print_path(path)
    print("Bye!")


def predict_test_db():
    print("\nCalculating test db error..")
    with open("test_db.csv") as db:
        csv_reader = csv.reader(db)
        attrs = next(csv_reader)
        attrs.remove(attrs[-1])
        count = 0
        errors = 0
        for row in csv_reader:
            count += 1
            item = {}
            label = row[-1]
            for i in range(len(row) - 1):
                item[attrs[i]] = row[i]
            if dealer.predict(item) != label:
                errors += 1
    print(f"The test db error is {errors/count}\n")


def main():
    for i in range(4):
        PLAYERS.append(Player(i, 4))
    print("Decision Tree in construction...")
    build_tree()
    print("Tree constructed!")

    predict_test_db()
    run_gui()


if __name__ == "__main__":
    main()
