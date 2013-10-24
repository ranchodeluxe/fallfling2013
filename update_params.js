var params_json = require('./params.json');
var fs = require('fs');

/*
**
**  get source
**
*/
var source_body;
fs.readFile( './source.json', 'utf8', function( err, data ){

    if( err ){
        console.log( err );
    }

    source_body = data;

});


/*
**
**  save old params
**
*/
fs.writeFile( './params.json.backup', JSON.stringify( params_json ), function( err ){

    if ( err ){
        console.log( err );
    }

});

/*
**
**  swap it and 
**  save new params.json
**
*/
params_json.body = source_body;
fs.writeFile( './params.json', JSON.stringify( params_json ), function( err ){

    if ( err ){
        console.log( err );
    }

});



