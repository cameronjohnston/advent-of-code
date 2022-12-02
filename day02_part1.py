import pandas as pd

# globals
CHOICES = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}
RESULTS = {
    'X': {
        'A': 3,
        'B': 0,
        'C': 6,
    },
    'Y': {
        'A': 6,
        'B': 3,
        'C': 0,
    },
    'Z': {
        'A': 0,
        'B': 6,
        'C': 3,
    },
}

file1 = open('day02_input.txt', 'r')
Lines = file1.readlines()

df = pd.DataFrame(columns=['opp_choice', 'my_choice'])

for l in Lines:
    l = l.rstrip()
    opp_choice, my_choice = l.split(' ')
    res = {
        'opp_choice': [l.split(' ')[0]],
        'my_choice': [l.split(' ')[1]],
    }
    df = pd.concat([df, pd.DataFrame.from_dict(res)])

# populate scores (for choice and result)
df['score_for_choice'] = df.apply(lambda row: CHOICES[row.my_choice], axis=1)
df['score_for_result'] = df.apply(lambda row: RESULTS[row.my_choice][row.opp_choice], axis=1)
df['total_score'] = df.apply(lambda row: row.score_for_choice + row.score_for_result, axis=1)

print(df['total_score'].sum())
