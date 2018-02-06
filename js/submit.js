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

SubmitModel.prototype.addStep = function(name) {
  this.steps.push(name);
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

  var row = document.createElement("div");
  row.classList.add('listItem');

  var col0 = document.createElement("div");
  col0.classList.add('col0');
  var rowid = document.createElement("input");
  rowid.setAttribute("type", "text");
  rowid.setAttribute("value", idx.toString());
  col0.appendChild(rowid);
  row.appendChild(col0);

  var col1 = document.createElement("div");
  col1.classList.add('col1');
  col1.innerHTML = jobStep;
  row.appendChild(col1);

  var col2 = document.createElement('div');
  col2.classList.add('col2');
  var rmbutton = document.createElement('button');
  var that = this;
  rmbutton.onclick = function() {
    that.model.steps.splice(idx, 1);
    that.update();
  }
  rmbutton.innerHTML = "Remove";
  col2.appendChild(rmbutton);
  row.appendChild(col2);

  this.div.appendChild(row);
  console.log(this.div.childNodes.length);
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

  this.buttonAdd = document.getElementById("buttonAdd");
  this.buttonReorder = document.getElementById("buttonReorder");
  this.selectJobStep = document.getElementById("selectJobStep");

  var that = this;

  //
  // Setup callbacks
  //

  this.buttonSubmit.addEventListener('click', function() {
    // TODO
  });
  this.buttonReset.addEventListener('click', function() {
    // TODO
  });
  this.buttonReceipt.addEventListener('click', function() {
    // TODO
  });

  this.buttonAdd.addEventListener('click', function() {
    model.addStep(that.selectJobStep.value);
    view.update();
  });

  this.buttonReorder.addEventListener('click', function() {
    // TODO
  });

  this.textName.addEventListener("change", function() {
    // TODO
  });

  this.fileInput.addEventListener("change", function() {
    // TODO
  });
}

//
// Instantiation
//

var submitModel = new SubmitModel();
var submitView = new SubmitView(submitModel, "jobSteps");
var submitControls = new SubmitControls(submitModel, submitView);

