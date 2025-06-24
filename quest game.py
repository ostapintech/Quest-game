import json
import hashlib
import os
import random
import sys

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = self.hash_password(password)
        self.completed_quests = []

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hash_password(password) == self.password

    def complete_quest(self, quest_title):
        if quest_title not in self.completed_quests:
            self.completed_quests.append(quest_title)

class Quest:
    def __init__(self, quest_title, description, choices):
        self.quest_title = quest_title
        self.description = description
        self.choices = choices

    def play(self):
        print(f"\n=== {self.quest_title} ===")
        print(self.description)
        print("Твої варіанти:")
        for option in self.choices:
            print(f"- {option}")

        try:
            choice = input("Твій вибір: ").strip().lower()
            if choice.isdigit() is True:
                raise ValueError
        except ValueError:
            print("Вводьте лише слова показані на екрані")
        else:
            if choice in self.choices:
                print(f"\nРезультат: {self.choices[choice]}")
            else:
                print("\nНевірний вибір.")

class Game():
    def __init__(self):
        self.users = []
        self.quests = []
        self.load_users()
        self.create_quests()

    def register_user(self):
        name = input("Введіть ваше імʼя: ")
        password = input("Введіть пароль: ")
        for user in self.users:
            if user.name == name:
                return "Користувач з таким імʼям вже існує"

        new_user = User(name, password)
        self.users.append(new_user)
        self.save_users()
        print(f"Користувача {name} - зареєестровано!")

    def save_users(self):
        data = []
        for user in self.users:
            data.append({
                "username": user.name,
                "password": user.password,
                "completed_quests": user.completed_quests
            })

        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_users(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                data = json.load(f)
                for user in data:
                    loaded_user = User(user["username"], "")
                    loaded_user.password = user["password"]
                    loaded_user.completed_quests = user["completed_quests"]
                    self.users.append(loaded_user)

    def login_user(self):
        name = input("Введіть ваше імʼя: ").strip()
        password = input("Введіть пароль: ").strip()

        for user in self.users:
            if user.name == name:
                if user.check_password(password):
                    print(f"Вітаю, {name}! Ви увійшли в систему.")
                    return user
                else:
                    print("Неправильний пароль.")
                    return None

        print("Користувача з таким імʼям не знайдено.")
        return None

    def start_quest(self, user):
        if not self.quests:
            print("Квести недоступні.")
            return

        quest = random.choice(self.quests)
        quest.play()
        user.complete_quest(quest.quest_title)
        self.save_users()

    def create_quests(self):
        q1 = Quest("Втеча з печери", "Ти прокинувся у печері...", {
            "ліворуч": "Ти врятувався!",
            "праворуч": "Тебе схопили."
        })
        q2 = Quest("Загублений скарб", "Ти стоїш перед старим храмом...", {
            "увійти": "Знайшов скарб!",
            "піти": "Втратив шанс назавжди."
        })
        self.quests = [q1, q2]

game = Game()

print("1. Зареєструватись\n"
      "2. Увійти\n"
      "0. Вийти")
try:
    choose = int(input(">> "))
    if choose < 0 or choose > 2:
        raise ValueError
except ValueError:
    print("Вводьте числа в 1 до 3")
else:
    match choose:
        case 1:
            current_user = game.register_user()
        case 2:
            current_user = game.login_user()
            print("Давай зіграємо у гру?\n"
                  "1. Так, давай\n"
                  "0. Ні")
            try:
                choose = int(input(">> "))
                if choose < 0 or choose > 1:
                    raise ValueError
            except ValueError:
                print("Вводьте лише числа 0 або 1")
            match choose:
                case 1:
                    game.start_quest(current_user)
                case 0:
                    sys.exit(0)
        case 0:
            sys.exit(0)