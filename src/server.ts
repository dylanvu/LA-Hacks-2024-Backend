import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import http from "http";
import WebSocket from "ws";

// load up dotenv stuff
dotenv.config();

const app = express();
const port = 5000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors({
    origin: '*'
}))

const server = http.createServer(app);

const wss = new WebSocket.Server({ server }); 

let clients: WebSocket[] = [];

wss.on("connection", (socket) => {
    console.log("A user has connected!");
    clients.push(socket);
    console.log(clients.length + " clients connected"); // number of
    socket.send("I see you!");
    socket.on("message", (data) => {
        console.log("Received: " + data);
        clients.forEach(function (client) {
            client.send(data);
        });
    });
});

wss.on("close", (socket: WebSocket) => { 
    console.log("A user has disconnected!");
    clients = clients.filter((client) => client !== socket);
    }
);

app.get('/', (req, res) => {
    res.send("Hello World!");
});

server.listen(port, () => {
    console.log(`Example app listening on http://localhost:${port}`);
});