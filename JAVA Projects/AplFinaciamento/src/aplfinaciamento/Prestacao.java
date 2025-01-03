/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package aplfinaciamento;

    private String valor_mensal() {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }
/**
 *
 * @author pamel
 */
public class Prestacao {
    
    private float taxa;
    private int valor, tempo;
   
    
    public Prestacao(){
    
    int valor = 0;
    float taxa = 0.1f;
    int tempo = 0;
    
}

public Prestacao(int valor, float taxa, int tempo){

this.valor = valor;
this.taxa = taxa;
this.tempo = tempo;

}

    /**
     * @return the taxa
     */
    public float getTaxa() {
        return taxa;
    }

    /**
     * @param taxa the taxa to set
     */
    public void setTaxa(float taxa) {
        this.taxa = taxa;
    }

    /**
     * @return the valor
     */
    public int getValor() {
        return valor;
    }

    /**
     * @param valor the valor to set
     */
    public void setValor(int valor) {
        this.valor = valor;
    }

    /**
     * @return the tempo
     */
    public int getTempo() {
        return tempo;
    }

    /**
     * @param tempo the tempo to set
     */
    public void setTempo(int tempo) {
        this.tempo = tempo;
    }

public float taxa(){
    return this.taxa / 1200;
    
}

public float valor_mensal(){
   float n =  12* this.tempo;
    float taxa_mensal = taxa(); // Chamada do método taxa() para calcular a taxa de juros mensal
        return (float) ((this.valor * taxa_mensal) / (1 - Math.pow(1 + taxa_mensal, -n)));
    }

   //return (float) (this.valor*(this.taxa* Math.pow(1,n))/Math.pow(1,n)-1);
}



    @Override
    public String toString(){
    return "Prestação: (R$)"+valor_mensal();
    
}


