import openai
import os

openai.api_key = ""
model_engine = "text-davinci-003"
fileNum = 0


# Generate a response
def askgpt(prompt, temp=0.7):
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temp,
    )
    return completion.choices[0].text


def main():
    print('Loading', end='')
    storyLine = askgpt('could you create a branching chart for a story line of a short adventure game')
    print('\b\b\b\b\b\b\b33%', end='')
    badGameCode = askgpt(f'code a python game that follows this story line: {storyLine}. write the code so it is executable when opened. Include number options for inputs.')
    print('\b\b\b66%', end='')
    # print(badGameCode, '\n\n')
    gameCode = askgpt(f'could you make this python code more user-proof: {badGameCode}. Return only the code.')
    print('\b\b\b')
    playGame(gameCode, storyLine)


def playGame(gameCode, storyLine):
    global fileNum
    while True:
        try:
            f = open(f"gameScript{fileNum}.py", "x")
            f.write(gameCode)
            f.close()
            os.system(f'python gameScript{fileNum}.py')
            break
        except FileExistsError:
            fileNum += 1
        except (NameError, SyntaxError):
            print('Encountered an error; Debugging')
            gameCode = askgpt(f'make this code runnable: {gameCode}')
            fileNum += 1
        except Exception:
            print('Unusable game; Regenerating story')
            main()

    while True:
        while True:
            try:
                userInput = int(input('\n\nDo you want to 1: play again, 2: update the game/fix a bug, or 3: exit?: '))
                break
            except ValueError:
                print('Invalid input')
        if userInput in [1, 2, 3]:
            if userInput == 1:
                os.system(f'python gameScript{fileNum}.py')
            elif userInput == 2:
                bug = input('Briefly describe the problem: ')
                playGame(askgpt(f'This is a python game script: {gameCode}. Update this python game code to fix the following problem: {bug}. Make sure the code is user-proof and follows the story: {storyLine}. Return only the fully updated game script.'), storyLine)
            elif userInput == 3:
                exit()
        else:
            print('Invalid Input')


main()
