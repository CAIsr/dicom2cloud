/* submit.js - MVC setup for job submission page.
 * Copyright (C) Isaac Lenton (aka ilent2) 2017.
 */

function SubmitModel() {
  this.human_name = "";
  this.input_file = null;
  this.steps = [];
}

SubmitModel.prototype.containsCloudStep = function() {
  // TODO
  return false;
}

function SubmitView(model, id) {
  this.model = model;
  this.div = document.getElementById(id);
  this.update();
}

SubmitView.prototype.clear = function() {
  this.div.innerHTML = "";
}

SubmitView.prototype.addHeader = function() {

  var html = `<div class="listHead">
    <div class="col0">Order</div>
    <div class="col1">Job Step</div>
    <div class="col2"></div>
  </div>
  `;

  this.div.innerHTML += html;
}

SubmitView.prototype.addInstructions = function() {

  var html = `<div class="listItem">
    <div class="col0"></div>
    <div class="col1">Select a job step from the above list and click add</div>
    <div class="col2"></div>
  </div>
  `;

  this.div.innerHTML += html;
}

SubmitView.prototype.addCloudAnonymise = function() {

  var html = `<div class="listItem">
    <div class="col0"></div>
    <div class="col1">Anonymise locally (required for cloud job)</div>
    <div class="col2"></div>
  </div>
  `;

  this.div.innerHTML += html;
}

SubmitView.prototype.addJobStep = function(idx, jobStep) {

  // TODO: Change this from being an example job step

  var html = `<div class="listItem">
    <div class="col0"><input type="text" value="0"/></div>
    <div class="col1">This is a example Job Step</div>
    <div class="col2"><button>Remove</button></div>
  </div>
  `;

  this.div.innerHTML += html;
}

SubmitView.prototype.update = function() {

  this.clear();
  this.addHeader();

  if (this.model.steps.length == 0) {
    this.addInstructions();
  } else {

    // Add anonymise step if we have a cloud step
    if (this.model.containsCloudStep()) {
      this.addCloudAnonymise();
    }

    // Add job steps
    for (var i = 0, step; step = this.model.steps[i]; ++i) {
      this.addJobStep(i, step);
    }
  }
}

// Setup the controls in the document
// The controls should tell the view to update when changed
function SubmitControls(model, view) {
  this.buttonSubmit = document.getElementById("buttonSubmit");
  this.buttonReset = document.getElementById("buttonReset");
  this.buttonReceipt = document.getElementById("buttonReceipt");

  this.textareaReceipt = document.getElementById("textareaReceipt");

  this.textName = document.getElementById("textName");
  this.fileInput = document.getElementById("fileInput");

  this.selectJobStep = document.getElementById("selectJobStep");

  // TODO: Setup callbacks
}

//
// Instantiation
//

var submitModel = new SubmitModel();
var submitView = new SubmitView(submitModel, "jobSteps");
var submitControls = new SubmitControls(submitModel, submitView);

