import requests as req
import json

class Salesfoceconnect:

    def __init__(self, login_url, payload):
        self.login_url = login_url
        #self.input_url = input_url
        self.payload = payload
        self.session = req.Session()

    def conn_and_get_token(self):
        #session = req.Session()
        res = self.session.post(self.login_url, data=self.payload)
        op_json = res.json()
        token = op_json['access_token']
        return token

    def get_json(self, token ,url_to_get):
        #session = req.Session()
        headers = {'content-type': 'application/json'}
        token = 'Bearer ' + token
        print(token)
        headers['Authorization'] = token
        acc_res = self.session.get(url_to_get, headers=headers)
        #acc_res = acc_res.json()
        return acc_res.json()

        

payload = {'client_id': 'Your Client ID',
               'client_secret': 'Your Client Secret',
               'username': 'Salesforce user name',
               'password': 'Salesforce user Password',
               'grant_type': 'Any  grant typr '
               }
url1 = 'URL to GET token'
url2="Retrioving Json out put "

salesforceobject = Salesfoceconnect(url1, payload)
token = salesforceobject.conn_and_get_token()



with open('input_from_salesforce.txt', 'w') as fp:   
    file_input = ["input_from_salesforce.txt"]
    input_from_salesforce = salesforceobject.get_json(token,url2)
    print(input_from_salesforce["nextRecordsUrl"])
    input_from_salesforce = json.dumps(input_from_salesforce, default='jsonDefault')
    
    fp.write(input_from_salesforce)
    input_from_salesforce = json.loads(input_from_salesforce)#, default='jsonDefault')
    print (input_from_salesforce['totalSize'])
    i=0
    while "nextRecordsUrl" in input_from_salesforce:
        print ("hello")
        with open("input_from_salesforce_" + str(i) + ".txt" , 'w') as fp:
            file_input.append("input_from_salesforce_" + str(i) + ".txt")
            url2 = input_from_salesforce["nextRecordsUrl"]
            print (input_from_salesforce["nextRecordsUrl"])
            url2=  'base url' + url2        
            input_from_salesforce = salesforceobject.get_json(token,url2)
            input_from_salesforce = json.dumps(input_from_salesforce, default='jsonDefault')
            fp.write(input_from_salesforce)
            input_from_salesforce = json.loads(input_from_salesforce)
            i = i+1



with open("input_from_salesforce_int.json", 'w') as f:  # fp.write(input_from_salesforce)
    for el in file_input:
        f1 = open(el, 'r')
        data = json.load(f1)
        f.write(json.dumps(data["records"], indent=1))


with open("input_from_salesforce_int.json" , 'r') as f_inr , open("advisor_input_from_salesforce.json", 'w') as f_fin :
    for line in f_inr:
        if "][" in line:
            f_fin.write(",")
        else:
            f_fin.write(line)


inputFile = open("input_from_salesforce.json")
data = json.load(inputFile)
inputFile.close()

count=len(data)
print ('count is:',count)

def collect_list(record):
    for element in record.values():
        if type(element) is dict:
            collect_list(element)
        else:
            list_1.append(element)
    return  list_1


with open('Json_to_csv_output.csv', 'w') as f_out_file:
    for record in data:
        list_1 = []
        var = collect_list(record)
        for index, item in enumerate(var):
            var[index] = str(item)
        f_out_file.write('|'.join(var) + '\n')


