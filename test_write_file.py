from functions.write_file import write_file

response1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(response1)
response2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(response2)
response3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(response3)
