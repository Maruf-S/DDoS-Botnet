const express = require("express");
const cors = require("cors");
const path = require("path");
const {static} = express;
const app = express();
const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server,{ cors: { origin: '*' } });
const bp = require("body-parser");
const routes = require("./routes/route");
app.use(bp.json());
app.use(cors());
app.use("/api", routes);
app.use(
  static(path.join(__dirname, './frontend/build'))
);
require("./sockets/socket")(io);
const PORT = process.env.PORT || 5000;
server.listen(PORT, async () => {
  console.log("listening on *:" + PORT);
});
