import csv

# File paths (update these with your actual file paths)
hindi_file = "D:\Speechtech\Hindi\cleaned_hindi_words.txt"
english_file = "D:\Speechtech\Hindi\words_translated.txt"
subset_file = "D:\Speechtech\Hindi\Real words.txt"
output_file = "D:\Speechtech\Hindi\hindi_subset.txt"

# Read words from the first file
with open(file1, "r", encoding="utf-8") as f:
    words1 = set(line.strip() for line in f if line.strip())

# Read words from the second file
with open(file2, "r", encoding="utf-8") as f:
    words2 = set(line.strip() for line in f if line.strip())

# Find words that are in file1 but not in file2
diff_words = words1 - words2

# Print the differences from file1
print("Words in file1 but not in file2:")
for word in diff_words:
    print(word)
