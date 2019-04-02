#Author: Whoever's running https://github.com/malware-reversing
#Put this script in the same directory as all the binaries created using ps2exe
#It will create powershell files in the same directory for all binaries created using ps2exe with the same name but extension .ps1
#This is a rather hackish script, but it works.
#If it does not work, the most likely reason will be the argument sent to parse_file(). This argument is directly related to the length of the embedded powershell script. Just try from "48" (script contains a few chars) to probably max "52" (long script). It's just that in my testing the script length was always "51", so I didn't spend too much time future proofing the script.


import base64
import os

directory = os.getcwd() + "\\";
files = []
for r, d, f in os.walk(directory):
  for file in f:
    files.append(os.path.join(r, file))

def parse_file(index_increment):
  start_index = file_contents.find(b'\x3C\x00\x66\x00\x69\x00\x6C\x00\x65\x00\x6E\x00\x61\x00\x6D\x00\x65\x00\x3E\x00\x22\x00\x01\x09\x2D\x00\x65\x00\x6E\x00\x64\x00\x01\x0D\x2D\x00\x64\x00\x65\x00\x62\x00\x75\x00\x67\x00');
  substring_contents = file_contents[start_index+index_increment:];
  end_index = substring_contents.find(b'\x00\x2f\x5e');
  substring_contents = substring_contents[0:end_index];
  substring_contents = substring_contents.replace(b'\x00',b'');
  substring_contents = substring_contents.decode("utf-8");
  powershell_code = base64.b64decode(substring_contents);
  powershell_file = open(f+".ps1","wb+"); #Create new powershell file with the extracted powershell script
  powershell_file.write(powershell_code);
  powershell_file.close();

for f in files:
  open_file = open(f, "rb");
  file_contents = open_file.read();
  open_file.close();
  if file_contents[0]==77 and file_contents[1]==90: #File starts with "MZ"
    try:
      parse_file(49); #can even be 48d for the shortest strings, so it seems like the longer the encoding is, then the bigger the number (so a catch-most script would go from 48-52 or something like that)
    except:
      try:
        parse_file(51);
      except:
        print("Could not resolve for file: " + f);
