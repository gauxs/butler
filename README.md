# Butler

Butler is a hackathon project we implemented at [Riverbed Hackathon](https://www.riverbed.com/) of 2019. Butler is a system which collects and store data like restaurant details, location, food menu and price, from food delivery websites like FoodPanda, Zomato through a web crawler and answer queries like cheapest meal plan.

![Butler_Design](https://user-images.githubusercontent.com/5405553/160556870-2fdf7c33-9bbd-49f8-a4c8-0040e9b7a2a7.jpg)


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

## Conclusion

Although we didn't won the hackathon but did got special mention :grin:
