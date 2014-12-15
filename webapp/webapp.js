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
        if (stdout) {
          console.log(stdout);

        }
        if (stderr) console.log(stderr);
    };
  var dictToString = function (args_dict) {
    res = "";
    res = res + args_dict.matrix_path + " " + 
    args_dict.n_lines + " " +
    args_dict.n_col + " " +
    args_dict.word_path + " " +
    args_dict.k + " " +
    args_dict.h + " " +
    args_dict.n_components + " " +
    args_dict.norm_row + " " +
    args_dict.precision;
    console.log(res);
    return res;
  };

  var executePythonSPCA = function (args_string, callback) {
    Meteor.npmRequire('child_process').exec("python " + "/Users/mcoenca/Documents/Thnktwice/Code/sviep-bigdata-python/call_spca.py " + args_string, callback);
  };

  var wrappedPythonSPCA = Meteor.wrapAsync(executePythonSPCA);

  Meteor.methods({
    executeSPCA: function(args_dict) {
      // args = []; args[0]=
      // args_dict = {matrix_path: "/Users/mcoenca/Documents/Thnktwice/Code/data/many-results_matrix.csv", n_lines: "2950", n_col: "9000", word_path: "/Users/mcoenca/Documents/Thnktwice/Code/data/many-results_words.csv", k:"10", h:"8000", n_components: "2", norm_row: "True", precision: "1.0e-8"};
      var args_string = dictToString(args_dict);
      if (!this.isSimulation){
        console.log("Starting spca...");
        return wrappedPythonSPCA(args_string, supercalback);
      }
    }
  });  
}
