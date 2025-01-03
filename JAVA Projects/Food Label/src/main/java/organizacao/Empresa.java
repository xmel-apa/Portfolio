/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package organizacao;


public class Empresa {
    private String razaoSocial;
    private String nomeSocial;
    private String cnpj;
    
    // Construtor
    public Empresa(String razaoSocial, String nomeSocial, String cnpj) {
        this.razaoSocial = razaoSocial;
        this.nomeSocial = nomeSocial;
        this.cnpj = cnpj;
    }

    /**
     * @return the razaoSocial
     */
    public String getRazaoSocial() {
        return razaoSocial;
    }

    /**
     * @param razaoSocial the razaoSocial to set
     */
    public void setRazaoSocial(String razaoSocial) {
        this.razaoSocial = razaoSocial;
    }

    /**
     * @return the nomeSocial
     */
    public String getNomeSocial() {
        return nomeSocial;
    }

    /**
     * @param nomeSocial the nomeSocial to set
     */
    public void setNomeSocial(String nomeSocial) {
        this.nomeSocial = nomeSocial;
    }

    /**
     * @return the cnpj
     */
    public String getCnpj() {
        return cnpj;
    }

    /**
     * @param cnpj the cnpj to set
     */
    public void setCnpj(String cnpj) {
        this.cnpj = cnpj;
    }
    
    @Override
    public String toString() {
        return "Empresa{" +
                "razaoSocial='" + razaoSocial + '\'' +
                ", nomeSocial='" + nomeSocial + '\'' +
                ", cnpj='" + cnpj + '\'' +
                '}';
    }
}