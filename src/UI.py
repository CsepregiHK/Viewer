def uifunc(searchclass):
    x = '1914'
    searchclass.load_data()
    while x != 'x':
        x = input("Kérdezz: ")
        if x == 'x':
            break
        else:
            for result in searchclass.run_search(x):
                date = result[0]
                title = result[1]
                text = result[2]
                spos = result[3]
                epos = result[4]
                print(date)
                print(title)
                if(spos > 0):
                    text_1 = text[:spos]
                    text_2 = text[spos:epos]
                    text_3 = text[epos:]
                    print(text_1, '!!!', text_2, '!!!', text_3)
                else:
                    print(text)
            print('------')