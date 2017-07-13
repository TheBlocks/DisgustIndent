import sys
import getopt

CHARS_AT_END = [";", "{", "}"]
HELP_SCREEN = """DisgustIndent v1.0.0
DisgustIndent is a Python script used to totally disgustify any script you have.

Usage:
    DisgustIndent.py input.txt output.txt [-h] [-s] [-t]

Where:
input.txt        The name of the file you want to disgustify
output.txt       The name of the file the output should be saved to
-h --help        Shows this help screen
-s --spaces      The number of spaces to add to the
-t --tablength   How many spaces 1 tab should be counted as"""

# Read file and place each line in contents list as a separate element
try:
    file = sys.argv[1]
    output_file = sys.argv[2]
except IndexError:
    # Print help screen if 2 file names weren't passed in
    print(HELP_SCREEN)
    quit()

with open(file, "r") as f:
    contents = f.read().split("\n")

# Get optional arguments
args, _ = getopt.getopt(sys.argv[2:], "hs:t:", ["help", "spaces", "tablength"])

# Print help if it was in the arguments
if len(args) > 0 and "-h" in args[0]:
    print(HELP_SCREEN)
    quit()

# Get the number of spaces between the semicolons and the end of the longest line
# Default is 4 spaces
# Also get how many spaces 1 tab is (for languages that use tabs instead of spaces)
# Default is 4 spaces for 1 tab
spaces = 4
tab_length = 4
if "-s" in (i[0] for i in args) or "-t" in (i[0] for i in args):
    for arg in args:
        # Get number of spaces between semicolons and end of the longest line
        if "-s" in arg or "--spaces" in arg:
            try:
                int(arg[1]) == float(arg[1])
            except ValueError:
                print("You must enter a valid integer for -s (--spaces)")
            else:
                spaces = int(arg[1])
        # Get tab length
        if "-t" in arg or "--tab-length" in arg:
            try:
                int(arg[1]) == float(arg[1])
            except ValueError:
                print("You must enter a valid integer for -t (--tablength)")
            else:
                tab_length = int(arg[1])

# Separate lines so that the last character is from CHARS_AT_END if possible
separated_text = contents
for index, line in enumerate(separated_text):
    # If the line contains any character from CHARS_AT_END
    if True in [x in line for x in CHARS_AT_END]:
        # Get the index of the first character from CHARS_AT_END that appears in the line
        char_index = min([line.find(x) if line.find(x) != -1 else float("inf") for x in CHARS_AT_END])
        if len(line)-1 > char_index:
            try:
                separated_text[index + 1]
            except IndexError:
                separated_text.append("")
            finally:
                separated_text[index + 1] = separated_text[index][char_index + 1:] + separated_text[index + 1]
                separated_text[index] = separated_text[index][:char_index + 1]

# Get the length of the longest line
longest_length = 0
for line in separated_text:
    line = line.expandtabs(tab_length)
    if len(line) > longest_length:
        longest_length = len(line)

# Index for the character at the end
padded_index = longest_length + spaces

# Add spaces in between the ; or { or } and the character before
spaced_text = separated_text
for index, line in enumerate(spaced_text):
    line = line.expandtabs(tab_length)
    # If the line ends with any character from CHARS_AT_END
    if True in [line.endswith(x) for x in CHARS_AT_END]:
        # Add spaces before the character at the end (align it)
        spaces_to_add = padded_index - len(line) - 1
        spaced_text[index] = spaced_text[index][:-1] + " " * spaces_to_add + spaced_text[index][-1:]

# Save this in the specified file
with open(output_file, "w") as f:
    f.write("\n".join(spaced_text))
