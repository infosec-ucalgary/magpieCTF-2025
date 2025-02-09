const express = require("express");
const cookieParser = require('cookie-parser');
var path = require('path');
const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(cookieParser());

app.get('/', (req, res)=>{
    res.cookie('wgrj', 'iirkb', { 
        httpOnly: true, 
        secure: true, // set to true if using HTTPS
        sameSite: 'lax'
    });
    res.sendFile(path.join(__dirname, 'public', 'home.html'));
});

app.get('/hidden', (req, res)=>{
    const user = req.cookies.wgrj
    if (user != 'crzav'){
        res.status(200);
        res.sendFile(path.join(__dirname, 'public', 'hidden.html'));
    } else {
        res.status(200);
        res.sendFile(path.join(__dirname, 'public', 'flag.html'));
    }
});

app.listen(PORT, (error) =>{
    if(!error)
        console.log("Server is Successfully Running, and App is listening on port "+ PORT)
    else 
        console.log("Error occurred, server can't start", error);
    }
);