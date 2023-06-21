"""
This is a launcher for Toontown Rewritten that will download the latest files from the content mirror and launch the game.
"""

import requests
import getpass
import subprocess
import sys
import time
import os 
import hashlib
import bz2
def login(username, password, queue_token=None, toonguard_code=None, auth_token=None):
    # Login to Toontown Rewritten
    login_url = "https://www.toontownrewritten.com/api/login?format=json"
    # get the sessionToken from the login response
    if auth_token and toonguard_code:
        data = {"username": username, "password": password,"appToken": toonguard_code, 'authToken': auth_token}
    elif queue_token:
        data = {"username": username, "password": password, "queueToken": queue_token}
    else:
        data = {"username": username, "password": password}

    response = requests.post(login_url, data=data)

    # Check if login was successful
    if response.status_code == 200:
        return response.json()
    else:
        print("Login failed.")
        sys.exit(1)

def download_file(url, filename, patch_manifest, headers):
   
    if os.path.isfile(filename):
        # check if the hash matches
        # if it does, skip it
        if get_file_hash(filename) == patch_manifest[filename]["hash"]:
            print(f"Skipping {filename} because it already exists.")
            return
        else:
            # update the file
            print(f"Updating {filename}...")
           # the file is the [filename] a hash , and bz2 
            file = requests.get(url + patch_manifest[filename]["dl"], headers=headers)
            with open (filename + ".bz2", 'wb') as zipped_file:
                # write the compressed file
                zipped_file.write(file.content)
            with open (filename, 'wb') as new_file, open(filename + ".bz2", 'rb') as zipped_file:
                # decompress the file
                new_file.write(bz2.decompress(zipped_file.read()))
            # delete the compressed file
            os.remove(filename + ".bz2")
    else:
        # if it doesn't exist, download it
        print(f"Downloading {filename}...")
        file = requests.get(url + patch_manifest[filename]["dl"], headers=headers)
        with open (filename + ".bz2", 'wb') as zipped_file:
            # write the compressed file
            zipped_file.write(file.content)
        with open (filename, 'wb') as new_file, open(filename + ".bz2", 'rb') as zipped_file:
            # decompress the file
            new_file.write(bz2.decompress(zipped_file.read()))
        # delete the compressed file
        os.remove(filename + ".bz2")
        


        
        
def get_file_hash(filename):
    # get the hash of a file
    return hashlib.sha1(open(filename, 'rb').read()).hexdigest()



