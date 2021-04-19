def optioon_but (message = """Форсаж 2  -http://example11.com | Кнопка 45 Ава - http://example2.com """): # Обработка 1
    arr = message.split("|")
    len_arr = len(arr)

    arr2 = []

    for i in range(0,len_arr):
        arr2 = (arr2 + arr[i].split("-"))

    dannie = arr2

    #print("Обработка1:",dannie)
    # Сортировка 1

    k = -1
    for i in arr2:
        k+=1
        if i[0] == ' ':
            if i[-1] == ' ':
                dannie[k] = (i[1:-1])
            else:
                dannie[k] = (i[1:])

        else:
            if i[-1] == ' ':
                dannie[k] = (i[:-1])
            else:
                pass

    #Сортировка 2
    #print("Обработка2:", dannie)

    k= -1
    for i in dannie:
        k+=1
        if i[0] == '\n':
            dannie[k] = i[1:]
    #Cортировка 3

    answer = []
    #print("Обработка3:", dannie)


    for i in range(0,len(dannie),2):

        answer.append({'name': dannie[i],"url": dannie[i+1]})

    return answer





def optioon_duble_button (message = """Форсаж 2 - Что бы посмотреть фильм сначала подпишись - Жми на имя что бы продолжить просмотр"""): # Обработка 2
    arr = message.split("-")
    k = -1
    dannie = arr
    for i in arr:
        k += 1
        if i[0] == ' ':
            if i[-1] == ' ':
                dannie[k] = (i[1:-1])
            else:
                dannie[k] = (i[1:])

        else:
            if i[-1] == ' ':
                dannie[k] = (i[:-1])
            else:
                pass
    return dannie