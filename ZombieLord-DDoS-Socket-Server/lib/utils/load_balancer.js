const {SocketService} = require("../classes/client_socket_list");
const { Client,ClientLocation } =  require("../classes/client");
let lastPicked = 0;
//Round Robin
function areServersAvailable(campus){
    let tempClientList = [...SocketService.clientsList];
    if(campus == "chs"){ // Special case
        tempClientList = tempClientList.filter(client => client.serverLocation != ClientLocation.global);
    }
    console.log(tempClientList.length);
    return tempClientList.length >0;
}
function pickClient(campus){
    let tempClientList = [...SocketService.clientsList];
    if(campus == "chs"){
        tempClientList = tempClientList.filter(client => client.serverLocation != ClientLocation.global);
    }
    let pick = lastPicked+1>tempClientList.length-1? 0 : lastPicked+1;
    lastPicked = pick;
    return tempClientList[pick];

}
module.exports = {pickClient,areServersAvailable}