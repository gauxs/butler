# Butler

Butler is a hackathon project we implemented at [Riverbed](https://www.riverbed.com/) hackathon of 2019.

## Installation

1. cmake

   ```
   apt install cmake
   ```

2. Flatbuffer

   ```
   cd tools
   git clone https://github.com/google/flatbuffers.git
   cd flatbuffers
   cmake -G "Unix Makefiles" (install cmake if need)
   make
   ```

3. npm & required modules

   ```
   apt install npm
   npm install redis
   npm install log4js
   npm install express-ws
   npm install express
   npm install ws
   npm install redis
   **NOTE:** All npm modules goes to "/usr/local/lib/node_modules/"
   ```

4. nodejs

   ```
   curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash
   sudo apt-get install -y nodejs
   ```
