var Twit = require(' t wit');
config = require('./config.js');
var
T = new Twit(config);
params = { q: 'neo4j ', count:lOO, lang:"en", since_id:620248636082024400 };
T.get('search/tweets', params, function(err, data, response) {
console.log(data);
} ) ;