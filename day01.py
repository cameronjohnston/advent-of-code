max = 0

file1 = open('day01_input01.txt', 'r')
Lines = file1.readlines()

cur_elf_total = 0

for l in Lines:
    val = l.strip()
    if val == '':
        if cur_elf_total > max:
            max = cur_elf_total
        cur_elf_total = 0
    else:
        cur_elf_total += int(val)

print(max)


