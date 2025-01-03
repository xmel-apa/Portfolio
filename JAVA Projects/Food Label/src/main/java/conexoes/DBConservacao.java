/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package conexoes;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/**
 *
 * @author Lucas
 */
public class DBConservacao {
    
     public void inserirDadosConservacao(int cod_conservacao, String ind_conserve) {
        String sql = "INSERT INTO conservacao (cod_conservacao,ind_conserve) VALUES (?,?)";
        
        Connection connection = null;
        PreparedStatement pstmt = null;
        
        try {
            connection = ConexaoDB.getConnection();
            pstmt = connection.prepareStatement(sql);

            pstmt.setInt(1, cod_conservacao);
            pstmt.setString(2, ind_conserve);

            int rowsAffected = pstmt.executeUpdate();
            if (rowsAffected > 0) {
                System.out.println("Inserção realizada com sucesso!");
            }

        } catch (SQLException e) {
            System.out.println("Erro ao inserir dados: " + e.getMessage());
        } finally {
            if (pstmt != null) {
                try {
                    pstmt.close();
                } catch (SQLException e) {
                    System.out.println("Erro ao fechar PreparedStatement: " + e.getMessage());
                }
            }
            ConexaoDB.closeConnection(connection);
        }
    }

    public static void main(String[] args) {
        
        DBConservacao dbconservacao = new DBConservacao();
        dbconservacao.inserirDadosConservacao(711,"Congelado");
    }
} 

