import openai

openai.api_key = ""
model_engine = "text-davinci-003"


def askgpt(prompt, temp=1.3):
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temp,
    )
    return completion.choices[0].text


def nextStep(choice):
    global story, options
    step = askgpt(f'Write 2 or 3 short sentences about what happens when the character chooses {choice} in the context of the story, {story}, and the backstory of the character, {backstory}.')
    print(step)
    story += step
    problem = askgpt(f'Write another 2 or 3 short sentences for the story, {story}, that leaves the main character with two options.')
    print(problem)
    story += problem
    options = askgpt(f'Write the two options at the end of the story, {step}, separated by a new line in the format: Option 1, Option 2.').strip()
    options = options.split('\n')
    while '' in options:
        options.remove('')
    while ' ' in options:
        options.remove(' ')
    # print(options)
    print(options[0], '\n', options[1])


character = askgpt('Give me a name for a main character in an RPG game.')
print('25%', end='')
backstory = askgpt(f'Write a 1-2 sentence backstory for the main character, {character}.')
print('\b\b\b50%', end='')
story = askgpt(f'Write a short story in 3-4 sentences that leaves, {character}, with a problem that has two solutions. The story must make sense in the context of the backstory of the character; {backstory}.')
print('\b\b\b75%', end='')
options = askgpt(f'Write the two options in the story, {story}, separated by a new line in the format: Option 1, Option 2.').strip()
print('\b\b\b', character.strip(), '\n')
print(backstory.strip(), '\n\n', '-----', '\n')
print(story.strip(), '\n')
options = options.split('\n')
while '' in options:
    options.remove('')
while ' ' in options:
    options.remove(' ')
# print(options)
print(options[0], '\n', options[1])

while True:
    try:
        choice = int(input('Enter (1/2): '))
        if choice in [1, 2]:
            # story += options[choice-1]
            nextStep(options[choice-1])
    except ValueError:
        print('Enter a number stupid')
