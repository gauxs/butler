# Butler

Butler is a hackathon project we implemented at [Riverbed](https://www.riverbed.com/) hackathon of 2019.

## Installation

1. cmake

   ```
   apt install cmake<br/>
   ```

2. Flatbuffer

   ```cd tools/<br/>
   git clone https://github.com/google/flatbuffers.git<br/>
   cd flatbuffers<br/>
   cmake -G "Unix Makefiles" (install cmake if need)<br/>
   make
   ```

**To install npm & required modules**<br/>
apt install npm<br/>
npm install redis<br/>
npm install log4js<br/>
npm install express-ws<br/>
npm install express<br/>
npm install ws<br/>
npm install redis<br/>
npm install express<br/>
npm install express-ws<br/>
**NOTE:** All npm modules goes to "/usr/local/lib/node_modules/"<br/>

**To install nodejs**<br/>
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -<br/>
sudo apt-get install -y nodejs<br/>
