import re

# --- TASK 1 ---git 
log_lines = [
    "2024-01-15 10:02:11 INFO Server started on port 8080",
    "2024-01-15 10:03:47 ERROR Failed to connect to database",
    "2024-01-16 08:15:00 WARNING Disk usage at 85%",
    "2024-01-16 14:22:39 ERROR Timeout while fetching https://example.com/api",
    "2024-01-17 09:00:05 INFO User admin logged in from 192.168.1.10",
    "2024-01-17 11:41:18 DEBUG Cache cleared successfully",
    "2024-01-18 03:12:56 ERROR Connection refused from 192.168.1.55",
    "2024-01-18 23:59:02 INFO Backup completed in 42s",
]

lines_2024_01_16 = []
lines_error_warning = []
ipv4_addresses = []
lines_ending_in_seconds = []
lines_with_url = []

for line in log_lines:
    # Find all lines logged on 2024-01-16.
    if re.match(r"2024-01-16", line):
        # print(re.match(r"2024-01-16", line))
        lines_2024_01_16.append(line)
    
    # Find all lines that are an ERROR or a WARNING.
    if re.search(r"ERROR|WARNING", line):
        # print(re.search(r"ERROR|WARNING", line))
        lines_error_warning.append(line)

    # Find all IPv4 addresses (four groups of 1-3 digits separated by dots) that appear anywhere in the log — only 2 of the 8 lines contain one.
    ipv4_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
    if ipv4_match:
        # print(ipv4_match)
        ipv4_addresses.append(ipv4_match.group())

    # Find all lines ending in a number of seconds, e.g. ...in 42s.
    if re.search(r"in \d+s", line):
        lines_ending_in_seconds.append(line)

    # Find all lines that mention a URL (starts with http:// or https://).
    if re.search(r"https?://", line):
        lines_with_url.append(line)


print(f"Lines logged on 2024-01-16: \n {lines_2024_01_16}")
print(f"Lines that are ERROR or WARNING: \n {lines_error_warning}")
print(f"IPv4 addresses found: \n {ipv4_addresses}")
print(f"Lines ending in seconds: \n {lines_ending_in_seconds}")
print(f"Lines with URLs: \n {lines_with_url}")


# (Optional) Check whether a single line, e.g. log_lines[0], matches the full expected format YYYY-MM-DD HH:MM:SS LEVEL message from start to end.
print(re.match(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s\w+\s.+", log_lines[0]))


# --- TASK 2 ---

# forward_MID + <sequence of interest> + reverse_complement(reverse_MID)

# class SequencingRead:
#     def 
