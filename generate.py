from MyQR import myqr
import os

f = open('students.txt', 'r')
lines = f.read().split("\n")
print(lines)

for i in range(0, len(lines)):
    data = lines[i]
    version, level, qr = myqr.run(
        str(data),
        level='H',
        version=1,
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=str(lines[i]+'.png'),
        save_dir=os.getcwd()
    )
