"use strict";

const sucks = require("sucks"),
  EcoVacsAPI = sucks.EcoVacsAPI,
  VacBot = sucks.VacBot,
  nodeMachineId = require("node-machine-id");

let account_id = process.env.EMAIL,
  password = process.env.PASSWORD,
  password_hash = EcoVacsAPI.md5(password),
  device_id = EcoVacsAPI.md5(nodeMachineId.machineIdSync()),
  country = "us",
  continent = "na";

let api = new EcoVacsAPI(device_id, country, continent);

exports.handler = (event, context, callback) => {
  api
    .connect(
      account_id,
      password_hash
    )
    .then(() => {
      api.devices().then(devices => {
        let vacuum = devices[0];
        let vacbot = new VacBot(
          api.uid,
          EcoVacsAPI.REALM,
          api.resource,
          api.user_access_token,
          vacuum,
          continent
        );
        vacbot.on("ready", event => {
          vacbot.run("batterystate");
          vacbot.run("clean");
          const duration = 1000 * 60 * 30;
          setTimeout(() => {
            vacbot.run("stop");
            vacbot.run("charge");
          }, duration);

          vacbot.on("BatteryInfo", battery => {
            console.log("Battery level: %d%", Math.round(battery * 100));
          });
        });
        vacbot.connect_and_wait_until_ready();
      });
    })
    .catch(e => {
      console.error("Failure in connecting!");
    });
};
