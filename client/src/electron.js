const { app, BrowserWindow } = require('electron');
const path = require('path');
const url = require('url');
const { spawn } = require('child_process');

let mainWindow;
let flaskApp; // Declare flaskApp variable here so it's accessible throughout the file

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 480,
    show: true,
    icon: path.join(__dirname, 'assets/images/logo.png'),
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

  // used for launching browser with console open
  // mainWindow.webContents.openDevTools();

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Start Flask app
  const flaskAppPath = path.join(__dirname, 'music_master_backend');
  console.log(`Flask app path: ${flaskAppPath}\n`);

  flaskApp = spawn(flaskAppPath, { // Assign the spawned process to the flaskApp variable
    cwd: __dirname,
  });

  flaskApp.stdout.on('data', (data) => {
    console.log(`Flask stdout: ${data}\n`);
  });

  flaskApp.stderr.on('data', (data) => {
    console.log(`Flask stderr: ${data}\n`);
  });

  flaskApp.on('close', (code) => {
    console.log(`Flask app exited with code ${code}\n`);
  });
}

app.on('ready', () => {
  createWindow();
});

app.on('window-all-closed', () => {
  if (flaskApp) {
    flaskApp.kill();
  }
  app.quit();
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// const unpackedPath = electronUtil.fixPathForAsarUnpack(backend); // this is supposed to allow asar = true
// https://github.com/sindresorhus/electron-util#fixpathforasarunpackpath
// cant get proper import of electron-util to work
// solution for now is to set asar = false in package.json

// let backend;
// backend = path.join(__dirname, 'music_master_backend');

// var execfile = require('child_process').execFile;
// console.log(`Flask app path: ${backend}\n`);

// execfile( backend, {windowsHide: true,},
// (err, stdout, stderr) => {
//     if (err) {
//         console.log(`open Flask err: ${err}\n`);
//     }
//     if (stdout) {
//         console.log(`open Flask stdout: ${stdout}\n`);
//     }
//     if (stderr) {
//         console.log(`open Flask stderr: ${stderr}\n`);
//     }
// })
