/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package etiqueta;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;


//"Responsável": Lucas

/**
 *
 * @author Lucas
 */
public class Validade {
    
    private String validade;
    private String validadefab;

    public Validade(String validade, String validadefab){
        this.validade = validade;
        this.validadefab = validadefab;
    }

    public Validade() {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    
    public String checkVencimento() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        LocalDate validadeDate;

        try {
            validadeDate = LocalDate.parse(validade, formatter);
        } catch (DateTimeParseException e) {
            e.printStackTrace();
            return "Data inválida";  // Retorna "Data inválida" se a data de validade não puder ser analisada
        }

        // Obtém a data atual
        LocalDate today = LocalDate.now();

        // Verifica se a data de validade é anterior à data atual
        if (validadeDate.isBefore(today.minusDays(1))) {
            return "Perto do vencimento";
        }

        // Verifica se a data de validade é um dia após a data atual
        if (validadeDate.isEqual(today.plusDays(1))) {
            return "Produto Vencido";
        }

        return "Válido";
    }
    
    public void inserirDataValidade(String validade, String tableName, String columnName) {
        // Formato da data esperado
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        LocalDate localDate = null;
        
        try {
            // Conversão da string para java.time.LocalDate
            localDate = LocalDate.parse(validade, formatter);
        } catch (DateTimeParseException e) {
            e.printStackTrace();
        }
    }
    
       public void inserirDataValidadeFab(String validadefab, String tableName, String columnName) {
        // Formato da data esperado
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        LocalDate localDate = null;
        
        try {
            // Conversão da string para java.time.LocalDate
            localDate = LocalDate.parse(validadefab, formatter);
        } catch (DateTimeParseException e) {
            e.printStackTrace();
        }
    }
    
    /**
     * @return the validade
     */
    public String getValidade(){
        return validade;
    }

    /**
     * @param validade the validade to set
     */
    public void setValidade(String validade) {
        this.validade = validade;
    }

    /**
     * @return the validadefab
     */
    public String getValidadefab() {
        return validadefab;
    }

    /**
     * @param validadefab the validadefab to set
     */
    public void setValidadefab(String validadefab) {
        this.validadefab = validadefab;
    }
}