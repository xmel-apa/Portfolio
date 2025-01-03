const express = require('express');
const router = express.Router();
const sequelize = require("sequelize");
const Categoria = require("../models/Categoria.js");
const login = require("../views/admin/selecaousuario.handlebars");

router.get('/', function(req, res){
    res.render('./admin/index.handlebars') 
});

router.get('/posts', function(req, res){
    res.send('Página de posts')
});

router.get('/categoria', function(req, res){
    res.render("./admin/categoria.handlebars")
});

/*router.get('/categoria/add', function(req, res){
    res.render("./admin/addcategoria.handlebars")
});*/

router.get('/login', function(req, res){
    res.render("./admin/login.handlebars")
});

router.get('/selecao', function(req, res){
    res.render("./admin/selecaousuario.handlebars")
});

/*router.post('/categoria/nova', (req, res) => {
   Categoria.create({ 
    nome: req.body.nome,
    slug: req.body.slug
   }).then(() => {
    console.log("Categoria salva com sucesso!")
   }).catch((err) =>{
    console.log("Erro ao salvar categoria",+err)
   })
});*/

module.exports = router;