try:
    # Open files
    file1 = open("D:/Speechtech/Hindi/syllable_subset/count_subset_phonemes.txt", "r")
    file2 = open("D:/Speechtech/Hindi/syllable_subset/count.txt", "w+")
    file3 = open("D:/Speechtech/Hindi/syllable_subset/phonemes.txt", "w+")
    
    # Read content
    content = file1.readlines()
    print(content)
    
    # Process each line
    for line in content:
        x = line.strip().split()  # Strip and split
        if len(x) >= 2:  # Ensure enough elements exist
            file3.write(x[-1] + "\n")  # Write last element to file3
            file2.write(x[-2] + "\n")  # Write second-to-last to file2
        else:
            print(f"Skipping line due to insufficient data: {line}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close files
    file1.close()
    file2.close()
    file3.close()
