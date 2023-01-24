### code to make a new blog entry using the minimal theme for github pages
from glob import glob as g

def get_posts(blog_dir):
    return []

## print the current blogs

# Get a list of dirs
dirs = g("../../../*/")

counter = 0
for dir in dirs:
    counter = counter + 1
    print(f"{counter}. {dir}")

blog_to_edit = int(input("Which blog would you like to add a page to?"))

if blog_to_edit in range(0,counter):
    blog_dir = dirs[blog_to_edit]
    blog_name = blog_dir.replace("../", "")[:-1]
    print(f"Editing blog {blog_name}...")
    blog_posts = get_posts(blog_dir)
else:
    print("Blog doesn't exist!")
