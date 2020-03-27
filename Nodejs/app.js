var Twit = require('twit');
config = require('./config.js');
var T = new Twit(config);
//var T = new Twit(config.twitter);
params = { q: 'neo4j', count:100, lang:"en", since_id:620248636082024400 };
T.get('search/tweets', params, function(err, data, response) {
console.log(data);
});