/**
 * 
 * :::: DOCUMENTATION from Lambda IFTTT template ::::
 * 
 * This is a sample that connects Lambda with IFTTT Maker channel. The event is
 * sent in this format: <serialNumber>-<clickType>.
 *
 * The following JSON template shows what is sent as the payload:
{
    "serialNumber": "GXXXXXXXXXXXXXXXXX",
    "batteryVoltage": "xxmV",
    "clickType": "SINGLE" | "DOUBLE" | "LONG"
}
 *
 * A "LONG" clickType is sent if the first press lasts longer than 1.5 seconds.
 * "SINGLE" and "DOUBLE" clickType payloads are sent for short clicks.
 *
 * For more documentation, follow the link below.
 * http://docs.aws.amazon.com/iot/latest/developerguide/iot-lambda-rule.html
 */

"use strict";

const https = require("https");
const iftttMakerKey = process.env.IFTTT_MAKER_KEY;

exports.handler = (event, context, callback) => {
  // Make sure you created a receipe for event IotButtonPress-<clickType>
  // on the IFTTT Webhooks channel from the dashboard.
  const webhookEvent = `IotButtonPress-${event.clickType}`;
  const url = `https://maker.ifttt.com/trigger/${webhookEvent}/with/key/${iftttMakerKey}`;
  https
    .get(url, res => {
      let body = "";
      console.log(`STATUS: ${res.statusCode}`);
      res.on("data", chunk => (body += chunk));
      res.on("end", () => {
        console.log(
          `Event ${event.clickType} has been sent to IFTTT Maker channel`
        );
        callback(null, body);
      });
    })
    .on("error", e => {
      console.log("Failed to trigger Maker channel", e);
      callback(`Failed to trigger Maker channel: ${e.message}`);
    });
};
