from functions.get_file_content import get_file_content

response1 = get_file_content("calculator", "main.py")
response2 = get_file_content("calculator", "pkg/calculator.py")
response3 = get_file_content("calculator", "/bin/cat")
response4 = get_file_content("calculator", "pkg/does_not_exist.py")

print(response1)
print(response2)
print(response3)
print(response4)
