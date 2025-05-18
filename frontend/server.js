// load the things we need
var express = require('express');
const axios = require('axios');
const bodyParser  = require('body-parser');
const path = require('path');


var app = express();

app.use(bodyParser.urlencoded({extended: false}));
// set the view engine to ejs
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(bodyParser.json());


app.get("/", function(request, response){
    response.render("page/login",{
    })
});

//LOGIN PAGE AUTHORIZATION
app.post('/login', function(req, res){
    var user = req.body.username;
    var password = req.body.password;
    if(user === 'admin' && password === 'password')
    {
        res.render('page/home.ejs', {
            user: user,
            auth: true
        });
    }
    else
    {
        res.render('page/unauthorize.ejs', {
            user: 'UNAUTHORIZED',
            auth: false
        });
    }
  })

app.get("/home", function(request, response){
    response.render("page/home",{
    })
});

//--------------------------------------------CAPTAIN-------------------------------------------------------------------------------------------------

//CAPTAIN GET PAGE

app.get("/captaininfo", function(request, response){
    axios.get(`http://127.0.0.1:5000/api/captain`)
    .then((res)=>{
        var captain = res.data;
        console.log(captain);

        response.render("page/captaininfo",{
            data: captain
        })
    });
});

//CAPTAIN ADD
//Redirect to the same page after added data.
app.post("/captainadd", function(request, response){
    var firstname = request.body.firstname;
    var lastname = request.body.lastname;
    var rank = request.body.Rank;
    var planet= request.body.homeplanet;
    axios.post(`http://127.0.0.1:5000/api/captain`,{  
          firstname: firstname,
          lastname: lastname,
          ranks: rank,
          homeplanet: planet
    })
    .then(function(res){
        response.redirect("/captaininfo");
    })
});

//CAPTAIN UPDATE
app.post("/updatecaptain", function(request, response){
    var cptfirstname = request.body.captainfn;
    var cptlastname = request.body.captainln;
    var firstname = request.body.ufirstname;
    var lastname = request.body.ulastname;
    var rank = request.body.uRank;
    var homeplanet= request.body.uhomeplanet;
    axios.put(`http://127.0.0.1:5000/api/captain`,{  
        
        selectfname: cptfirstname,
        selectlname: cptlastname,
        firstname: firstname,
        lastname: lastname,
        ranks: rank,
        homeplanet: homeplanet
        
    })
    .then(function(res){
        response.redirect("/captaininfo");
    })
    .catch(function(err) {
        console.error('Error updating captain:', err);
        response.status(500).send('An error occurred while updating the captain.');
    });
});

//DELETE CAPTAIN FUNCTION
app.post("/deletecaptain", function(request, response){
    var delete_f = request.body.delete_first;
    var delete_l = request.body.delete_last
    axios.delete(`http://127.0.0.1:5000/api/captain`,{  
        data: {
        firstname: delete_f,
        lastname: delete_l 
        } 
            
        })
    .then(function(res){
        response.redirect("/captaininfo");
    })
    .catch(function(err) {
        console.error('Error deleting captain:', err);
        response.status(500).send('An error occurred while deleting captain.');
    });
});
//--------------------------------------------SPACESHIP-------------------------------------------------------------------------------------------------
//GET SPACESHIP DATA
app.get("/spaceship", function(request, response){
    axios.get(`http://127.0.0.1:5000/api/spaceship`)
    .then((res)=>{
        var ship = res.data;
        console.log(ship);

        response.render("page/spaceship",{
            shipdata: ship
        })
    });
});

//ADD SHIP DATA

app.post("/shipadd", function(request, response){
    var captainfname = request.body.captainfname;
    var captainlname = request.body.captainlname;
    var shipweight = request.body.shipweight;
    var shipname = request.body.shipname;
    axios.post(`http://127.0.0.1:5000/api/spaceship`,{  
        captainfname: captainfname,
        captainlname: captainlname,
        shipname: shipname,
        maxweight: shipweight
  })
  .then(function(res){
      response.redirect("/spaceship");
  })
});

//UPDATE SHIP DATA
app.post("/updateship", function(request, response){
    var shipname = request.body.shipname;
    var captainfname = request.body.captainfname;
    var captianlname = request.body.captainlname;
    var maxweight = request.body.shipweight;
    var ship = request.body.newshipname;
    axios.put(`http://127.0.0.1:5000/api/spaceship`,{  
        shipname: shipname,
        captainfname: captainfname,
        captainlname: captianlname,
        maxweight: maxweight,
        newshipname: ship
        
    })
    .then(function(res){
        response.redirect("/spaceship");
    })
    .catch(function(err) {
        console.error('Error updating spaceship:', err);
        response.status(500).send('An error occurred while updating the spaceship.');
    });
});

//DELETE SPACESHIP

//DELETE SHIP FUNCTION
app.post("/deleteship", function(request, response){
    var id = request.body.id_delete;
    axios.delete(`http://127.0.0.1:5000/api/spaceship`,{  
        data: {
            shipname: id 
            }
        })
    .then(function(res){
        response.redirect("/spaceship");
    })
    .catch(function(err) {
        console.error('Error deleting spaceship:', err);
        response.status(500).send('An error occurred while deleting spaceship.');
    });
});


//CARGO GET PAGE
app.get("/cargo", function(request, response){
    axios.get(`http://127.0.0.1:5000/api/cargo`)
    .then((res)=>{
        var cargo = res.data;
        console.log(cargo);

        response.render("page/cargo",{
            cargodata: cargo
        })
    });
});

//ADD CARGO DATA

app.post("/addcargo", function(request, response){
    var cargoid = request.body.cargoid;
    var shipname = request.body.shipname;
    var cargotype = request.body.cargotype;
    var weight = request.body.weight;
    var departure = request.body.departure;
    var arrival = request.body.arrival;
    axios.post(`http://127.0.0.1:5000/api/cargo`,{  
        cargo_id: cargoid,
        shipname: shipname,
        cargotype: cargotype,
        weight: weight,
        departure: departure,
        arrival: arrival

  })
  .then(function(res){
      response.redirect("/cargo");
  })
});

//UPDATE CARGO
//IF SHIPID DOES NOT EXIST, THE DATA WON'T UPDATE
app.post("/updatecargo", function(request, response){
    var cargoid = request.body.cargoid;
    var cargotype = request.body.cargotype;
    var newweight = request.body.weight;
    var departure = request.body.departure;
    var arrival = request.body.arrival;
    var shipname = request.body.shipname;

    console.log({
        cargoid: cargoid,
        weight: newweight,
        cargotype: cargotype,
        departure: departure,
        arrival: arrival,
        shipname: shipname
    });
    axios.put(`http://127.0.0.1:5000/api/cargo`,{  
        
        cargo_id: cargoid,
        weight: newweight,
        cargotype: cargotype,
        departure: departure,
        arrival: arrival,
        shipname: shipname
        
    })
    .then(function(res){
        response.redirect("/cargo");
    })
    .catch(function(err) {
        console.error('Error updating cargo:', err);
        response.status(500).send('An error occurred while updating the cargo.');
    });
});



//DELETE CARGO FUNCTION
app.post("/deletecargo", function(request, response){
    var id = request.body.id_delete;
    axios.delete(`http://127.0.0.1:5000/api/cargo`,{  
        data: {
            cargo_id: id 
            }
        })
    .then(function(res){
        response.redirect("/cargo");
    })
    .catch(function(err) {
        console.error('Error updating cargo:', err);
        response.status(500).send('An error occurred while deleting cargo.');
    });
});


app.listen(7000);
console.log('7000 is the magic port');