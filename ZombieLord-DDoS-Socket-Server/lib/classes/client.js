class ClientVersion {
  static v1 = 1;
}
class Client {
  id; //Socket Id
  name;
  socket;
  serverLocation;
  priority;
  version;
  busy = false;
  constructor({id, name, socket, version}) {
    this.id = id;
    this.name = name;
    this.socket = socket;
    this.version = version;
  }
}
class AttackType{
  static icmp = "ICMP";
  static syn = "SYN";
  static udp = "UDP";
}
module.exports = { Client, ClientVersion ,AttackType};
