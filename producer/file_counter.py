with open("muon_run2022G_v11.txt") as f:
    lines = [line.strip() for line in f.readlines()]

split = 1

lines = [lines[split * n:split * n + split] for n in range(0, len(lines) // split + 1)]


for ip, pack in enumerate(lines):
    with open("input_files/input_files_%s.txt" % ip, "w+") as f:
        for line in pack:
            # f.write("%s\n" % line)
            f.write("root://xrootd-cms.infn.it://%s\n" % line)
