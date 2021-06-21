import dfc as d

def deleter(username,curdir_items,foldername):
    for item in curdir_items:
        if item['name'] == foldername:
            curdir_items = item['children']
            for item in curdir_items:
                if item['type']=="dir":
                    deleter(username,item["children"],item['name'])
                else:
                    host = item["host"]
                    d.deletefile(username,item['name'],host)