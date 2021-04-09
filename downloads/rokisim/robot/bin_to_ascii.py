import struct
normals = []
points = []
triangles = []
triangle_number = 0
def load_binary_stl(fp):
    '''
    二位元 STL 檔案格式如下:
    檔案標頭共有 80 個字元(bytes), 內容通常省略, 但是內容不可使用 solid, 以免與文字檔案 STL 混淆
    UINT8[80] – Header
    UINT32 – Number of triangles (I:佔 4 bytes 的 unsigned integer)
  
    foreach triangle
    REAL32[3] – Normal vector (f:每一座標分量為一佔 4 bytes 的 float, 共佔 12 bytes)
    REAL32[3] – Vertex 1
    REAL32[3] – Vertex 2
    REAL32[3] – Vertex 3
    UINT16 – Attribute byte count (H:兩個 bytes 的 unsigned short, 表示 attribute byte count)
    end
  
    '''
    # 已經在外部開檔
    #fp=open(filename,'rb')
    header=fp.read(80)
    triangle_number = struct.unpack('I',fp.read(4))[0]
    #print(triangle_number)
    count=0
    while True:
        try:
            p=fp.read(12)
            if len(p)==12:
                n=[struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]]
                normals.append(n)
                l = len(points)
                #print(n)
            p=fp.read(12)
            if len(p)==12:
                p1=[struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]]
                points.append(p1)
                #print(p1)
            p=fp.read(12)
            if len(p)==12:
                p2=[struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]]
                points.append(p2)
            p=fp.read(12)
            if len(p)==12:
                p3=[struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]]
                points.append(p3)
                triangles.append((l, l+1, l+2))
            # 使用 count 來計算三角形平面個數
            # triangle_number 為 STL 檔案中的三角形個數
            count += 1
            #print(count)
            # 在前面 12*4 個 bytes 的 normal 與三個點資料後, 為
            # 一個 2 bytes 長的 unsigned short, 其值為零, 為 attribute
            fp.read(2)
            # 讀完所有三角平面後, 即跳出 while
            if count > triangle_number:
                break
        except EOFError:
            break
    #fp.close()
def read_length(f):
    length = struct.unpack("@i", f.read(4))
    return length[0]
def read_header(f):
    f.seek(f.tell()+80)
    
def eformat(f, prec, exp_digits):
    s = "%.*e"%(prec, f)
    mantissa, exp = s.split('e')
    # add 1 to digits as 1 is taken by sign +/-
    return "%se%+0*d"%(mantissa, exp_digits+1, int(exp))
    
def write_as_ascii(outfilename):
    f = open(outfilename, "w")
    f.write ("solid "+outfilename+"\n")
    # write color
    f.write("\tcolor 0.816 0.816 0.816\n")
    scale = 1.0
    for n  in range(len(triangles)):
        #"{:e}".format(float_number)
        f.write ("\tfacet normal {} {} {}\n".format(eformat(normals[n][0]*scale, 6, 2) ,eformat(normals[n][1]*scale, 6, 2),eformat(normals[n][2]*scale, 6, 2)))
        f.write ("\t\touter loop\n")
        f.write ("\t\t\tvertex {} {} {}\n".format(eformat(points[triangles[n][0]][0]*scale, 6, 2),eformat(points[triangles[n][0]][1]*scale, 6, 2),eformat(points[triangles[n][0]][2]*scale, 6, 2)))
        f.write ("\t\t\tvertex {} {} {}\n".format(eformat(points[triangles[n][1]][0]*scale, 6, 2),eformat(points[triangles[n][1]][1]*scale, 6, 2),eformat(points[triangles[n][1]][2]*scale, 6, 2)))
        f.write ("\t\t\tvertex {} {} {}\n".format(eformat(points[triangles[n][2]][0]*scale, 6, 2),eformat(points[triangles[n][2]][1]*scale, 6, 2),eformat(points[triangles[n][2]][2]*scale, 6, 2)))
        f.write ("\t\tendloop\n")
        f.write ("\tendfacet\n")
    f.write ("endsolid "+outfilename)
    f.close()
def main():
    infilename = "joint1.stl"
    outfilename = "joint1a.stl"
    try:
        f = open(infilename, "rb")
        #read_header(f)
        #l = read_length(f)
        try:
            load_binary_stl(f)
            l = len(normals)
        except Exception as e:
            print("Exception",e)
        print(len(normals), len(points), len(triangles), l)
        write_as_ascii(outfilename)
        print("done")
    except Exception as e:
        print(e)
if __name__ == '__main__':
    main()