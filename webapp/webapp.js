Comps = new Mongo.Collection("comps");

if (Meteor.isClient) {

  Template.testsBoard.helpers({
    tests: function () {
      return Comps.find({});
    }
  });

  Template.testsBoard.events({
    'click button': function () {
      // increment the counter when button is clicked
      Session.set("counter", Session.get("counter") + 1);
    }
  });
}

if (Meteor.isServer) {
  Meteor.startup(function () {
  });

    //Declare the methods on the server that can be accessed by the client
  var supercalback = function (error, stdout, stderr) {
        if (error) console.log(error);
        if (stdout) console.log(stdout);
        if (stderr) console.log(stderr);
    };

  var executePythonSPCA = function (args, callback) {
    Meteor.npmRequire('child_process').exec("python " + "/Users/mcoenca/Documents/Thnktwice/Code/sviep-bigdata-python/main.py", callback);
  };

  var wrappedPythonSPCA = Meteor.wrapAsync(executePythonSPCA);

  Meteor.methods({
    executeSPCA: function(args) {
      if (!this.isSimulation){
        console.log("Starting spca...");
        return wrappedPythonSPCA({}, supercalback);
      }
    }
  });  
}
