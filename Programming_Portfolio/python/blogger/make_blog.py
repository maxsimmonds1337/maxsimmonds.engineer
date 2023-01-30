### code to make a new blog entry using the minimal theme for github pages
from glob import glob as g
import os
from datetime import datetime

base_path = "../../../"

def get_posts(blog_dir):
    """Get's the blog posts from a given blog directory"""
    # get the markdown files from the given directory
    blogs =  g(blog_dir+"*.md")

    # strip the ../ and the trailing /
    blogs = [''.join(blog.replace("../", "").split("/")[-1:]) for blog in blogs]

    # TODO: make the blogs chronological

    return blogs

# this function adds the name of the blog (specified by the user) along with the posted date to the index 
# ---

# ## [Blog Post 0 - Day 0](blog0.md)
# Posted: 01/08/2022

# ---

# DIY One Wheel
# Start Date: 31/07/2022

# End Date: On going

# This is my current project, a self balancing electric skateboard, commonly known as a OneWheel.
def add_blog(base_dir, blog_name, blog_desc):
    # open index page
    with open(f"{base_dir}/index.md") as f:
        print(f)
    # write a new blog entry
    #   start date
    #   end date (on going)



def update_end_date(blog_dir, blog_name):
    pass

def add_post(blog_dir, blog_name, blog_number):
    cmd = "code " + blog_dir + "blog" + str(counter - 1) + ".md"
    os.system(cmd)
    with open(blog_dir + blog_name, "a") as f:
        posted_date = datetime.now().strftime("%d/%m/%y")
        f.write("---\n")
        f.write("## [Blog Post " + str(blog_number) + " - " + blog_name + "(" + blog_name + ")\n")
        f.write("Posted: " + str(posted_date))
        f.write(f"Last Edited: {posted_date}")
        f.write("\n---")

## print the current blogs

# Get a list of dirs
dirs = g(base_path+"*/")

counter = 0
for dir in dirs:
    counter = counter + 1
    print(f"{counter}. {dir}")

option = input("Which blog would you like to add a page to? (Press N for a new blog): ")

if int(option) in range(0,counter):
    blog_dir = dirs[int(option)]
    blog_name = blog_dir.replace("../", "")[:-1]
    print(f"Editing blog {blog_name}...")
    blog_posts = get_posts(blog_dir)
    print(f"Current Blogs:")
    counter = 0
    # if len == 0, then there's no homepage (or blogs)
    if len(blog_posts) == 0:
        option = input("There's no homepage for this blog!\nWould you like to make one now? (Hit enter to exit, or a name to continue)")
        if option == None:
            exit()
        # Make the homepage
        os.system("touch " + blog_dir + "/index.md")

        blog_title = input("Title of the blog? ")

        with open(blog_dir + "/index.md") as f:
            f.write("# " + blog_title)
    
    if len(blog_posts) == 1:
        print("No blog posts!")
    else:

        for blog in blog_posts:
            counter += 1
            print(f"{counter}. {blog}")

        blog_number = (counter - 1)
        option = input("Which blog to edit? Or, create a new blog with command N: ")

        if option == "N":
            add_post(blog_dir, blog_name, blog_number)
        else:
            # update the index to show the last edit on this blog (might be tricky)
            #open the blog
            print(f"Opening blog '{blog_dir + blog_posts[int(option)-1]}''")
            os.system("code " + blog_dir + str(blog_posts[int(option)-1]))

elif option == "N":
    pass
    # add_blog(base_dir, blog_name, blog_desc)        
else:
    print("Blog doesn't exist!")
