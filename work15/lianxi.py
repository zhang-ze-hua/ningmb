while True:
    try:
        s = input()
        print(s)
        list1 = list(s.split(" "))
        print(list1)
        list1.sort()
        print(" ".join(list1))
    except:
        break