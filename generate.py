import json, os, random

current_path = os.getcwd().replace('\\','/')

block_list = os.listdir(current_path + '/ref/minecraft/loot_table/blocks')
entity_list = os.listdir(current_path + '/ref/minecraft/loot_table/entities')
entity_list.remove('sheep')
sheep_list = os.listdir(current_path + '/ref/minecraft/loot_table/entities/sheep')
recipe_list = os.listdir(current_path + '/ref/minecraft/recipe')

item_reg_list = ['minecraft:elytra'] * 2 + ['minecraft:cod_bucket', 'minecraft:pufferfish_bucket', 'minecraft:salmon_bucket', 'minecraft:tadpole_bucket'] + ['minecraft:blast_furnace', 'minecraft:smoker'] + ['minecraft:furnace','minecraft:stonecutter'] * 3 + ['minecraft:ender_eye'] * 8 + ['minecraft:crafting_table'] * 10 + ['minecraft:arrow','minecraft:crossbow','minecraft:bow','minecraft:shears','minecraft:iron_shovel','minecraft:diamond_shovel','minecraft:iron_hoe','minecraft:diamond_hoe','minecraft:iron_axe','minecraft:diamond_axe','minecraft:iron_pickaxe','minecraft:diamond_pickaxe','minecraft:netherite_pickaxe','minecraft:golden_pickaxe']

def reg_entry_child(entry):
    global item_reg_list
    if entry['type'] == 'minecraft:item':
        item_reg_list.append(entry['name'])
    if entry['type'] == 'minecraft:alternatives':
        for child in entry['children']:
            reg_entry_child(child)
    return

def mod_entry_child(entry):
    global item_reg_list
    if entry['type'] == 'minecraft:item':
        entry['name'] = item_reg_list.pop()
    if entry['type'] == 'minecraft:alternatives':
        for child in entry['children']:
            mod_entry_child(child)
    return

def reg_item_loot(file):
    global item_reg_list
    with open(file,'r',encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        try:
            for pool in json_data['pools']:
                for entry in pool['entries']:
                    reg_entry_child(entry)
        except KeyError:
            return
    return

def reg_item_recipe(file):
    global item_reg_list
    with open(file,'r',encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        try:
            item_reg_list.append(json_data['result']['id'])
        except KeyError:
            return
    return

def mod_item_loot(rfile,wfile):
    global item_reg_list
    with open(rfile,'r',encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        item_name = item_reg_list[-1]
        try:
            for pool in json_data['pools']:
                for entry in pool['entries']:
                    mod_entry_child(entry)
        except KeyError:
            return
        with open(wfile,'w',encoding="utf-8") as write_file:
            json.dump(json_data, write_file, indent=4)
    return

def mod_item_recipe(rfile,wfile):
    global item_reg_list
    with open(rfile,'r',encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        try:
            json_data['result']['id'] = item_reg_list.pop()
            json_data['result']['count'] = 1
        except KeyError:
            return
        with open(wfile,'w',encoding="utf-8") as write_file:
            json.dump(json_data, write_file, indent=4)
    return

#register items

for file in block_list:
    open_dir = current_path + '/ref/minecraft/loot_table/blocks/' + file
    reg_item_loot(open_dir)

for file in entity_list:
    open_dir = current_path + '/ref/minecraft/loot_table/entities/' + file
    reg_item_loot(open_dir)

for file in sheep_list:
    open_dir = current_path + '/ref/minecraft/loot_table/entities/sheep/' + file
    reg_item_loot(open_dir)

for file in recipe_list:
    open_dir = current_path + '/ref/minecraft/recipe/' + file
    reg_item_recipe(open_dir)

random.shuffle(item_reg_list)
#print(item_reg_list)

#replace files

for file in block_list:
    read_dir = current_path + '/ref/minecraft/loot_table/blocks/' + file
    write_dir = current_path + '/data/minecraft/loot_table/blocks/' + file
    mod_item_loot(read_dir,write_dir)

for file in entity_list:
    read_dir = current_path + '/ref/minecraft/loot_table/entities/' + file
    write_dir = current_path + '/data/minecraft/loot_table/entities/' + file
    mod_item_loot(read_dir,write_dir)


for file in sheep_list:
    read_dir = current_path + '/ref/minecraft/loot_table/entities/sheep/' + file
    write_dir = current_path + '/data/minecraft/loot_table/entities/sheep/' + file
    mod_item_loot(read_dir,write_dir)

for file in recipe_list:
    read_dir  = current_path + '/ref/minecraft/recipe/' + file
    write_dir  = current_path + '/data/minecraft/recipe/' + file
    mod_item_recipe(read_dir,write_dir)
