import random

chars = []
options = "123!@#%$%^&89*/"
passwordLenLimitor = 0
for option in options:
    chars.append(random.choice(options))
    passwordLenLimitor += 1
    if passwordLenLimitor >= 8:
        break
    
suggestedPassword = "".join(chars)
print(suggestedPassword)
print(len(suggestedPassword))
