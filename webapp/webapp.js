Comps = new Mongo.Collection("comps");

if (Meteor.isClient) {

  Template.testsBoard.helpers({
    tests: function () {
      return Comps.find({});
    }
  });

  Template.runExperimentForm.events({
    'click #submit_call': function (e, templ) {
       e.preventDefault();

      var args_dict = {};

      args_dict.matrix_path   = templ.$("#matrix_path").val();
      args_dict.word_path     = templ.$("#word_path").val();
      args_dict.n_lines       = templ.$("#n_lines").val();
      args_dict.n_col         = templ.$("#n_col").val();
      args_dict.k             = templ.$("#k").val();
      args_dict.h             = templ.$("#h").val();
      args_dict.n_components  = templ.$("#n_components").val();
      args_dict.norm_row      = templ.$("form input[type=radio]:checked").val();
      args_dict.precision     = templ.$("#precision").val();

      Meteor.call('executeSPCA', args_dict);
    },
    'submit form': function (e, templ) {
      e.preventDefault();

      var args_dict = {};

      args_dict.matrix_path   = templ.$("#matrix_path").val();
      args_dict.word_path     = templ.$("#word_path").val();
      args_dict.n_lines       = templ.$("#n_lines").val();
      args_dict.n_col         = templ.$("#n_col").val();
      args_dict.k             = templ.$("#k").val();
      args_dict.h             = templ.$("#h").val();
      args_dict.n_components  = templ.$("#n_components").val();
      args_dict.norm_row      = templ.$("form input[type=radio]:checked").val();
      args_dict.precision     = templ.$("#precision").val();

      Meteor.call('executeSPCA', args_dict);
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
    // res = res + process.env.PWD + "/assets/app" + args_dict.matrix_path + " " + 
    res = res + args_dict.matrix_path + " " +
    args_dict.n_lines + " " +
    args_dict.n_col + " " +
    // process.env.PWD + "/assets/app" + args_dict.word_path + " " +
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
    var file_path = process.env.PWD + "/private/call_spca.py ";
    // console.log(file_path);
    Meteor.npmRequire('child_process').exec("python " + file_path + args_string, callback);
  };

  var wrappedPythonSPCA = Meteor.wrapAsync(executePythonSPCA);

  Meteor.methods({
    executeSPCA: function(args_dict) {
      // args_dict = {matrix_path: "/Users/mcoenca/Documents/Thnktwice/Code/data/many-results_matrix.csv", n_lines: "2950", n_col: "9000", word_path: "/Users/mcoenca/Documents/Thnktwice/Code/data/many-results_words.csv", k:"10", h:"8000", n_components: "2", norm_row: "True", precision: "1.0e-8"};
      var args_string = dictToString(args_dict);
      if (!this.isSimulation){
        console.log("Starting spca...");
        return wrappedPythonSPCA(args_string, supercalback);
      }
    }
  });  
}