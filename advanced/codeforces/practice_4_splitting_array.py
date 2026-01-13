'''
Леша и разбиение массива
'''

num_elements = int(input())
lesha_arr = list(map(int, input().split()))

if sum(lesha_arr) != 0:
    print("YES")
    print(1)
    print(f"1 {num_elements}")
else:
    for i in range(num_elements):
        if lesha_arr[i] != 0:
            print("YES")
            print(2)
            print(f"1 {i + 1}")
            print(f"{i + 2} {num_elements}")
            break
    else:
        print("NO")
