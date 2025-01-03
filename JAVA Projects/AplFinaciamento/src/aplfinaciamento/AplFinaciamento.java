 /*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package aplfinaciamento;
import java.util.Scanner;
/**
 *
 * @author pamel
 */
public class AplFinaciamento {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        Scanner scan = new Scanner(System.in);
        System.out.println("Valor:       \n");
        int valor = scan.nextInt();
        System.out.println("Taxa Anual:  \n");
        float taxa = scan.nextFloat();
        System.out.println("Tempo(anos):   ");
        int tempo = scan.nextInt();
        
        Prestacao prestacao = new Prestacao(valor,taxa,tempo);
    
}
}