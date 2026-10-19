#Presorting Naif: Mencari Modus

arr = [1, 6, 10, 5, 6 , 5, 4]
def pencarian_modus(arr):
    count_mode = 0
    mode = None
    for i in range(len(arr)):
        count = 0
        nilai_sekarang = arr[i]
        for j in range(len(arr)):
            if nilai_sekarang == arr[j]:
                count += 1
        if count > count_mode:
            count_mode = count
            mode = nilai_sekarang
    print(mode, count_mode)

pencarian_modus(arr)
            
            