#!/usr/bin/env python

# THE BEER-WARE LICENSE (Revision 42):
#
# momu (https://github.com/momu) wrote this file.  As long as you 
# retain this notice you can do whatever you want with this stuff. If
# we meet some day, and you think this stuff is worth it, you can buy
# me a beer in return.


import sys
import tablib
import locale
import ruamel.yaml
import argparse


locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
members = []

# mitgliedskonto_zahlungsgrund, mitglied_empfaenger,
# mitglied_anrede_du, mitgliedskonto_differenz, mitglied_id

class Member:
    
    def __init__(self, id, opening=None, address=None, email=None, vorname=None, name=None):
        self.account = tablib.Dataset(headers=['description', 'value'])
        self.account_sum = 0.0
        
        self.id = int(id)
        if opening is not None:
            self.opening = opening
        if address is not None:
            self.address = address
        if email is not None:
            self.email = email
        if vorname is not None:
            self.vorname = vorname
        if name is not None:
            self.name = name
        #self.value[0] = value
        
    
    def __eq__(self, other_member):
        return self.id == other_member.id
    
    def add_to_account(self, description, value):
        self.account.append([description, value])
        self.account_sum += float(locale.atof(value))
    
    def generate_filename(self):
        return self.name + '_' + self.vorname + '_' + str(self.id) + '.yaml'
    
    def get_yaml_data(self):
        member_data = {'to': self.address.replace('\n','  \n'), 
                       'sum': locale.format_string("%.2f", self.account_sum), 
                       'opening': self.opening,
                       'email': self.vorname + ' ' + self.name + ' <' + self.email + '>'}
        member_data['position']= []
        for i in range(self.account.height):     
            member_data['position'].append({'description': self.account['description'][i], 
                                          'value': self.account['value'][i]})
            
        return member_data
        
        
   

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv-file", default='example-export.csv', help="CSV File")
    parser.add_argument("-o", "--output-dir", default='data', help="Output Directory")
    args = parser.parse_args()
    process_csv(args.csv_file)
    write_member_yaml(args.output_dir)


def process_csv(csv_file):
    data = tablib.Dataset().load(open(csv_file).read())
    
    
    for i in range(data.height):
        data_row = tablib.Dataset(data[i], headers=data.headers)
        member = Member(data_row['mitglied_id'][0], 
                        data_row['mitglied_anrede_du'][0], 
                        data_row['mitglied_empfaenger'][0], 
                        data_row['mitglied_email'][0],
                        data_row['mitglied_vorname'][0],
                        data_row['mitglied_name'][0])
        
        if not member in members:
            members.append(member)
            print('append member: ' + data_row['mitglied_name'][0])
        members[members.index(member)].add_to_account(data_row['mitgliedskonto_zahlungsgrund'][0],
                    data_row['mitgliedskonto_differenz'][0])
        print('add to account ' + data_row['mitglied_name'][0] + ' - ' + 
              data_row['mitgliedskonto_zahlungsgrund'][0] + ':' +
                    data_row['mitgliedskonto_differenz'][0])
    

def write_member_yaml(output_dir):
    
    for member in members:
        with open(output_dir + '/' + member.generate_filename(), 'w') as file:
            ruamel.yaml.round_trip_dump(member.get_yaml_data(), file, default_style= '|', indent=0, block_seq_indent=0, explicit_start=True, explicit_end=True,default_flow_style=False)
            # print(ruamel.yaml.dump(yaml_data))
            
        
sys.exit(main())
