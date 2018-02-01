/* updateCheck.js - Script to check for updates and change UI appropriately.
 * Copyright (C) Isaac Lenton (aka ilent2) 2017.
 */

var divOnline = document.getElementById("interface_online");
var divLatest = document.getElementById("interface_ok");
var divUpdate = document.getElementById("interface_update");
var divConnect = document.getElementById("interface_connect");

divOnline.style.display = "none";
divLatest.style.display = "none";
divUpdate.style.display = "none";
divConnect.style.display = "block";

// Set the current version
$("#interface\\_current").text("Current version: " + thisVersion);

if (window.location.hostname == "caisr.github.io") {
  divOnline.style.display = "block";
  divConnect.style.display = "none";
} else {

  // Set the latest version
  fetch('https://caisr.github.io/dicom2cloud/uiversion.js')
    .then(response => response.text())
    .then(function(text) {
      console.log(typeof text);
      var version = text.split("=")[1].trim().slice(1, -2);
      $("#interface\\_latest").text("Latest version: " + version);

      if (version == thisVersion) {
        divLatest.style.display = "block";
        divConnect.style.display = "none";
      } else if (version != thisVersion) {
        divUpdate.style.display = "block";
        divConnect.style.display = "none";
      }
    });
}

