# Butler
To install cmake \n
apt install cmake

To install Flatbuffer
cd tools/
git clone https://github.com/google/flatbuffers.git
cd flatbuffers
cmake -G "Unix Makefiles" (install cmake if need)
make

To install npm & required modules
apt install npm
npm install redis
npm install log4js
npm install express-ws
npm install express
NOTE: All npm modules goes to "/usr/local/lib/node_modules/"

To install nodejs
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install -y nodejs
