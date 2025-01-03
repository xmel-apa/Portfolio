/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package conexoes;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.PreparedStatement;

/**
 *
 * @author Lucas
 */
public class DBCategoria {

    public void inserirDadosCategoria(int cod_categoria, String categoria_produto) {
        String sql = "INSERT INTO categoria (cod_categoria,categoria_produto) VALUES (?,?)";
        
        Connection connection = null;
        PreparedStatement pstmt = null;
        
        try {
            connection = ConexaoDB.getConnection();
            pstmt = connection.prepareStatement(sql);

            pstmt.setInt(1, cod_categoria);
            pstmt.setString(2, categoria_produto);

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
        
        DBCategoria dbc = new DBCategoria();
        dbc.inserirDadosCategoria(3006,"Fungos");
    }
} 
