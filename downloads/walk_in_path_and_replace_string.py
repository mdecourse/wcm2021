import os
findText = """content to remove"""
for dname, dirs, files in os.walk("path_name"):
    for fname in files:
        if fname[-5:] == ".html":
            print(fname)
            fpath = os.path.join(dname, fname)
            with open(fpath, encoding="utf-8") as f:
                s = f.read()
            s = s.replace(findText, "")
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(s)