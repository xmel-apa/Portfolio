// Carregando modulos
const express = require('express');
const handlebars = require('express-handlebars');
const bodyParser = require('body-parser');
const app = express();
const admin = require("./routes/admin");
const path = require('path');
//const sequelize = require('sequelize');
//Configuracoes
//Body Parser
 app.use(bodyParser.urlencoded({extended: true}));
 app.use(bodyParser.json());
//Handlebars
 app.engine('handlebars', handlebars.engine({defaultLayout: 'main',
    runtimeOptions:{
      allowProtoPropertiesByDefault: true,
      allowProtoMethodsByDefault: true
    }
}));
 app.set('View engine', 'handlebars');
//Postegres

//Mongoose
  /*mongoose.Promise = global.Promise;
  mongoose.connect("mongodb://localhost:27017/CT").then(()=>{
    console.log("Conectado ao mongo")
  }).catch((err)=>{
    console.log("Falha ao se conectar",+err)
  });*/
    
//Public
 app.use(express.static(path.join(__dirname + '/public')));
//Rotas
 app.use('/admin', admin);
//Outros
const PORT = 8088;
app.listen(PORT, function(){
    console.log('Servidor rodando!')
});