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
public class DBEmpresa {

    
     public void inserirDadosEmpresa(int cnpj, String razao_social, String nome_fantasia) {
        String sql = "INSERT INTO empresa (cnpj,razao_social,nome_fantasia) VALUES (?,?,?)";
        
        Connection connection = null;
        PreparedStatement pstmt = null;
        
        try {
            connection = ConexaoDB.getConnection();
            pstmt = connection.prepareStatement(sql);

            pstmt.setInt(1, cnpj);
            pstmt.setString(2, razao_social);
            pstmt.setString(3, nome_fantasia);

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
        
        DBEmpresa dbempresa = new DBEmpresa();
        dbempresa.inserirDadosEmpresa(1211,"General Motors do Brasil S.A","Chevrolet");
    }
} 