def download_content_mirror_files(content_mirror_url, patch_manifest_url, headers):
    
    # url also includes the filename
    # url = "https://download.toontownrewritten.com/patches/phase_3.mf.a847b3e3a6.bz2"
    """Download files from the content mirror using patch manifest.
    here is the patch manifest format:
    {"winter_snow.mf": {"dl": "winter_snow.mf.c9f3256fcc.bz2",
      "hash": "c9f3256fccb29542d2cf24d2bc62386ec19e5536",
        "compHash": "691aec5873c1f634e1c255a2fd37f4cd96ee0201", 
        "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, 
        "phase_12.mf": {"dl": "phase_12.mf.2a1c5aa418.bz2", 
        "hash": "2a1c5aa418036d0438320f330a25e8beb90a893d",
          "compHash": "46c7a33a2cd6e7cbb969bf62ededd1c5f98cd517",
            "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, 
            "phase_13.mf": {"dl": "phase_13.mf.154823fc24.bz2", 
            "hash": "154823fc24c28075b6ac49553dfe067f2d90b31d", 
            "compHash": "1d54fb0b18f0d4d30e50071e2ddfb2967105bb58", 
            "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]},
              "phase_3.5.mf": {"dl": "phase_3.5.mf.0e78ac9923.bz2", 
              "hash": "0e78ac99232f859aadec507027a0d9745d109388",
                "compHash": "759d161da812c43a7958eeaecb8118c37213a83b",
                  "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]},
                    "phase_10.mf": {"dl": "phase_10.mf.ef0b0735c2.bz2", 
                    "hash": "ef0b0735c27ce0672648a48d3d8d9a233225c0b8",
                      "compHash": "0594bc0d163e5202307c19b620a592236b118abc", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "winter_music.mf": {"dl": "winter_music.mf.4f98338576.bz2", "hash": "4f98338576ddb26995a2099bf135a3d0cae3d323", "compHash": "f3177cf311fcf63ac70f5214628910c9fd6fcd46", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "Toontown Rewritten": {"dl": "Toontown%20Rewritten.fb2a62d844.bz2", "hash": "fb2a62d84417fb228c914d64ef78fbab0ab8ed3d", "compHash": "b6d4f18faf49369bf4223ccf181ef3d69ebb2836", "patches": {}, "only": ["darwin"]}, "phase_9.mf": {"dl": "phase_9.mf.853ab10ee3.bz2", "hash": "853ab10ee325e7066fb3883b730de07e4a1a0087", "compHash": "d599032ae2a86ff7c1a9a7c7a57efeb44b547e18", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "TTRGame.vlt": {"dl": "TTRGame.vlt.228df23cb8.bz2", "hash": "228df23cb81a64f8c3d0c6ccb2ffca7d9079da95", "compHash": "8cdb2592deb24450a30b276ec3f5be7e7345b0cf", "patches": {"764a3c3e1fc1534caaa8ba016145c3e7668a7544": {"filename": "TTRGame.vlt.228df23cb8_from_764a3.bsdiff.bz2", "patchHash": "1bf53341c5f8e558df7d4d0a0a15b1fcc32323fe", "compPatchHash": "a3bb382a8bbbcd213dfa877e148964eda6f50537"}, "3fb5a649f061b40c7d6d0ffbaca21b88295fabab": {"filename": "TTRGame.vlt.228df23cb8_from_3fb5a.bsdiff.bz2", "patchHash": "2c2f106c8d40204f5886135c2fee995d1f681289", "compPatchHash": "34403dc3a943b3a7c677bec71ea114790110dc3d"}, "2abe29ad6d68f2e756dbe2312a2b9f9ac97005f4": {"filename": "TTRGame.vlt.228df23cb8_from_2abe2.bsdiff.bz2", "patchHash": "accebb8d5fd32d0ef4258617f9dc84108959f67a", "compPatchHash": "2f33412c0c348b868d4db291e84d4fed879b4372"}, "6b68c58c73e4b48bdb9a2adc574366d52249aea5": {"filename": "TTRGame.vlt.228df23cb8_from_6b68c.bsdiff.bz2", "patchHash": "0f1f53072f1c6f6dd99a1112f7edbf0aaf84b18f", "compPatchHash": "e48069bec0562e5f19905c4a7b560e02bee96999"}}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "phase_51.mf": {"dl": "phase_51.mf.8d687a28b9.bz2", "hash": "8d687a28b9f673912382a3ddac49fecbf45b9aa1", "compHash": "e0931209fb86575da8156879b51700af3de9d5e9", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "phase_8.mf": {"dl": "phase_8.mf.9d4a0d464d.bz2", "hash": "9d4a0d464df607037bfa6de98d4c36eb3f51f4db", "compHash": "e1b5cfbc618e12e8686b65774e82bb2cc3fd499f", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "winter_decorations.mf": {"dl": "winter_decorations.mf.6fdc23822d.bz2", "hash": "6fdc23822d6eb6d29080d936e73add729a95beea", "compHash": "0e097ea07c5593c5045e4a8888f82a34c37d82de", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "phase_5.mf": {"dl": "phase_5.mf.6089c470b6.bz2", "hash": "6089c470b69f337563af6d15eb4bac8d6987443e", "compHash": "94cced342390c4fc9f5776abbc3838df311e1709", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "phase_11.mf": {"dl": "phase_11.mf.cd416c1db7.bz2", "hash": "cd416c1db778e9bd03ff12ed5e1aca872a729e9d", "compHash": "7ce11d53c387fe7c2ea83e227f1b96e21ca99cf9", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "phase_4.mf": {"dl": "phase_4.mf.f96620b303.bz2", "hash": "f96620b303a227d0af4b778c949b2e5e4c8e6d78", "compHash": "22c6675b3f00d319f10fe7a1a04ca6afa55774b8", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "phase_5.5.mf": {"dl": "phase_5.5.mf.d38ce49034.bz2", "hash": "d38ce49034f8b3959a0af4874a5b151888426a98", "compHash": "2a8626938eda1a8f22bfff5aaff7b2851e25655f", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "phase_14.mf": {"dl": "phase_14.mf.d2b6f35177.bz2", "hash": "d2b6f35177decba7051fbe6b8a1778e7c074b1bb", "compHash": "0eaa3d18df4ad0b1e11c3f64e53c789e2e349882", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "phase_7.mf": {"dl": "phase_7.mf.5eb81e8178.bz2", "hash": "5eb81e8178aaa74beb0f0b0b4c48278079b92db4", "compHash": "cbed9c38169b8b11e3a56876e2e964915b2a5723", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "phase_3.mf": {"dl": "phase_3.mf.a847b3e3a6.bz2", "hash": "a847b3e3a6729845837327025343d76c3d3479fe", "compHash": "02817afdb9b98545944aef79d569a60c83065cd9", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "phase_6.mf": {"dl": "phase_6.mf.b92786ec6f.bz2", "hash": "b92786ec6f070f748097b02b51344935fe17a8c1", "compHash": "8a875c855d2f276b775c5d9ec33f4dc6d2484848", "patches": {}, "only": ["darwin", "linux", "linux2", "win32", "win64"]}, "libopenal.so.1": {"dl": "libopenal.so.1.00c072bae9.bz2", "hash": "00c072bae9306db334fd26ea077df96b2cc21c83", "compHash": "45a7b884022dd395386d7e5e1ff41b044c02f6ac", "patches": {}, "only": ["linux", "linux2"]}, "TTREngine": {"dl": "TTREngine.3a43ea714a.bz2", "hash": "3a43ea714a44a005bf6c3fc6ce11dd1ff3949ea8", "compHash": "ea1f5ec6c3b484e76948309564a316c5c56fce3c", "patches": {}, "only": ["linux", "linux2"]}, "OpenAL32.dll": {"dl": "OpenAL32.dll.7a3f153aa4.bz2", "hash": "7a3f153aa484edc4c040f559b832ad0940351a81", "compHash": "8c4ed3117e013eb0cc768df05b2d6789216e5709", "patches": {}, "only": ["win32"]}, "TTREngine.exe": {"dl": "TTREngine.exe.e797976df7.bz2", "hash": "e797976df7e484f5809e0c3189dd5a011d59fb6a", "compHash": "ddc4af14aaa112f21495038aa999a66949253d86", "patches": {}, "only": ["win32"]}, "TTREngine64.exe": {"dl": "TTREngine64.exe.1ef17aa7f5.bz2", "hash": "1ef17aa7f5bf6e3e3cee3e430c2c03d2f8c9908d", "compHash": "8a5d1842532b0cca71b5f7ea6949bd73d330aad8", "patches": {}, "only": ["win64"]}, "OpenAL64.dll": {"dl": "OpenAL64.dll.92665077fe.bz2", "hash": "92665077fe52265cdc63b452b3ef413825b1e84d", "compHash": "9b1405f6903090d453f13e36353ccaf40f9a3490", "patches": {}, "only": ["win64"]}}
    """
    

    # Download patch manifest file
    response = requests.get(patch_manifest_url)
    patch_manifest = response.text
    # make a directory for storing the game files
    if not os.path.exists("Toontown Rewritten"):
        os.mkdir("Toontown Rewritten")
    os.chdir("Toontown Rewritten")
    
    # convert the patch manifest to a dictionary
    patch_manifest = eval(patch_manifest)

    # loop through the patch manifest
    for file in patch_manifest:
        # check if the file is in the user's os
        if sys.platform not in patch_manifest[file]["only"]:
            continue


        

    
        download_file(content_mirror_url, file, patch_manifest, headers)
        # TODO estimate percentage of completion
    if os.getcwd().split("/")[-1] == "Toontown Rewritten":
        os.chdir("..")
    
