/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Interface.java to edit this template
 */
package caracteristicas;

// "Responsável" Lucas

/**
 *
 * @author x542895
 */
public interface Categoria {    
    //Atributos em interfaces não podem ser privados, provavelmente precisaremos colocar em outra classe ou em produto.

    public static final String nome_categoria = "";
    public static final String CARNES = "Carnes";
    public static final String AVES = "Aves";
    public static final String PEIXES = "Peixes";
    public static final String LATICINIOS = "Latícinios";
    public static final String LEGUMES = "Legumes";
    public static final String DOCES = "Doces";        
    public static final String MASSAS = "Massas";
    public static final String FRUTAS = "Frutas";
    public static final String HORTALICAS = "Hortaliças";
    public static final String PAES = "Pães";
    public static final String FUNGOS = "Fungos";
    
    
    //Métodos em interfaces não podem ter corpo (parametros), então acho que possivelmente poderiamos puxar o metodo para
    // a classe produto e implementar os parametros lá mas fica por conta de vocês.
    
    public String selecaoTipoCategoria();
    
    public String getCategoria();
    
    public String setCategoria();
    
}