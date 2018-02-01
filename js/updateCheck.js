/* updateCheck.js - Script to check for updates and change UI appropriately.
 * Copyright (C) Isaac Lenton (aka ilent2) 2017.
 */

var divOnline = document.getElementById("interface_online");
var divLatest = document.getElementById("interface_latest");
var divUpdate = document.getElementById("interface_update");
var divConnect = document.getElementById("interface_connect");

divOnline.style.display = "none";
divLatest.style.display = "none";
divUpdate.style.display = "none";
divConnect.style.display = "block";

// Set the current version
$("#interface\\_current").text("Current version: " + thisVersion);

// Set the latest version
fetch('https://caisr.github.io/dicom2cloud/uiversion.js')
  .then(response => response.text())
  .then(text => $("#interface\\_latest").html(text));


