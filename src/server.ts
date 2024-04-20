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

wss.on("connection", (socket) => {
    console.log("A user has connected!");
    socket.send("I see you!");
});

app.get('/', (req, res) => {
    res.send("Hello World!");
});

server.listen(port, () => {
    console.log(`Example app listening on http://localhost:${port}`);
});