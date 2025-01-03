/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package etiqueta;
import java.time.*;
import java.time.LocalDate;
import java.time.Month;


//"Responsável": Lucas
/**
 *
 * @author x542895
 */
public class Notificacao {
    
    public String retornarNotificacao(String notificacao){
        
        Validade checkV = new Validade();
        
        if (checkV.checkVencimento() == "Vencido"){
            return "O produto está vencido";
        }
        
        if(checkV.checkVencimento() == "Perto do vencimento" ){
            return "Produto está 1 dia perto do vencimento.";
        }
        return null;
    }
    
 /*   public boolean excluirNotificacao(String exnotificacao){
        return false;
    }
   */ 
}
