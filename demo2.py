#!/usr/bin/python3
import requests
import argparse
import sys
import json

# Constants
hybrid_url = "https://www.hybrid-analysis.com/api/v2/"

def upload_file(args):
    dbg_flag = args.dbg_flag
    hybrid_api = args.hybrid_api
    hybrid_ua = args.hybrid_ua

    hybrid_file = args.hybrid_file
    hybrid_env = args.hybrid_env

    pmsg="Submitting File to Hybrid-Analysis"
    print(pmsg + "\n" + "="*len(pmsg)) if dbg_flag else 0
    
    try:
        loc_file = {'file': open(hybrid_file,"rb").read()}
    except OSError:
        print("Sorry, could not open local file: " + hybrid_file)
        sys.exit()

    request_headers = {'user-agent': hybrid_ua,'api-key': hybrid_api}
    request_data = {'environment_id':hybrid_env}
    url = hybrid_url + "submit/file"

    # Verbose/Debug
    print(hybrid_api) if dbg_flag else 0
    print(request_headers) if dbg_flag else 0
    print(loc_file) if dbg_flag else 0
    print(url) if dbg_flag else 0

    response = requests.post(url, data=request_data, files=loc_file, headers=request_headers)
    pjson = json.loads(response.text)
    print(json.dumps(pjson, indent=4, sort_keys=True))
    sys.exit()

def get_job(args):
    dbg_flag = args.dbg_flag
    hybrid_api = args.hybrid_api
    hybrid_ua = args.hybrid_ua

    hybrid_job_id = args.hybrid_job_id

    pmsg="Retrieving Job State from Hybrid-Analysis"
    print(pmsg + "\n" + "="*len(pmsg)) if dbg_flag else 0

    request_headers = {'user-agent': hybrid_ua,'api-key': hybrid_api}
    url = hybrid_url + "report/" + hybrid_job_id + "/state"

    print(url) if dbg_flag else 0

    response = requests.get(url, headers=request_headers)
    pjson = json.loads(response.text)
    print(json.dumps(pjson, indent=4, sort_keys=True))

    if pjson["state"] == "ERROR":
        print("---> Hybrid-Analysis state is ERROR")

    if pjson["state"] == "SUCCESS":
        print("---> Hybrid-Analysis state is SUCCESS")

        pmsg="Retrieving Job Report from Hybrid-Analysis"
        print(pmsg + "\n" + "="*len(pmsg)) if dbg_flag else 0

        ###########################################
        # Full report requires default API privs
        ###########################################
        #url = hybrid_url + "report/" + hybrid_job_id + "/report/json"
        ###########################################

        url = hybrid_url + "report/" + hybrid_job_id + "/summary"
        print(url) if dbg_flag else 0
        response = requests.get(url, headers=request_headers)
        pjson = json.loads(response.text)
        print(json.dumps(pjson, indent=4, sort_keys=True))

    sys.exit()

def empty_func(args):
    parser.parse_args(['--help'])
    sys.exit()


# Setup arguments
parser = argparse.ArgumentParser(description='Hybrid-Analysis (hybrid-analysis.com)  demo for Siemplify =)')
parser.set_defaults(func=empty_func)
subparsers = parser.add_subparsers(help="sub-command help")

parser_a = subparsers.add_parser('upload', help="Upload file for analysis")
parser_a.add_argument('-k', dest='hybrid_api', help='Hybrid-Analysis API Key', required=True)
parser_a.add_argument('-f', dest='hybrid_file', help='File to be uploaded for analysis', required=True)
parser_a.add_argument('-e', dest='hybrid_env', help='Environment ID. Available environments ID: 300: "Linux (Ubuntu 16.04, 64 bit)", 200: "Android Static Analysis", 120: "Windows 7 64 bit", 110: "Windows 7 32 bit (HWP Support)", 100: "Windows 7 32 bit"', choices=[300,200,120,110,100], type=int, required=True)
parser_a.add_argument('-u', dest='hybrid_ua', help='In order to bypass the internal User-Agent blacklist checks, a browser typical User-Agent string or e.g. "Falcon Sandbox" has to be provided', required=False)
parser_a.add_argument('-v', dest='dbg_flag', help='Verbose output', action='store_true')
parser_a.set_defaults(func=upload_file,hybrid_ua="Falcon Sandbox")

parser_b = subparsers.add_parser('download', help="Download job-id")
parser_b.add_argument('-k', dest='hybrid_api', help='Hybrid-Analysis API Key', required=True)
parser_b.add_argument('-j', dest='hybrid_job_id', help='Job ID to request analysis results', required=True)
parser_b.add_argument('-u', dest='hybrid_ua', help='In order to bypass the internal User-Agent blacklist checks, a browser typical User-Agent string or e.g. "Falcon Sandbox" has to be provided', required=False)
parser_b.add_argument('-v', dest='dbg_flag', help='Verbose output', action='store_true')
parser_b.set_defaults(func=get_job,hybrid_ua="Falcon Sandbox")

parser.set_defaults(dbg_flag=False)

# Parse Arguments - Call Function
args = parser.parse_args()
dbg_flag = args.dbg_flag
print(args) if dbg_flag else 0
args.func(args)
sys.exit()

