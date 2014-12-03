""" Write a program that prompts for a file name,
    and then reads through the file looking for lines of the form:
    X-DSPAM-Confidence: 0.865

    When you encounter a line that starts with "",
    pull apart the line to extract the floating point number on the line.
    Count these lines and compute the total of the spam confidence values from these lines.
    When you reach the end of the file, print out the average spam confidence.
"""
count = 0
spam_conf_header = "X-DSPAM-Confidence:"
fname = raw_input("Enter file name:")
fh = open(fname)
for line in fh:
    count += 1 # Hmm, this counts all lines, not just those with X-DSPAM-Confidence
    if not line.startswith(spam_conf_header):
        continue    # Give continue its own line. More readable.

    length = len(line)
    # Avoid "magic numbers" like 21
    line_offset_after_header = len(spam_conf_header)+1
    number = line[line_offset_after_header:]
    float_number = float(number)
    print line, count, float_number

print "Done"
