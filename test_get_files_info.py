from functions.get_files_info import get_files_info

response1 = get_files_info("calculator", ".")
response2 = get_files_info("calculator", "pkg")
response3 = get_files_info("calculator", "/bin")
response4 = get_files_info("calculator", "../")

print(response1)
print(response2)
print(response3)
print(response4)
