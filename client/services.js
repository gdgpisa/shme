var Services_serverStatus = "Offline"
let Services_server = null
var Services_ResponseHandler = function (data) { }
var Services_CloseHandler = function (data) { }
var Services_OpenHandler = function () { }
function Services_connect() {
    try {
        Services_server = new WebSocket("wss://my.awesome.domain:5000")
        Services_server.onmessage = function (event) {
            if (event.data instanceof Blob) {
                reader = new FileReader()
                reader.onload = function () {
                    console.log(reader.result)
                    let received = JSON.parse(reader.result)
                    if (Services_serverStatus == "connected" && received.code == 200) { Services_serverStatus = "logged" }
                    Services_ResponseHandler(received)
                }
                reader.readAsText(event.data)
            } else {
                let received = JSON.parse(event.data)
                if (Services_serverStatus == "connected" && received.code == 200) { Services_serverStatus = "logged" }
                Services_ResponseHandler(received)
            }
        }
        Services_server.onopen = function () {
            Services_serverStatus = "connected"
            console.log("connection ready")
            Services_OpenHandler()
        }
        Services_server.onclose = Services_CloseHandler
    }
    catch (ex) { new Snackbar("Server Irragiungibile") }
}
function Services_auth(login, pass) {
    let message = { "code": 0, "id": login, "pw": pass }
    console.log("messaggio di autenticazione")
    if (Services_serverStatus == "connected") {
        console.log("inviato")
        Services_server.send(JSON.stringify(message))
        return !0
    }
    return !1
}
function Services_sendMessage(operation, value) {
    let message = { "code": 100, "op": operation, "val": value }
    console.log(message)
    if (Services_serverStatus == "logged") {
        Services_server.send(JSON.stringify(message))
        return !0
    }
    return !1
}
