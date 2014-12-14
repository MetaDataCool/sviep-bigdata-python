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
    // code to run on server at startup
  });
}
