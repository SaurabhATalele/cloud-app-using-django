from datetime import date

class fs:
    def __init__(self,dirs):
        self.root_dir_items = dirs['children']
        self.dir_items = self.root_dir_items
        self.cur_dir_items = self.dir_items

        self.cur_dir = 'root'

    def data(self):
        a = { 'name':'root',
              'children':self.root_dir_items
              }
        return a
       
    
    def cd(self,dir_name):

        if dir_name == "root":
            self.cur_dir = "root"
            self.cur_dir_items = self.root_dir_items
        else:
            self.cur_dir = self.cur_dir+'/'+dir_name
            if self.cur_dir.__contains__('/'):
                c = self.cur_dir.split('/')
                for path in c:
                            
                    if path == "root":
                        self.cur_dir_items  = self.root_dir_items
                    else:
                        for item in self.dir_items:
                            if path == item['name'] and item["type"] == 'dir':
                                self.dir_items  = item['children']
                                self.cur_dir_items = self.dir_items
       

    def back(self):
        cd = self.cur_dir
        
        cd =  cd.split("/")
        
        cd.pop(-1)
        
        for path in cd:
                      
            if path == "root":
                self.cur_dir_items  = self.root_dir_items
                self.cur_dir = 'root'
            else:
                self.cur_dir = self.cur_dir+'/'+path
                for item in self.cur_dir_items:
                    if path == item['name'] and item["type"] == 'dir':
                        self.dir_items  = item['children']
                        self.cur_dir_items = self.dir_items
            
    

    def add_item(self,name,type,*argv):
        size = 0
        host = ''
        host2 = ''
        if argv:
            size = argv[0]
            host = argv[1]
            host2 = argv[2]
            
                
        da = date.today()
        a = str(da)

        if type == "dir":
            item = {
                "name":name,
                "type":type,
                "date_created":a,
                "children":[]
            }
        else:
            item = {
                "name":name,
                "type":type,
                'size':size,
                "date_created": a,
                'host':host,
                "host2":host2

            }
        self.cur_dir_items.append(item)
        print("item added Successfully")

    def remove_item(self,item_name):
        cdi  = self.cur_dir_items
        for i in cdi:
            if i['name']== item_name:
                cdi.remove(i)
        self.cur_dir_items = cdi

    def files(self):
        self.f =[]
        self.dat = {}
        d = self.cur_dir_items
        for file in d:
            if file['type'] != 'dir':
                self.dat['type'] = file['type']

                self.dat['name'] = file['name']
                self.dat['date_created'] = file['date_created']
                self.dat['size'] = file['size']

                self.f.append(self.dat)

                self.dat = {}
        return self.f
        
    def files(self,name):
        self.f =[]
        self.dat = {}
        d = self.cur_dir_items
        for file in d:
            if file['type'] != 'dir':
                self.dat['type'] = file['type']
                self.dat['name'] = file['name']
                if self.dat['name'].__contains__(name):
                    
                    self.dat['date_created'] = file['date_created']
                    self.dat['size'] = file['size']

                    self.f.append(self.dat)

                self.dat = {}
        return self.f


    def folders(self,name):
        self.f =[]
        self.dat = {}
        d = self.cur_dir_items
        for file in d:
            if file['type'] == 'dir':
                self.dat["name"] = file['name']
                if self.dat["name"].__contains__(name):
                    self.dat["date_created"] = file['date_created']   
                    self.f.append(self.dat)
                self.dat = {}
        return self.f  
            

    def storage_used(self):
        self.size = 0
        items = self.root_dir_items
        def rec(items):
            for item in items:
                for i in item:
                    if "size" in i:
                        self.size = self.size +item['size']
        rec(items)

        for item in items:
            for i in item:
                if "children" in i:
                    rec(item["children"])
                    

        return self.size