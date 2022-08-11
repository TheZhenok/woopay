from datetime import date
import random


def generate_cvv() -> str:
    i = random.randint(0, 9)
    j = random.randint(0, 9)
    k = random.randint(0, 9)
    cvv = str(i) + str(j) + str(k)
    return cvv


def generate_user_id(objs: list) -> str:
    while True:
        f = random.randint(0, 9)
        s = random.randint(0, 9)
        if (int(str(f) + str(s)) >= 50 and int(str(f) + str(s)) <= 99) or (int(str(f) + str(s)) <= 4):
            break

    id: str = str(f) + str(s)
    while len(id) < 12:
        id += str(random.randint(0, 9))
        
    for i in objs:
        if i.iin == id:
            generate_user_id(objs)

    return id


def generate_card_number(obj) -> str:
    objs: list = obj.get_all()
    num = "4"
    while len(num) < 16:
        num += str(random.randint(0, 9))
        
    for i in objs:
        if i.number == num:
            generate_card_number(objs)

    return num