def toon_guard_authenticate(username, password):
    print("Enter your toonguard code, or type 'resend' to resend the code.")
    toonguard_code = input("Toonguard code: ")
    if toonguard_code == "resend":
        while True:
            login_data = login(username, password)
            print(f"Partial login: {login_data['banner']}")
            print("Enter your toonguard code, or type 'resend' to resend the code.")
            toonguard_code = input("Toonguard code: ")
            if toonguard_code != "resend":
                break
        print(login_data)
        # auth token is the token sent in the partially authenticated response
        auth_token = login_data["authToken"]
        login(username, password, toonguard_code=toonguard_code, auth_token=auth_token)


def check_if_still_queued(username, password, queue_token):
    still_queued = True
    while still_queued:
        time.sleep(1)
        print('Checking if still queued...')
        login_data = login(username, password, queue_token=queue_token)
        if login_data["success"] == "delayed":
            print(f"Queued: {login_data['position']} in line, ETA: {login_data['eta']} seconds")
            # check the server again
            login(username, password, queue_token=queue_token)
        elif login_data["success"] == "true":
            still_queued = False
            print("Login successful.")
        else:
            # login failed
            print("Login failed: {}".format(login_data["banner"]))
            sys.exit(1)
# Main function
def main():
    # Patch manifest URL and content mirror URL
    patch_manifest_url = "https://cdn.toontownrewritten.com/content/patchmanifest.txt"
    content_mirror_url = "https://download.toontownrewritten.com/patches/"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    # Download files from the content mirror using patch manifest
    download_content_mirror_files(content_mirror_url, patch_manifest_url, headers)
    # before launching lets make sure everything is executable
    if sys.platform == "darwin":
       # make the Toontown Rewritten executable,  executable
         os.chmod("Toontown Rewritten/Toontown Rewritten", 0o755)
    

    username = input("Enter your Toontown Rewritten username: ")
    password = getpass.getpass("Enter your Toontown Rewritten password: ")

    login_data = login(username, password)

    if "success" in login_data and login_data["success"]:
        if login_data["success"] == "delayed":
            print(f"Queued: {login_data['position']} in line, ETA: {login_data['eta']} seconds")
            queue_token = login_data["queueToken"]
            check_if_still_queued(username, password, queue_token)
        elif login_data["success"] == "partial":
            print(f"Partial login: {login_data['banner']}")
            toon_guard_authenticate(username, password)
        elif login_data["success"] == "true":
            print("Login successful.")
        else:
            # login failed
            print("Login failed:".format(login_data["banner"]))
            sys.exit(1)
        

            
  
        print('Launching Toontown Rewritten...')
        os.environ["TTR_GAMESERVER"] = login_data["gameserver"]
        os.environ["TTR_PLAYCOOKIE"] = login_data["cookie"]
        


        # launch for mac 
        if sys.platform == "darwin":
            # if these directories don't exist, make them
            if not os.path.exists("Toontown Rewritten/Frameworks"):
                os.mkdir("Toontown Rewritten/Frameworks")

            subprocess.Popen(["Toontown Rewritten/Toontown Rewritten"])
        # launch for linux
        elif sys.platform == "linux":
            # make the TTREngine,  executable
            os.chmod("Toontown Rewritten/TTREngine", 0o755)
            subprocess.Popen(["Toontown Rewritten/TTREngine"])
        # launch for windows
        elif sys.platform == "win32":
            subprocess.Popen(["Toontown Rewritten/TTREngine.exe"])
       
                       
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
