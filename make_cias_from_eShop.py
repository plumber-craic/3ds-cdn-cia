import argparse
import os
import re
import subprocess
from support import maketicket_from_enctitlekeys_v3 as make_ticket
import sys
import xml.etree.ElementTree as ET

def name_from_id(id, dir):    
    xmlfile = r'support\3dsTitles.xml'
    xmltree = ET.parse(xmlfile)     
    for release in xmltree.getroot():        
        if release.find('titleid').text==id:
            name = release.find('name').text                
            return name
    # fallback to using the part of the dirname that came before id
    name = dir.split(id)[0]    
    if len(name) >= 3:
        name = name[:-2]        
        return name 
    # if still nothing, give up
    return "TitleID Not Found"

    
    
def region_from_path(root):
    tokens = root.split('\\')
    if 'EUR' in tokens:
        return 'EUR'
    elif 'USA' in tokens: 
        return 'USA'
    else:
        return 'ALL'


def type_from_path(fullpath):    
    tokens = fullpath.split('\\')
    if 'DLCS' in tokens:
        return ['DLC']
    elif 'ESHOP' in tokens: 
        return ['eShop']
    elif 'UPDATES' in tokens:
        ver = re.search('\((.*?)\)', fullpath)
        if ver:
            ver = ver.group(1)
            return ['Update', ver]
        else:
            return ['Update']
    else:
        return ['Other']
        
    
def main():
    # parse arguments    
    ver = '1.00'
    dt = 'March 7, 2019'
    parser = argparse.ArgumentParser(description='Batch eShop CIA Generator, by plumber_craic\nVersion {}, {}\nMakes CIAs from eShop titles downloaded with the WiiU USB loader.'.format(ver, dt)) 
    parser.add_argument( 'input',  help='Parent directory containing one or more games downloaded by WiiU USB loader. Game directories must contain the title id and should also contain the the name, e.g. \'Donkey Kong [0004000000041D00]\'') 
    parser.add_argument( 'output', type=str, help='Destination directory for the CIAs')
    if len(sys.argv) != 3:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    
    # find titles recursively in requested directory
    # directory name must contain a 16 digit title key and game dir must have title.tmd
    titles = []
    for root, dirs, _ in os.walk(args.input):
        for dir in dirs:
            files = os.listdir(os.path.join(root, dir))
            match = re.search('(0004[0-9a-zA-Z]{10}00)', dir)
            if (match and ('tmd' in files)) or (match and ('title.tmd' in files)):
                this_title = {}
                this_title['dir'] = os.path.join(os.path.abspath(root), dir)
                this_title['id'] = match.group(1).upper()
                this_title['name'] = name_from_id(this_title['id'], dir)
                this_title['result'] = ''
                this_title['region'] = region_from_path(root)
                this_title['type'] = type_from_path(os.path.join(os.path.abspath(root), dir))
                if len(this_title['type']) == 1:
                    this_title['type'] = this_title['type'][0]
                    this_title['update_version'] = ''                    
                else:
                    this_title['update_version'] = this_title['type'][1]
                    this_title['type'] = this_title['type'][0]
                titles.append(this_title)
    
    # make tickets
    for title in titles:
        if len(title['update_version']) > 0:
            cia_file = os.path.join(args.output, title['region'], title['type'], title['name'] + ' (' + title['update_version'] + ') [' + title['id'] + '].cia')
        else:
            cia_file = os.path.join(args.output, title['region'], title['type'], title['name'] + ' [' + title['id'] + '].cia')
        if not os.path.exists(os.path.join(args.output, title['region'], title['type'])):
            os.makedirs(os.path.join(args.output, title['region'], title['type']))
        cia_file_path = os.path.join(args.output, cia_file)
        # when make_cdn_cia.exe fails it can create 0 byte files. This check will force a retry
        if not os.path.exists(cia_file_path) or os.path.getsize(cia_file_path) == 0:
            print("Making ticket for \"{}\" [{}]".format(title['name'], title['id'])) 
            ticket_result = make_ticket.main(title['dir'], r'support\encTitleKeys.bin')
            # make CIA if ticket was created successfully        
            if ticket_result == 0:                
                print("Making CIA at {}".format(cia_file)) 
                cia_result = subprocess.call(r'support\make_cdn_cia64_1.2.exe "{}" "{}"'.format(title['dir'], cia_file))
                if cia_result == 0:
                    print("OK")
                    title['result'] = 0
                else:
                    print("Error")
                    title['result'] = 1
            else:
                print("Error")
                title['result'] = 1
    success_count = len([t for t in titles if t['result'] == 0])
    fail_count = len([t for t in titles if t['result'] == 1])
    ignore_count = len(titles) - (success_count + fail_count)
    print('=' * 40)
    print("Created CIAs for {}/{} titles. Ignored {} titles because they already have CIAs at the requested location.".format(success_count, fail_count+success_count, ignore_count))
    if fail_count > 0:
        print('=' * 40)
        print("Failed to create CIAs for the following folders:")
        for title in titles:
            if title['result'] == 1:
                print(title['dir'])
            
if __name__ == "__main__":
    main()