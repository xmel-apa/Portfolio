/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package etiqueta;

import caracteristicas.Conservacao;
import caracteristicas.Categoria;
import etiqueta.Validade;
import java.util.Scanner;
/**
 *
 * @author pamel
 */
public abstract class Produto implements Conservacao, Categoria{
    
    private String nome_produto;
    private String lote;
    private String sif;
    private float peso;
    private String responsavel_etiqueta;
    private String marca_fornecedor;
    private String id;
    
    public Produto(String nomeproduto, String lote, String sif, float peso, 
            String responsavel_etiqueta, String marca_fornecedor,
            String id){
        
    this.nome_produto=nome_produto;
    this.lote=lote;
    this.sif=sif;
    this.peso=peso;
    this.responsavel_etiqueta=responsavel_etiqueta;
    this.marca_fornecedor=marca_fornecedor;
    this.id=id;
    }

    /**
     * @return the nome_produto
     */
    public String getNome_produto() {
        return nome_produto;
    }

    /**
     * @param nome_produto the nome_produto to set
     */
    public void setNome_produto(String nome_produto) {
        this.nome_produto = nome_produto;
    }

    /**
     * @return the lote
     */
    public String getLote() {
        return lote;
    }

    /**
     * @param lote the lote to set
     */
    public void setLote(String lote) {
        this.lote = lote;
    }

    /**
     * @return the sif
     */
    public String getSif() {
        return sif;
    }

    /**
     * @param sif the sif to set
     */
    public void setSif(String sif) {
        this.sif = sif;
    }

    /**
     * @return the peso
     */
    public float getPeso() {
        return peso;
    }

    /**
     * @param peso the peso to set
     */
    public void setPeso(float peso) {
        this.peso = peso;
    }


    /**
     * @return the responsavel_etiqueta
     */
    public String getResponsavel_etiqueta() {
        return responsavel_etiqueta;
    }

    /**
     * @param responsavel_etiqueta the responsavel_etiqueta to set
     */
    public void setResponsavel_etiqueta(String responsavel_etiqueta) {
        this.responsavel_etiqueta = responsavel_etiqueta;
    }

    /**
     * @return the marca_fornecedor
     */
    public String getMarca_fornecedor() {
        return marca_fornecedor;
    }

    /**
     * @param marca_fornecedor the marca_fornecedor to set
     */
    public void setMarca_fornecedor(String marca_fornecedor) {
        this.marca_fornecedor = marca_fornecedor;
    }

    /**
     * @return the id
     */
    public String getId() {
        return id;
    }

    /**
     * @param id the id to set
     */
    public void setId(String id) {
        this.id = id;
    }
    
    public String getcadastrarProduto(){
        return cadastrarProduto();
}    
    
    public String cadastrarProduto(){
        return null;
} 
    
    public String getverificarProduto(){
        return verificarProduto();
}    

    public String verificarProduto(){
        
     this.nome_produto = "nome_produto";


/* CREATE VIEW Relacao_validade  
AS 
SELECT p.nome_produto as "Nome do Produto", TO_CHAR(v.data_validade, 'dd/mm/yyyy') 
as "Data da Validade",
  v.data_validade-now()::date AS "Dias Faltantes para Vencimento", c.categoria_produto as "Categoria do Produto",
CASE 
WHEN v.data_validade-now()::date <=0 
THEN 'Vencido'
ELSE 'Válido'
END "Status"
FROM produto p, validade v, categoria c WHERE p.cod_validade=v.cod_validade AND p.cod_categoria=c.cod_categoria;
*/
        return null;
}    

    public boolean getapagarProduto(){
        return apagarProduto();
}    
    
    public boolean apagarProduto(){
        return false;
}  

    @Override
    public String selecaoTipoCategoria(){
        
        int escolha = 0;
        String categoriaEscolhida = "";

        switch (escolha) {
            case 1 -> categoriaEscolhida = "Carnes";
            case 2 -> categoriaEscolhida = "Aves";
            case 3 -> categoriaEscolhida = "Peixes";
            case 4 -> categoriaEscolhida = "Laticínios";
            case 5 -> categoriaEscolhida = "Legumes";
            case 6 -> categoriaEscolhida = "Doces";
            case 7 -> categoriaEscolhida = "Frutas";
            case 8 -> categoriaEscolhida = "Massas";
            case 9 -> categoriaEscolhida = "Hortaliças";
            case 10 -> categoriaEscolhida = "Pães";
            case 11 -> categoriaEscolhida = "Fungos";
            default -> System.out.println("Escolha inválida.");
        }
        return categoriaEscolhida;
}

    @Override
    public String selecaoTipoConservacao(){
                
        int escolha = 0;
        String conservacaoEscolhida = "";

        switch (escolha) {
            case 1 -> conservacaoEscolhida = "Temperatura Ambiente";
            case 2 -> conservacaoEscolhida = "Refrigerado";
            case 3 -> conservacaoEscolhida = "Congelado";
            default -> System.out.println("Escolha inválida.");
        }
        return conservacaoEscolhida;
}
}