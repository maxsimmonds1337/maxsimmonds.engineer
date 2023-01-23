### code to make a new blog entry using the minimal theme for github pages

from glob import glob as g

print(g("./Pages/blog*.md"))