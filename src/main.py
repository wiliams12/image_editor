from functionality import Editor

editor = Editor()

editor.load("HGWRE5805.JPG")
editor.crop((30,30), (0,0))
pixel_set = []

# Red vertical line
for y in range(10, 21):
    pixel_set.append(((15, y), (255, 0, 0)))  # x=15, y=10..20

# Red horizontal line
for x in range(10, 21):
    pixel_set.append(((x, 15), (255, 0, 0)))  # y=15, x=10..20

# Green border box around the cross
for x in range(9, 22):
    pixel_set.append(((x, 9), (0, 255, 0)))   # top border
    pixel_set.append(((x, 21), (0, 255, 0)))  # bottom border
for y in range(9, 22):
    pixel_set.append(((9, y), (0, 255, 0)))   # left border
    pixel_set.append(((21, y), (0, 255, 0)))  # right border
editor.draw(pixel_set)
editor.show()