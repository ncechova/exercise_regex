import re
from Bio import SeqIO
import gzip
import csv

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


# print(f"Lines logged on 2024-01-16: \n {lines_2024_01_16}")
# print(f"Lines that are ERROR or WARNING: \n {lines_error_warning}")
# print(f"IPv4 addresses found: \n {ipv4_addresses}")
# print(f"Lines ending in seconds: \n {lines_ending_in_seconds}")
# print(f"Lines with URLs: \n {lines_with_url}")


# (Optional) Check whether a single line, e.g. log_lines[0], matches the full expected format YYYY-MM-DD HH:MM:SS LEVEL message from start to end.
print(re.match(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s\w+\s.+", log_lines[0]))


# --- TASK 2 ---

# forward_MID + <sequence of interest> + reverse_complement(reverse_MID)

def reverse_complement(dna_sequence):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    reversed_sequence = dna_sequence[::-1]
    return ''.join(complement[base] for base in reversed_sequence)


class SequencingRead:
    def __init__(self, read_id, sequence):
        self.read_id = read_id
        self.sequence = sequence


    def matches_mid_pair(self, forward_mid, reverse_mid):
        # Create a regex pattern to match the forward MID at the start and the reverse complement of the reverse MID at the end
        reverse_comp = reverse_complement(reverse_mid)
        pattern = f"^{forward_mid}.*{reverse_comp}$"
        if re.match(pattern, self.sequence):
            return True
        return False

    def trim_mid_pair(self, forward_mid, reverse_mid):
        if self.matches_mid_pair(forward_mid, reverse_mid):
            reverse_comp = reverse_complement(reverse_mid)
            # Remove the forward MID and the reverse complement of the reverse MID from the sequence
            trimmed_sequence = re.sub(f"^{forward_mid}", "", self.sequence)
            trimmed_sequence = re.sub(f"{reverse_comp}$", "", trimmed_sequence)
            return trimmed_sequence
        return None

    def describe(self):
        return f"{type(self).__name__} {self.read_id} ({len(self.sequence)} bp)"

r1 = SequencingRead("demo_1", "AGCTTCGA" + "N" * 20 + reverse_complement("TGCAGGTC"))
# print(r1.describe())
# print(r1.matches_mid_pair("AGCTTCGA", "TGCAGGTC"))  # True
# print(r1.matches_mid_pair("CGATCGAT", "GCTAGCTA"))  # False
# print(r1.trim_mid_pair("AGCTTCGA", "TGCAGGTC"))     # 20 x "N"


# --- TASK 3 ---
class Demultiplexer:
    def __init__(self, fasta_path, mid_table_path):
        self.fasta_path = fasta_path
        self.mid_table_path = mid_table_path
        self.reads = []

        with gzip.open(self.fasta_path, "rt") as file:
            for record in SeqIO.parse(file, "fasta"):
                read = SequencingRead(record.id, str(record.seq))
                self.reads.append(read)
                # print(read.describe())

        with open(self.mid_table_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                forward_mid = row['forward_MID']
                reverse_mid = row['reverse_MID']



if __name__ == "__main__":
    fasta_file = "fishes.fna.gz"
    mid_table_file = "fishes_MIDs.csv"
    demultiplexer = Demultiplexer(fasta_file, mid_table_file)
    print(demultiplexer)

