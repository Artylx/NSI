albi = [["Janvier",5.4,55.9,96.6],
["Février",6.4,53.1,118.6],
["Mars",9.3,51.5,177],
["Avril",11.8,82,183.6],
["Mai",15.9,79.9,219.3],
["Juin",19.6,64.4,244.9],
["Juillet",22.3,40.6,270.6],
["Août",22,55.9,255.7],
["Septembre",18.5,57.1,213.5],
["Octobre",14.6,65.4,154.1],
["Novembre",9,60,92.7],
["Décembre",5.9,65.1,86.8]]

paris=[ ['Janvier', 4.9, 51, 62.5],
        ['Février', 5.6, 41.2, 79.2],
        ['Mars', 8.8, 47.6, 128.9],
        ['Avril', 11.5, 51.8, 166],
        ['Mai', 15.2, 63.2, 193.8],
        ['Juin', 18.3, 49.6, 202.1],
        ['Juillet', 20.5, 62.3, 212.2],
        ['Juin', 18.3, 49.6, 202.1],
        ['Juillet', 20.5, 62.3, 212.2],
        ['Août', 20.3, 52.7, 212.1],
        ['Septembre', 16.9, 47.6, 167.9],
        ['Octobre', 13, 61.5, 117.8],
        ['Novembre', 8.3, 51.1, 67.7],
        ['Décembre', 5.5, 57.8, 51.4] ]

def show_datas(datas):
    for month in datas:
        print(f"{month[0]} : {month[1]} °C/ {month[2]} mm/ {month[3]} h")

def clean_datas(datas):
    L1 = []
    for month in datas:
        if not month in L1:
            L1.append(month)
        else:
            print("Doublon supprimé :", month)
    return L1

#show_datas(albi)

paris = clean_datas(paris)
show_datas(paris)