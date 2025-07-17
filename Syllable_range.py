from indic_unified_parser.uparser import wordparse

file1 = open("D:\Speechtech\Hindi\syllable_subset\total_syllables.txt", "r", encoding="utf8")
file2 = open("D:/Speechtech/Hindi/syllable_subset/subset_syllables.txt", "w", encoding="utf8")
lsflag = 0
wfflag = 0
clearflag = 0
content = file1.readlines()

def extract_syllables(parsed_output_string):

    start_idx = parsed_output_string.find("'(")  
    if start_idx == -1:
        return []
    end_idx = parsed_output_string.rfind("))")  # Find the end of the data
    data = parsed_output_string[start_idx + 2:end_idx + 1]
    
    syllables = []
    for group in data.split(") (( "):  # Split into groups like "p" "r" "a"
        group = group.replace("(", "").replace(")", "").replace('"', "").strip()
        if group:
            syllables.append("".join(group.split()))  # Combine letters into a syable
    
    return syllables

for i in range(len(content)):
    parsed_output_string = wordparse(content[i].strip(), lsflag, wfflag, clearflag)    
    syllables = extract_syllables(parsed_output_string)
    for j in range(len(syllables)):
        file2.write(syllables[j][:-1]+'\n')

file1.close()
file2.close()
