import pandas as pd

# globals
CHOICES = {
    'X': {  # need to lose
        'A': 3,  # scissors
        'B': 1,  # rock
        'C': 2,  # paper
    },
    'Y': {  # need to draw
        'A': 1,  # rock
        'B': 2,  # paper
        'C': 3,  # scissors
    },
    'Z': {  # need to win
        'A': 2,  # paper
        'B': 3,  # scissors
        'C': 1,  # rock
    },
}
RESULTS = {
    'X': 0,
    'Y': 3,
    'Z': 6,
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
df['score_for_choice'] = df.apply(lambda row: CHOICES[row.my_choice][row.opp_choice], axis=1)
df['score_for_result'] = df.apply(lambda row: RESULTS[row.my_choice], axis=1)
df['total_score'] = df.apply(lambda row: row.score_for_choice + row.score_for_result, axis=1)

print(df['total_score'].sum())
