max = [0, 0, 0]

file1 = open('day01_input01.txt', 'r')
Lines = file1.readlines()

cur_elf_total = 0

for l in Lines:
    val = l.strip()
    if val == '':
        for i in (0, len(max)-1):
            if cur_elf_total > max[i]:
                max.insert(i, cur_elf_total)
                max = max[0:3] # truncate to 3 elements
                max.sort(reverse=True) # descending
                break # avoid dupes
        cur_elf_total = 0
    else:
        cur_elf_total += int(val)

# print(max)
print(sum(max))


