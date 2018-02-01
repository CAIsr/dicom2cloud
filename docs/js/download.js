/* download.js - Downloads a dicom2cloud user interface using GitZip.
 * Copyright (C) Isaac Lenton (aka ilent2) 2017.
 */

// From SO/a/21903119/2372604
function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

var version = getUrlParameter('ver');
console.log(version);
if (version !== undefined) {
  GitZip.zipRepo("https://github.com/CAIsr/dicom2cloud/"
      + version + "/docs");
}

