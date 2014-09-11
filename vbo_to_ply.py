from __future__ import division
import sys 
FILE=sys.argv[1]
OUTFILE=sys.argv[2]
stride=14
indices=[0,1,2,6,7,8]
zoom=16
maximum_range = 4096

open(OUTFILE, 'w').close()

def tile_to_meters(i):
	return 40075016.68557849 / pow(2, zoom)

conversion_factor = tile_to_meters(zoom) / maximum_range

def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

lines = file_len(FILE)
keep = []

loops = int(lines/stride)

for i in range(0,loops):
	offset= i*stride
	offset_indices = [j + offset for j in indices]
	# print offset_indices
	for k in offset_indices:
		keep.append(k)
# print keep
newline = ""
index = 0
vertex_count = 0
newfile = open(OUTFILE, "w")

with open(FILE, "r") as file:
	for i, line in enumerate(file):
		if i in keep:
			# print i, index, ":", line
			newline = newline + line.rstrip(",\n") + " "
			if index == len(indices)-1:
				tokens = newline.split(" ")
				tokens[0] = str(float(tokens[0]) * conversion_factor)
				tokens[1] = str(float(tokens[1]) * conversion_factor)
				tokens[3] = str(int(float(tokens[3]) * 255))
				tokens[4] = str(int(float(tokens[4]) * 255))
				tokens[5] = str(int(float(tokens[5]) * 255))
				newline = " ".join(tokens)
				newfile.write(newline + "\n")
				newline = ""
				index = 0
				vertex_count += 1
			else:
				index += 1
		if (i % 1000 == 0):
			print(str(round(i / offset_indices[len(offset_indices)-1] * 100, 2))+"%")
	face_count = int(vertex_count / 3)
	for i in range(face_count):
		j = i*3
		newline = "3 "+str(j)+" "+str(j+1)+" "+str(j+2)+"\n"
		newfile.write(newline)
newfile.close()


def line_prepend(filename,line):
    with open(filename,'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write(line.rstrip('\r\n') + '\n' + content)

header = '''ply
format ascii 1.0
element vertex '''+str(vertex_count)+'''
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
element face '''+str(face_count)+'''
property list uchar int vertex_indices
end_header
'''
line_prepend(OUTFILE, header)