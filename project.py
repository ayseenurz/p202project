class Book:
  def __init__(self, title, author):
    self.title = title
    self.author = author
    
  def show_info(self):
    print(f"Title : {self.title}, Author: {self.author}")

class Ebook(Book):
  def __init__(self, title, author, type):
    super().__init__(title,author)
    self.type = type

  def show_information(self):
    print("\nThis book is written by", self.author, "and is of type", self.type,"with title", self.title,"\n")

b1 = Ebook("1984","George Orwell", "Pdf")
b1.show_information()

import platform

x = dir(platform)
print(x)