from MOTVOY_III import MOTVOY_III
import sys

text = ' '.join(sys.argv[1:])

motvoy = MOTVOY_III()
motvoy.say(text, wait=True)

input("Нажмите ENTER для завершения")

motvoy.close()