/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */
package com.mycompany.foodlabel;
import etiqueta.Produto;
import conexoes.ConexaoDB;
/**
 *
 * @author x542895
 */
public class FoodLabel {

    public static void main(String[] args) {
        System.out.println("Hello World!");
        
        Produto produto;
            
  //      ConexaoDB con = ConexaoDB.getConnection(); // obtém conexão
        
        String sql = """
        INSERT INTO produto (cod_produto,cod_categoria,cod_conservacao,cod_usuario,cod_validade,sif,lote,nome_produto,peso) VALUES 
        (nextval('sqproduto'),'3020','711','6','1311','092345','1301','Tomate','5') ;""";
      //  System.out.println(produto);
     //   produto.cadastrarProduto();
          
    }
}