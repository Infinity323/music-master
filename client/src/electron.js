const { app, BrowserWindow } = require('electron');
const path = require('path');
const url = require('url');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;

// Create a writable stream to the log file
const logStream = fs.createWriteStream(path.join(app.getPath('userData'), 'debug.log'), { flags: 'a' });

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 500,
        webPreferences: {
            nodeIntegration: true,
        },
    });

    const startUrl = process.env.ELECTRON_START_URL || url.format({
        pathname: path.join(__dirname, '/../build/index.html'),
        protocol: 'file:',
        slashes: true,
    });

    mainWindow.loadURL(startUrl);

    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    let backend;
    backend = path.join(__dirname, 'music_master_backend');

    // const unpackedPath = electronUtil.fixPathForAsarUnpack(backend); // this is supposed to allow asar = true
    // https://github.com/sindresorhus/electron-util#fixpathforasarunpackpath
    // cant get proper import of electron-util to work
    // solution for now is to set asar = false in package.json

    var execfile = require('child_process').execFile;
    logStream.write(`Flask app path: ${backend}\n`);
    fs.readdir(__dirname, (err, files) => {
        logStream.write(`Contents of directory: ${files.join(', ')}\n`);
    });

    execfile( backend, {windowsHide: true,},
    (err, stdout, stderr) => {
        if (err) {
            logStream.write(`open Flask err: ${err}\n`);
        }
        if (stdout) {
            logStream.write(`open Flask stdout: ${stdout}\n`);
        }
        if (stderr) {
            logStream.write(`open Flask stderr: ${stderr}\n`);
        }
    })
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        if (backend) {
            backend.kill();
        }
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

    // Start Flask app
    // const flaskAppPath = path.join(__dirname, 'music_master_backend');
    // logStream.write(`Flask app path: ${flaskAppPath}\n`);
    // fs.readdir(__dirname, (err, files) => {
    //     logStream.write(`Contents of directory: ${files.join(', ')}\n`);
    // });
    // const flaskApp = spawn([flaskAppPath], {
    //     cwd: __dirname,
    // });

    // flaskApp.stdout.on('data', (data) => {
    //     logStream.write(`Flask stdout: ${data}\n`);
    // });

    // flaskApp.stderr.on('data', (data) => {
    //     logStream.write(`Flask stderr: ${data}\n`);
    // });

    // flaskApp.on('close', (code) => {
    //     logStream.write(`Flask app exited with code ${code}\n`);
    // });